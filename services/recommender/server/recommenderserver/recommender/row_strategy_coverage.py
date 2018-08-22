import requests
import csv
from learner_inferences_client import Learner
from recommenderserver.recommender.config import RowStrategyConfig, CassGraph
from recommenderserver.recommender.query_cacher import QueryCacher
from recommenderserver.recommender.utils import load_or_instantiate


activities_json = requests.get("insertIPAddr/activity-index/activities").json()

ELO_alignments = {}
cached_CASS_comp_nums = {}
ELO_num_to_obj = {}
cass_graph = load_or_instantiate('recommenderserver.resources', CassGraph, '59e884bb-510b-4f36-8443-8c3842336e28')

print("Getting ELO data from CASS...")
CASS_framework = requests.get("http://insertCassUrl/api/data/insertCassSchemaUrl.0.3.Framework/59e884bb-510b-4f36-8443-8c3842336e28").json()
CASS_competency_urls = CASS_framework["competency"]
for comp_url in CASS_competency_urls:
    ELO_number = requests.get(comp_url).json()["ceasn:codedNotation"]
    # Skip TLOs since they don't have activities
    if "." not in ELO_number:
        continue
    ELO_alignments[ELO_number] = []
    cached_CASS_comp_nums[comp_url] = ELO_number
    ELO_num_to_obj[ELO_number] = cass_graph.get_obj_by_id(comp_url)


print("Getting ELO alignments from activities...")
for activity in activities_json:
    ELO_identifier = activity["identifier"]

    # Skip debug activities, and pre/post tests
    skip_it = False
    for item in ["Debug", "PreTest", "PostTest"]:
        if item in activity.get("educationalUse", []):
            skip_it = True
            break

    if skip_it:
        print('Skipping: item={} found in educationalUse={}'.format(item, activity.get('educationalUse')))
        continue
    else:
        print('Not Skipping: items={} not found in educationalUse={}'.format(["Debug", "PreTest", "PostTest"], activity.get('educationalUse')))

    for item in activity["educationalAlignment"]:
        if item["additionalType"] == "ELOAlignment":
            try:
                target_url = item["targetUrl"]
                if target_url in cached_CASS_comp_nums:
                    ELO_number = cached_CASS_comp_nums[target_url]
                else:
                    comp_data = requests.get(item["targetUrl"]).json()
                    ELO_number = comp_data["ceasn:codedNotation"]
            except:
                print("Couldn't get ELOAlignment data for activity " + ELO_identifier)
                continue

            if ELO_number not in ELO_alignments:
                ELO_alignments[ELO_number] = [activity]
            else:
                ELO_alignments[ELO_number].append(activity)

print("\n\n\nActivity/Assessment Alignments:")


sorted_ELO_nums = sorted(ELO_alignments.keys())

print('Setting up the row strategies')
query_cacher = QueryCacher()
learner = Learner(name="dummy", identifier="dummy", context="dummy", type="Learner", mastery_estimates=[], activity_attempt_counters=[])
elo_row_strats = [
            row_strategy(learner=learner, query_cacher=query_cacher, cass_graph=cass_graph,
                         filter_locked_activities=True) for row_strategy in RowStrategyConfig.DEFAULT_COMPETENCY_ROW_STRATEGIES]

print('Running all the strategy on each ELO and saving the returned activity ids')
ELO_num_to_strategy_results = {}
for ELO_num in sorted_ELO_nums:

    ELO_num_to_strategy_results[ELO_num] = {}
    for strat in elo_row_strats:
        recommendation_row = strat.instantiate_row(ELO_num_to_obj[ELO_num])
        ELO_num_to_strategy_results[ELO_num][strat.__class__.__name__] = [] if recommendation_row is None else [a.activity_id for a in recommendation_row.activities]


with open('ELO_Row_Strategy_Results_by_ELO.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['ELO#', 'Strategy Name', 'Activities'])

    print('\n\n\n')
    print("ELO Row Strategy Results, by ELO")
    print('ELO:{:<10} | strat_name:{:<38} | activities:{}'.format('','',''))
    for ELO_num, strat_results in ELO_num_to_strategy_results.items():
        print('-'*90)
        for strat_name, activities in strat_results.items():
            print('ELO:{:<10} | strat_name:{:<38} | activities:{}'.format(ELO_num, strat_name, activities))
            writer.writerow([ELO_num, strat_name, activities])

with open('Applicable_Activities_and_ELO_Row_Strategies_that_Return_them_by_ELO.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['ELO#', 'Activity', 'Educational Uses', 'Applicable ELO Row Strategies'])

    print('\n\n\n')
    print("Applicable Activities & ELO Row Strategies that Return them, by ELO")
    print('ELO:{:6.6} | activity:{:30.30} | Educational Uses:{:40.40} | Applicable ELO Row Strategies:{}'.format('','','',''))
    for ELO_num in sorted_ELO_nums:
        print('-' * 90)
        if len(ELO_alignments[ELO_num]) == 0:
            print('ELO:{:6.6} | No Activities{:26.26} | N/A{:54.54} | N/A'.format(ELO_num, '', ''))
            writer.writerow([ELO_num, 'No Activities', 'N/A', 'N/A'])
            continue

        for activity in ELO_alignments[ELO_num]:
            activity_name = activity["name"]
            educational_uses = activity["educationalUse"]
            applicable_strat_names = []

            for strat_name, activities in ELO_num_to_strategy_results[ELO_num].items():
            # for ELO_num, strat_results in ELO_num_to_strategy_results.items():
            #     for strat_name, activities in strat_results.items():
                if activity["identifier"] in activities:
                    applicable_strat_names.append(strat_name)
            print('ELO:{:6.6} | activity:{:30.30} | Educational Uses:{!s:40.40s} | Applicable ELO Row Strategies:{}'.format(ELO_num, activity_name, educational_uses, applicable_strat_names))
            writer.writerow([ELO_num, activity_name, educational_uses, applicable_strat_names])
            # print("    " + activity_name + " - " + str(educational_uses))
