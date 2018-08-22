from __future__ import absolute_import

import unittest
from copy import deepcopy
from typing import List
from unittest import mock
from unittest.mock import Mock

import dateutil
import recommenderserver
import recommenderserver.recommender.config
from activity_index_client import LearningActivity
from cass_graph_client.cass_graph import CassGraph
from learner_inferences_client import Learner, ActivityAttemptCounter, MasteryEstimate, CompetencyAttemptCounter, Goal
from recommenderserver.config import CassConfig
from recommenderserver.recommender.query_cacher import QueryCacher
from recommenderserver.recommender.recommender import MandatoryAssignmentMaker, Recommendation, Recommender
from recommenderserver.recommender.row_strategies import AllActivities, Shiny, MoveToNextSection
from recommenderserver.recommender.row_strategies import AffectConfusedOrNew, ReviewActivities, \
    AffectBored, AffectFrustratedOrBored, PopularActivities, \
    HighestRatedActivities, ChallengingActivities, IntermediateActivities, IntroductoryActivities, NewCompetency
from recommenderserver.recommender.utils import get_current_elos, is_shiny, is_assessment_for_elo, \
    filter_assessment_activities
from recommenderserver.recommender.utils import get_last_activity_url_identifier, \
    mongo_id_from_url, MagicStrings, get_aligned_elo
from recommenderserver.test import utils
from recommenderuisupportclient.models import LearnerTokens


class RecommenderTest(unittest.TestCase):

    # <editor-fold desc="Test Setup">

    @classmethod
    def setUpClass(cls):
        if utils.cass_pickle_exists():
            cls.cass_graph = utils.load_cass_graph()
        else:
            cls.cass_graph = CassGraph("59e884bb-510b-4f36-8443-8c3842336e28")
            utils.dump_cass_graph(cls.cass_graph)

        cls._name_to_learners, cls._id_to_learners = utils.load_test_learners()
        cls._name_to_activity, cls._id_to_activity = utils.load_test_activities()
        cls._all_activities = utils.load_test_activities_all()
        cls._id_to_learner_tokens = utils.load_test_tokens()

    def setUp(self):
        self.name_to_learners = deepcopy(self._name_to_learners)
        self.id_to_learners = deepcopy(self._id_to_learners)
        self.name_to_activity = deepcopy(self._name_to_activity)
        self.id_to_activity = deepcopy(self._id_to_activity)
        self.all_activities = deepcopy(self._all_activities)
        self.id_to_learner_tokens = deepcopy(self._id_to_learner_tokens)

    # </editor-fold>

    # <editor-fold desc="MandatoryAssignmentMaker tests">

    def test_recommend_check_on_learning_assessment(self):
        # Given a learner that has taken at least one LearningActivity
        john_superlearner = self.name_to_learners['John Superlearner']

        # And the most recent activity has a check on learning assessment educational alignment object
        last_activity = self._get_activity(mongo_id_from_url(get_last_activity_url_identifier(john_superlearner)))

        check_on_learning_alignment = last_activity.educational_alignment[-1]
        self.assertEqual(MagicStrings.AdditionalTypes.APPROPRIATE_ASSESSMENT_ALIGNMENT,
                         check_on_learning_alignment.additional_type)

        # When an assignment is requested from the mandatory assignment maker
        assignment = self._default_assignment_request(john_superlearner)

        # Then a Recommendation object is returned where the assignment id corresponds
        # to a formative assessment that assess the learners last activity
        self.assertEqual(check_on_learning_alignment.target_url, assignment.assignment.activity_id)

    def test_recommend_self_report_after_activity_if_there_is_no_check_on_learning_assessment(self):
        # Given a learner
        john_superlearner = self.name_to_learners['John Superlearner']

        # Who's last activity is not an assessment
        last_activity = self._get_activity(mongo_id_from_url(get_last_activity_url_identifier(john_superlearner)))

        self.assertEqual(self.name_to_activity['Mastering Cookie Making'].identifier, last_activity.identifier)
        self.assertNotIn(last_activity.learning_resource_type,
                         MagicStrings.LearningResourceTypes.get_assessment_types())

        # And who's last activity has no check on learning assessment
        # (Remove the check on learning alignment object which is last elem in list... hacky)
        last_activity.educational_alignment.pop(-1)

        # When get mandatory assignment is called
        assignment = self._default_assignment_request(john_superlearner)

        # Then the recommendation assignment is the self report
        self.assertEqual(MagicStrings.UnitTestAssertions.SELF_REPORT_URL_IDENTIFIER, assignment.assignment.activity_id)

    def test_recommend_self_report_after_learner_has_taken_a_normal_learning_activity(self):
        # Given a learner
        john_superlearner = self.name_to_learners['John Superlearner']

        # Who's last activity WAS a normal learning activity
        john_superlearner.activity_attempt_counters.append(ActivityAttemptCounter(context="tla-declarations.jsonld",
                                                                                  type="ActivityAttemptCounter",
                                                                                  activity_id="https://activity-index-service/activities/5099803df3f4948bd2f98391",
                                                                                  attempts=1,
                                                                                  last_attempt_date_time=dateutil.parser.parse(
                                                                                      "2019-02-25T12:25:00")))

        # And has already taken the self-report
        john_superlearner.activity_attempt_counters.append(ActivityAttemptCounter(context="tla-declarations.jsonld",
                                                                                  type="ActivityAttemptCounter",
                                                                                  activity_id="https://activity-index-service/activities/995abcddf3f494selfreport",
                                                                                  attempts=1,
                                                                                  last_attempt_date_time=dateutil.parser.parse(
                                                                                      "2019-02-26T12:25:00")))

        # When get mandatory assignment is called
        assignment = self._default_assignment_request(john_superlearner)

        # Then the recommendation assignment is the self report
        self.assertEqual("https://activity-index-service/activities/995abcddf3f494selfreport", assignment.assignment.activity_id)

    def test_recommend_unit_assessment_posttest_for_tlo_when_leaner_has_just_mastered_a_tlo(self):
        with mock.patch.object(
            recommenderserver.recommender.config.MandatoryAssignmentMakerConfig, 'TLO_UNIT_ASSESSMENT', return_value=True
        ):
            # Given a learner
            john_superlearner = self.name_to_learners['John Superlearner']

            # Who has taken a learning assessment
            john_superlearner.activity_attempt_counters.append(ActivityAttemptCounter(context="tla-declarations.jsonld",
                                                                                      type="ActivityAttemptCounter",
                                                                                      activity_id="https://activity-index-service/activities/5b00c8372a78f29959236bd2",
                                                                                      attempts=1,
                                                                                      last_attempt_date_time=dateutil.parser.parse(
                                                                                          "2019-02-25T12:25:00")))
            # And taken a self report
            john_superlearner.activity_attempt_counters.append(ActivityAttemptCounter(context="tla-declarations.jsonld",
                                                                                      type="ActivityAttemptCounter",
                                                                                      activity_id="https://activity-index-service/activities/5b01c5c92a78f29959236bd4",
                                                                                      attempts=1,
                                                                                      last_attempt_date_time=dateutil.parser.parse(
                                                                                          "2019-02-25T12:30:00")))

            # And who holds mastery for all ELOs in a TLO
            tlo = self.cass_graph.get_first_top_level_competency()
            elos = self.cass_graph.get_competency_chain(tlo)
            john_superlearner.mastery_estimates = list()
            for elo in elos:
                self._master_competency(elo, john_superlearner)
            # But has not taken the unit assessment for that TLO
            self.assertFalse(self._tlo_held_in_mastery_estimates(tlo.id, john_superlearner))

            # When get mandatory assignment is called
            assignment = self._default_assignment_request(john_superlearner)

            # Then the recommendation assignment is the posttest unit assessment for that TLO
            self.assertEqual(MagicStrings.UnitTestAssertions.UNIT_ASSESSMENT_IDENTIFIER, assignment.assignment.activity_id)

    def test_recommend_unit_assessment_posttest_for_tlo_when_leaner_has_previously_failed_the_assessment(self):
        with mock.patch.object(
                recommenderserver.recommender.config.MandatoryAssignmentMakerConfig, 'TLO_UNIT_ASSESSMENT',
                return_value=True
        ):
            # Given a learner
            john_superlearner = self.name_to_learners['John Superlearner']

            # Who has taken a learning assessment
            john_superlearner.activity_attempt_counters.append(ActivityAttemptCounter(context="tla-declarations.jsonld",
                                                                                      type="ActivityAttemptCounter",
                                                                                      activity_id="https://activity-index-service/activities/5b00c8372a78f29959236bd2",
                                                                                      attempts=1,
                                                                                      last_attempt_date_time=dateutil.parser.parse(
                                                                                          "2019-02-25T12:25:00")))
            # And taken a self report
            john_superlearner.activity_attempt_counters.append(ActivityAttemptCounter(context="tla-declarations.jsonld",
                                                                                      type="ActivityAttemptCounter",
                                                                                      activity_id="https://activity-index-service/activities/5b01c5c92a78f29959236bd4",
                                                                                      attempts=1,
                                                                                      last_attempt_date_time=dateutil.parser.parse(
                                                                                          "2019-02-25T12:30:00")))

            # Who holds mastery for all ELOs in a TLO
            tlo = self.cass_graph.get_first_top_level_competency()
            elos = self.cass_graph.get_competency_chain(tlo)
            john_superlearner.mastery_estimates = list()
            for elo in elos:
                self._master_competency(elo, john_superlearner)
            # But has not passed the unit assessment for that TLO
            john_superlearner.mastery_estimates.append(MasteryEstimate(context="tla-declarations.jsonld",
                                                                       type="MasteryEstimate",
                                                                       competency_id=tlo.id,
                                                                       mastery=MagicStrings.MasteryEstimates.NOT_HELD,
                                                                       timestamp="2018-10-15T11:40:07"))

            # And has not taken the unit assessment for that TLO in the past 3 normal activities (non-assessment, non-self-report)
            john_superlearner.activity_attempt_counters.append(ActivityAttemptCounter(context="tla-declarations.jsonld",
                                                                                      type="ActivityAttemptCounter",
                                                                                      activity_id="https://activity-index-service/activities/5099803df3f4948bd2f98391",
                                                                                      attempts=1,
                                                                                      last_attempt_date_time=dateutil.parser.parse(
                                                                                          "2019-02-25T12:25:00")))

            john_superlearner.activity_attempt_counters.append(ActivityAttemptCounter(context="tla-declarations.jsonld",
                                                                                      type="ActivityAttemptCounter",
                                                                                      activity_id="https://activity-index-service/activities/5099803df3f4948bd2f98391",
                                                                                      attempts=1,
                                                                                      last_attempt_date_time=dateutil.parser.parse(
                                                                                          "2019-02-25T12:25:00")))

            john_superlearner.activity_attempt_counters.append(ActivityAttemptCounter(context="tla-declarations.jsonld",
                                                                                      type="ActivityAttemptCounter",
                                                                                      activity_id="https://activity-index-service/activities/5099803df3f4948bd2f98391",
                                                                                      attempts=1,
                                                                                      last_attempt_date_time=dateutil.parser.parse(
                                                                                          "2019-02-25T12:25:00")))

            # Who has taken a learning assessment
            john_superlearner.activity_attempt_counters.append(ActivityAttemptCounter(context="tla-declarations.jsonld",
                                                                                      type="ActivityAttemptCounter",
                                                                                      activity_id="https://activity-index-service/activities/5b00c8372a78f29959236bd2",
                                                                                      attempts=1,
                                                                                      last_attempt_date_time=dateutil.parser.parse(
                                                                                          "2019-02-25T12:25:00")))
            # And taken a self report
            john_superlearner.activity_attempt_counters.append(ActivityAttemptCounter(context="tla-declarations.jsonld",
                                                                                      type="ActivityAttemptCounter",
                                                                                      activity_id="https://activity-index-service/activities/5b01c5c92a78f29959236bd4",
                                                                                      attempts=1,
                                                                                      last_attempt_date_time=dateutil.parser.parse(
                                                                                          "2019-02-25T12:30:00")))

            # When get mandatory assignment is called
            assignment = self._default_assignment_request(john_superlearner)

            # Then the recommendation assignment is the posttest unit assessment for that TLO
            self.assertEqual("https://activity-index-service/activities/995abcddf3f494selfreport", assignment.assignment.activity_id)

    def test_do_not_recommend_unit_assessment_posttest_for_tlo_when_leaner_has_previously_failed_the_assessment_if_they_took_the_assessment_recently(
            self):
        # Given a learner
        john_superlearner = self.name_to_learners['John Superlearner']

        # Who has taken a learning assessment
        john_superlearner.activity_attempt_counters.append(ActivityAttemptCounter(context="tla-declarations.jsonld",
                                                                                  type="ActivityAttemptCounter",
                                                                                  activity_id="https://activity-index-service/activities/5b00c8372a78f29959236bd2",
                                                                                  attempts=1,
                                                                                  last_attempt_date_time=dateutil.parser.parse(
                                                                                      "2019-02-25T12:25:00")))
        # And taken a self report
        john_superlearner.activity_attempt_counters.append(ActivityAttemptCounter(context="tla-declarations.jsonld",
                                                                                  type="ActivityAttemptCounter",
                                                                                  activity_id="https://activity-index-service/activities/5b01c5c92a78f29959236bd4",
                                                                                  attempts=1,
                                                                                  last_attempt_date_time=dateutil.parser.parse(
                                                                                      "2019-02-25T12:30:00")))

        # Who holds mastery for all ELOs in a TLO
        tlo = self.cass_graph.get_first_top_level_competency()
        elos = self.cass_graph.get_competency_chain(tlo)
        john_superlearner.mastery_estimates = list()
        for elo in elos:
            self._master_competency(elo, john_superlearner)
        # But has not passed the unit assessment for that TLO
        john_superlearner.mastery_estimates.append(MasteryEstimate(context="tla-declarations.jsonld",
                                                                   type="MasteryEstimate",
                                                                   competency_id=tlo.id,
                                                                   mastery=MagicStrings.MasteryEstimates.NOT_HELD,
                                                                   timestamp="2018-10-15T11:40:07"))

        # And HAS taken the unit assessment for that TLO in the past 3 normal activities (non-assessment, non-self-report)
        john_superlearner.activity_attempt_counters.append(ActivityAttemptCounter(context="tla-declarations.jsonld",
                                                                                  type="ActivityAttemptCounter",
                                                                                  activity_id="https://activity-index-service/activities/5b01c5c92a78f29959236bd5",
                                                                                  attempts=1,
                                                                                  last_attempt_date_time=dateutil.parser.parse(
                                                                                      "2018-10-15T11:40:07")))

        # When get mandatory assignment is called
        assignment = self._default_assignment_request(john_superlearner)

        # Then the recommendation assignment is NOT the posttest unit assessment for that TLO
        if assignment is not None:
            self.assertNotEquals(MagicStrings.UnitTestAssertions.UNIT_ASSESSMENT_IDENTIFIER,
                                 assignment.assignment.activity_id)

    # </editor-fold>

    # <editor-fold desc="Recommendation RowStrategy tests">

    def test_new_user(self):
        # Given a learner
        john_superlearner = self.name_to_learners['John Superlearner']

        # Who has done nothing
        john_superlearner = self._clear_user(john_superlearner)

        # When recommendation is called
        recommendation = self._default_recommender_request(john_superlearner)

        # Recommendation rows should be produced
        self.assertNotEqual(recommendation.recommendations, None)

        # Learner should have a recommendation for primer activities
        self.assertTrue(self._strategy_in_recommendation(recommendation, AffectConfusedOrNew.__name__))
        # That contains the following activities
        self.assertTrue(self._activities_in_recommendation(recommendation, AffectConfusedOrNew.__name__, [
            'https://activity-index-service/activities/5b01c5c92a78f29959236bd6']))

        # And a recommendation for popular activities
        self.assertTrue(self._strategy_in_recommendation(recommendation, PopularActivities.__name__))
        # That contains the following activities
        self.assertTrue(self._activities_in_recommendation(recommendation, PopularActivities.__name__, [
            'https://activity-index-service/activities/5b01c5c92a78f29959236bd6',
            'https://activity-index-service/activities/5b01c5c92a78f29959236bd7',
            'https://activity-index-service/activities/5b01c5c92a78f29959236bd8',
            'https://activity-index-service/activities/5b01c5c92a78f2995another']))

        # And a recommendation for the highest rated activities
        self.assertTrue(self._strategy_in_recommendation(recommendation, HighestRatedActivities.__name__))
        # That contains the following activities
        self.assertTrue(self._activities_in_recommendation(recommendation, HighestRatedActivities.__name__, [
            'https://activity-index-service/activities/5b01c5c92a78f29959236bd6',
            'https://activity-index-service/activities/5b01c5c92a78f29959236bd7',
            'https://activity-index-service/activities/5b01c5c92a78f29959236bd8',
            'https://activity-index-service/activities/5b01c5c92a78f2995another']))

    def test_bored_user(self):
        # Given a learner
        john_superlearner = self.name_to_learners['John Superlearner']

        # Who starts with nothing
        john_superlearner = self._clear_user(john_superlearner)

        # Who is bored
        john_superlearner.bored = True

        # When recommendation is called
        recommendation = self._default_recommender_request(john_superlearner)

        # Recommendation rows should be produced
        self.assertNotEqual(recommendation.recommendations, None)

        # Learner should have a recommendation for Challenging and Interactive Activities
        self.assertTrue(self._strategy_in_recommendation(recommendation, AffectBored.__name__))
        # That contains the following activities
        self.assertTrue(self._activities_in_recommendation(recommendation, AffectBored.__name__,
                                                           [
                                                               'https://activity-index-service/activities/5b01c5c92a78f29959236bd8']))

        # And a should have a recommendation for Approachable and Interactive Activities
        self.assertTrue(self._strategy_in_recommendation(recommendation, AffectFrustratedOrBored.__name__))
        # That contains the following activities
        self.assertTrue(
            self._activities_in_recommendation(recommendation, AffectFrustratedOrBored.__name__,
                                               ['https://activity-index-service/activities/5b01c5c92a78f29959236bd7']))

    def test_frustrated_user(self):
        # Given a learner
        john_superlearner = self.name_to_learners['John Superlearner']

        # Who starts with nothing
        john_superlearner = self._clear_user(john_superlearner)

        # Who is bored
        john_superlearner.frustrated = True

        # When recommendation is called
        recommendation = self._default_recommender_request(john_superlearner)

        # Recommendation rows should be produced
        self.assertNotEqual(recommendation.recommendations, None)

        # Learner should NOT have a recommendation for Challenging and Interactive Activities
        self.assertFalse(self._strategy_in_recommendation(recommendation, AffectBored.__name__))

        # And a should have a recommendation for Approachable and Interactive Activities
        self.assertTrue(self._strategy_in_recommendation(recommendation, AffectFrustratedOrBored.__name__))
        # That contains the following activities
        self.assertTrue(
            self._activities_in_recommendation(recommendation, AffectFrustratedOrBored.__name__,
                                               ['https://activity-index-service/activities/5b01c5c92a78f29959236bd7']))

    def test_review(self):
        # Given a learner
        john_superlearner = self.name_to_learners['John Superlearner']

        # Who starts with nothing
        john_superlearner = self._clear_user(john_superlearner)

        # Who then forgets an ELO
        tlo = self.cass_graph.get_first_top_level_competency()
        elos = self.cass_graph.get_competency_chain(tlo)
        elo = elos[0]
        john_superlearner.mastery_estimates.append(MasteryEstimate(context="tla-declarations.jsonld",
                                                                   type="MasteryEstimate",
                                                                   competency_id=elo.id,
                                                                   mastery="forgot",
                                                                   timestamp="2018-10-15T11:25:07"))

        # When a recommendation is called
        recommendation = self._default_recommender_request(john_superlearner)

        # Recommendation rows should be produced
        self.assertNotEqual(recommendation.recommendations, None)

        # Learner should have a recommendation for Review Activities in up to 3 forgotten ELOs
        self.assertTrue(self._strategy_in_recommendation(recommendation, ReviewActivities.__name__))
        # That contains the following activities
        self.assertTrue(self._activities_in_recommendation(recommendation, ReviewActivities.__name__, [
            'https://activity-index-service/activities/5b01c5c92a78f29959236bd9']))

    def test_something_new_strategy_returns_activities_for_an_elo_where_the_user_has_no_competency_attempts(self):
        # Given a learner
        john_superlearner = self.name_to_learners['John Superlearner']

        john_superlearner = self._clear_user(john_superlearner)

        target_parent_id = 'https://insertCassUrl/api/data/insertCassSchemaUrl.0.3.Competency/6bdc90f5-6d6c-4884-9581-dc2e0c9c07f1'
        john_superlearner.goals.append(Goal(
            context='http://insertCassSchemaUrl/0.3',
            competency_id=target_parent_id,
            type='Goal'
        ))

        self._clear_user(john_superlearner)

        target_elo_id = 'https://insertCassUrl/api/data/insertCassSchemaUrl.0.3.Competency/86b50eaa-74e2-412f-b858-9d5610b52bef'

        # Who only has one non-mastered and attempted elo
        for competency in self.cass_graph.get_entire_chain():
            if competency.id != target_elo_id and competency.id != target_parent_id:
                # print(competency.id)
                self._master_competency(competency, john_superlearner)
                self._add_competency_attempt(competency, john_superlearner)

        active_elos = get_current_elos(john_superlearner, self.cass_graph)
        self.assertEqual(len(active_elos), 1)
        active_elo = active_elos[0]

        self.assertTrue(CassConfig.ILL_DEFINED_CONCEPT_TERM in active_elo.ceasnconcept_term)
        self.assertEqual(active_elo.id, target_elo_id)


        # Then the SomethingNew strategy can only instantiate that ELO
        query_mock = self._default_query_mock()
        strategy = NewCompetency(john_superlearner, query_mock, self.cass_graph, False)
        applicable_elos = strategy.can_instantiate(active_elos)
        self.assertTrue(len(applicable_elos) == 1)
        applicable_elo = applicable_elos[0]
        self.assertEqual(applicable_elo, active_elo)

        # And when a recommendation is made with that elo
        row = strategy.instantiate_row(applicable_elo)

        # Then the recommendation has activities for only that ELO
        activities = [query_mock.get_activity(mongo_id_from_url(recommended_activity.activity_id)) for
                      recommended_activity in row.activities]
        self.assertTrue(all(get_aligned_elo(activity) == applicable_elo.id for activity in activities))

    def test_something_new_strategy_not_returned_in_well_defined_case(self):
        # Given a learner
        john_superlearner = self.name_to_learners['John Superlearner']
        self._clear_user(john_superlearner)

        # who is in the well-defined case (a new learner in this case)
        active_elos = get_current_elos(john_superlearner, self.cass_graph)
        self.assertEqual(len(active_elos), 1)
        elo = active_elos[0]
        self.assertIn(CassConfig.WELL_DEFINED_CONCEPT_TERM, elo.ceasnconcept_term)

        # When the SomethingNew strategy is called
        strategy = NewCompetency(john_superlearner, self._default_query_mock(), self.cass_graph, False)
        applicable_elos = strategy.can_instantiate(active_elos)

        # The strategy can not be applied to any elos
        self.assertEqual(len(applicable_elos), 0)

    def test_locked_activity(self):
        # Given a learner
        john_superlearner = self.name_to_learners['John Superlearner']

        # Who starts with nothing
        john_superlearner = self._clear_user(john_superlearner)

        # Who has taken a learning assessment
        john_superlearner.activity_attempt_counters.append(ActivityAttemptCounter(context="tla-declarations.jsonld",
                                                                                  type="ActivityAttemptCounter",
                                                                                  activity_id="https://activity-index-service/activities/5b00c8372a78f29959236bd2",
                                                                                  attempts=1,
                                                                                  last_attempt_date_time=dateutil.parser.parse(
                                                                                      "2019-02-25T12:25:00")))
        # And taken a self report
        john_superlearner.activity_attempt_counters.append(ActivityAttemptCounter(context="tla-declarations.jsonld",
                                                                                  type="ActivityAttemptCounter",
                                                                                  activity_id="https://activity-index-service/activities/5b01c5c92a78f29959236bd4",
                                                                                  attempts=1,
                                                                                  last_attempt_date_time=dateutil.parser.parse(
                                                                                      "2019-02-25T12:30:00")))

        # And who holds mastery for all ELOs in the First TLO
        tlo = self.cass_graph.get_first_top_level_competency()
        elos = self.cass_graph.get_competency_chain(tlo)
        john_superlearner.mastery_estimates = list()
        for elo in elos:
            self._master_competency(elo, john_superlearner)

        # And holds mastery for the first TLO
        self._master_competency(tlo, john_superlearner)

        # And who has started a the second ELO in the second
        tlo2 = self.cass_graph.get_next_neighbor(tlo)
        elos2 = self.cass_graph.get_competency_chain(tlo2)
        john_superlearner.mastery_estimates.append(MasteryEstimate(context="tla-declarations.jsonld",
                                                                   type="MasteryEstimate",
                                                                   competency_id=elos2[0].id,
                                                                   mastery="indeterminate",
                                                                   timestamp="2018-10-15T11:25:07"))

        # When a recommendation is called
        recommendation = self._default_recommender_request(john_superlearner)

        # The Real World activity should not appear in any recommendation row.
        self.assertFalse(self._activities_in_any_recommendation(recommendation, [
            "https://activity-index-service/activities/5b01c5c92a78f29959236be0"]))

    def test_shiny_strategy(self):
        # Given a learner
        john_superlearner = self.name_to_learners['John Superlearner']
        john_superlearner = self._clear_user(john_superlearner)

        # With an active ELO
        active_elos = get_current_elos(john_superlearner, self.cass_graph)
        self.assertEqual(len(active_elos), 1)
        elo = active_elos[0]

        # When the Shiny strategy is called
        query_mock = self._default_query_mock()
        strategy = Shiny(john_superlearner, query_mock, self.cass_graph, False)
        applicable_elos = strategy.can_instantiate(active_elos)
        self.assertEqual(len(applicable_elos), 1)
        applicable_elo = applicable_elos[0]
        self.assertEqual(elo, applicable_elo)

        # Then it returns shiny activities
        row = strategy.instantiate_row(applicable_elo)
        activities = [query_mock.get_activity(mongo_id_from_url(recommended_activity.activity_id)) for recommended_activity in row.activities]
        self.assertGreater(len(activities), 0)
        self.assertTrue(all(is_shiny(activity) for activity in activities))

    # </editor-fold>

    # <editor-fold desc="Deduplication tests">

    def test_activity_should_not_appear_in_multiple_recommendation_rows(self):
        # Given a user
        john_superlearner = self.name_to_learners['John Superlearner']
        # Who has done nothing
        john_superlearner = self._clear_user(john_superlearner)

        # And Two Primer Row Strategies
        primer_strategy_1 = AffectConfusedOrNew(john_superlearner, self._default_query_mock(), self.cass_graph, True)
        primer_strategy_2 = AffectConfusedOrNew(john_superlearner, self._default_query_mock(), self.cass_graph, True)

        # And an activity that is returned by both strategies for that user
        activity_id = 'https://activity-index-service/activities/5b01c5c92a78f29959236bd6'

        elo = self.cass_graph.competency_objs[
            'http://insertCassUrl/api/data/insertCassSchemaUrl.0.3.Competency/2fef4ebf-a526-4037-b9f4-fe53383db51a']
        self.assertTrue(primer_strategy_1.can_instantiate([elo]))
        self.assertTrue(primer_strategy_2.can_instantiate([elo]))

        row_strategy_1_recommendation = Recommendation(recommendations=[primer_strategy_1.instantiate_row(elo)])
        self.assertTrue(self._activities_in_any_recommendation(row_strategy_1_recommendation, [activity_id]))

        row_strategy_2_recommendation = Recommendation(recommendations=[primer_strategy_2.instantiate_row(elo)])
        self.assertTrue(self._activities_in_any_recommendation(row_strategy_2_recommendation, [activity_id]))

        # When a Recommender is instantiated with those same row strategies (and is set to deduplicate)
        recommender = Recommender(learner=john_superlearner, query_cacher=self._default_query_mock(),
                                  elo_row_strategy_classes=[AffectConfusedOrNew, AffectConfusedOrNew],
                                  activity_row_strategy_classes=[],
                                  cass_graph=self.cass_graph, filter_locked=True, deduplicate_rows=True)

        # And a recommendation is made
        recommender_recommendation = recommender.get_recommendation()

        # Then the activity only appears in one of the returned rows
        self.assertTrue(self._activity_appears_in_exactly_one_row(recommender_recommendation, activity_id))

    def test_deduplication_does_not_remove_non_duplicate_activities(self):
        john_superlearner = self.name_to_learners['John Superlearner']
        john_superlearner = self._clear_user(john_superlearner)

        recommender = Recommender(learner=john_superlearner,
                    query_cacher=self._default_query_mock(),
                    elo_row_strategy_classes=[],
                    activity_row_strategy_classes=[AllActivities],
                    cass_graph=self.cass_graph,
                    filter_locked=True,
                    deduplicate_rows=True)
        recommendation = recommender.get_recommendation()
        self.assertEqual(len(recommendation.recommendations[0].activities), len(filter_assessment_activities(self.all_activities)))

    def test_current_elos(self):
        # Given a user
        learner = self.name_to_learners['John Superlearner']
        # Who starts with nothing
        learner = self._clear_user(learner)
        learner.mastery_estimates = list()

        # Who holds a mastery in the first TLO and all subsequent ELOs
        tlo = self.cass_graph.get_first_top_level_competency()
        for x in range(0, 3):
            elos = self.cass_graph.get_competency_chain(tlo)
            for elo in elos:
                self._master_competency(elo, learner)

            # And holds mastery for the first TLO
            self._master_competency(tlo, learner)
            tlo = self.cass_graph.get_next_neighbor(tlo)

        # Who has a goal for ELO 4.1
        goal_elo = self.cass_graph.get_first_child(tlo)
        goal = Goal(context="context", type="type", competency_id=goal_elo.id)
        learner.goals = [goal]

        # The current TLO should be TLO 4
        self.assertEqual(tlo.ceasncoded_notation, '4')
        current_elo_check = ['4.1.1']

        # Current ELOs are gotten based on the state of mastery of all TLOs and ELOs
        current_elos = get_current_elos(learner, self.cass_graph)

        elo_numbers = [
            elo.ceasncoded_notation for elo in current_elos
        ]

        # The number of current ELOs should match expectations
        self.assertEqual(len(elo_numbers), len(current_elo_check))

        # And the ELOs should match expectations
        self.assertEqual(set(elo_numbers), set(current_elo_check))

    def test_move_to_next_section_strategy_returns_all_assessment_for_current_elo(self):
        # Given a user
        learner = self.name_to_learners['John Superlearner']
        # Who starts with nothing (You know nothing John Superlearner Snow)
        learner = self._clear_user(learner)

        # When the the MoveToNextSection strategy is used
        query_mock = self._default_query_mock()
        move_to_next = MoveToNextSection(learner, query_mock, self.cass_graph, True)

        # Then John is given a recommendation for the assessments of the first ELO
        elo_1_1 = self.cass_graph.competency_objs[
            'http://insertCassUrl/api/data/insertCassSchemaUrl.0.3.Competency/2fef4ebf-a526-4037-b9f4-fe53383db51a']
        rec_row = move_to_next.instantiate_row(elo_1_1)

        self.assertGreater(len(rec_row.activities), 0)

        for recommended_activity in rec_row.activities:
            activity = query_mock.get_activity(mongo_id_from_url(recommended_activity.activity_id))
            self.assertTrue(is_assessment_for_elo(activity, elo_1_1))


    def non_move_to_next_section_strategies_do_not_return_any_assessments(self):
        # Given a user
        learner = self.name_to_learners['John Superlearner']
        # Who starts with nothing (You know nothing John Superlearner Snow)
        learner = self._clear_user(learner)

        # When the the strategy is not MoveToNextSection
        query_mock = self._default_query_mock()
        all_activities = AllActivities(learner, query_mock, self.cass_graph, True)

        # Then John is given a recommendation for the assessments of the first ELO
        elo_1_1 = self.cass_graph.competency_objs[
            'http://insertCassUrl/api/data/insertCassSchemaUrl.0.3.Competency/2fef4ebf-a526-4037-b9f4-fe53383db51a']
        rec_row = all_activities.instantiate_row(elo_1_1, True)

        self.assertGreater(len(rec_row.activities), 0)

        for recommended_activity in rec_row.activities:
            activity = query_mock.get_activity(mongo_id_from_url(recommended_activity.activity_id))
            self.assertFalse(is_assessment_for_elo(activity, elo_1_1))

    # </editor-fold>

    # <editor-fold desc="Test Helpers">

    def _get_learner(self, id: str) -> Learner:
        return self.id_to_learners[id]

    def _get_activity(self, id: str) -> LearningActivity:
        return self.id_to_activity[id]

    def _get_activities(self) -> List[LearningActivity]:
        return self.all_activities

    def _get_learner_tokens(self, id: str) -> LearnerTokens:
        return self.id_to_learner_tokens[id]

    def _update_learner(self, identifier, learner_patch: Learner):
        learner = self.id_to_learners[mongo_id_from_url(identifier)]
        if learner_patch.goals is not None:
            learner.goals = learner_patch.goals
            learner.past_goals = learner_patch.past_goals
        if learner_patch.mastery_estimates is not None:
            learner.past_mastery_estimates = learner_patch.past_mastery_estimates
            learner.mastery_estimates = learner_patch.mastery_estimates

    def _strategy_in_recommendation(self, recommendation: Recommendation, strategy_name: str):
        for recommendation_row in recommendation.recommendations:
            if recommendation_row.name == strategy_name:
                return True

        return False

    def _activities_in_any_recommendation(self, recommendation: Recommendation, recommended_activities: List[str]):
        for recommendation_row in recommendation.recommendations:
            if set([activity.activity_id for activity in recommendation_row.activities]) == set(recommended_activities):
                return True

        return False

    def _activities_in_recommendation(self, recommendation: Recommendation, strategy_name: str,
                                      recommended_activities: List[str]):
        for recommendation_row in recommendation.recommendations:
            if recommendation_row.name == strategy_name:
                return set([activity.activity_id for activity in recommendation_row.activities]) == set(
                    recommended_activities)

        return False

    def _activity_appears_in_exactly_one_row(self, recommendation: Recommendation, activity: str):
        activity_appeared = False
        for recommendation_row in recommendation.recommendations:
            if activity in [recommended_activity.activity_id for recommended_activity in recommendation_row.activities]:
                if activity_appeared: return False
                activity_appeared = True
        return activity_appeared

    def _clear_user(self, learner: Learner):
        learner.mastery_estimates = []
        learner.activity_attempt_counters = []
        learner.mastery_probabilities = []
        learner.past_mastery_estimates = []
        learner.past_goals = []
        learner.competency_attempt_counters = []
        return learner

    def _tlo_held_in_mastery_estimates(self, tlo_id: str, learner: Learner):
        for mastery_estimate in learner.mastery_estimates:
            if mastery_estimate.competency_id == tlo_id:
                if mastery_estimate.mastery == 'held':
                    return True
                return False

        return False

    def _default_assignment_request(self, learner: Learner) -> Recommendation:
        assignment_maker = MandatoryAssignmentMaker(learner, "fake etag", self._default_query_mock(), self.cass_graph)
        return assignment_maker.get_mandatory_assignment()

    def _default_recommender_request(self, learner: Learner, deduplicate=False) -> Recommendation:
        recommender = Recommender(learner=learner,
                                  query_cacher=self._default_query_mock(),
                                  elo_row_strategy_classes=[AffectConfusedOrNew, ReviewActivities,
                                                            AffectBored,
                                                            AffectFrustratedOrBored, PopularActivities,
                                                            HighestRatedActivities, ChallengingActivities,
                                                            IntermediateActivities, IntroductoryActivities],
                                  activity_row_strategy_classes=[],
                                  cass_graph=self.cass_graph,
                                  filter_locked=True,
                                  deduplicate_rows=deduplicate)
        return recommender.get_recommendation()

    def _default_query_mock(self):
        mock_query_cacher = Mock(QueryCacher)
        mock_query_cacher.get_learner.side_effect = self._get_learner
        mock_query_cacher.get_activity.side_effect = self._get_activity
        mock_query_cacher.get_activities.side_effect = self._get_activities
        mock_query_cacher.get_learner_tokens = self._get_learner_tokens
        mock_query_cacher.update_learner = self._update_learner
        mock_query_cacher.get_self_report = lambda: self.id_to_activity["995abcddf3f494selfreport"]
        return mock_query_cacher

    def _make_master_of_tlo(self, learner, tlo):
        self._master_competency(tlo, learner)
        for elo in self.cass_graph.get_competency_chain(tlo):
            self._master_competency(elo, learner)

    def _master_competency(self, competency, learner):
        learner.mastery_estimates.append(MasteryEstimate(context="tla-declarations.jsonld",
                                                         type="MasteryEstimate",
                                                         competency_id=competency.id,
                                                         mastery="held",
                                                         timestamp="2018-10-15T11:25:07"))

    def _add_competency_attempt(self, competency, learner):
        learner.competency_attempt_counters.append(CompetencyAttemptCounter(context="tla-declarations.jsonld",
                                                                            type="CompetencyAttemptCounter",
                                                                            competency_id=competency.id,
                                                                            attempts=1,
                                                                            last_attempt_date_time="2018-10-15T11:25:07"))

    # </editor-fold>


if __name__ == '__main__':
    unittest.main()
