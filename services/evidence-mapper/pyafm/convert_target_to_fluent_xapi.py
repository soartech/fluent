import json

def convert_statement(target_statement):
    fluent_statement = target_statement
    extensions = fluent_statement['context'].get('extensions', None)
    if extensions is not None:
        competencies = extensions.get('http://www.soartech.com/target/competencies', None)

        del fluent_statement['context']['extensions']['http://www.soartech.com/target/competencies']

        if extensions.get('http://www.soartech.com/target/learnsphere-transaction-id', None):
            del fluent_statement['context']['extensions']['http://www.soartech.com/target/learnsphere-transaction-id']

        ext_tlo_elo = list()
        if competencies is not None:
            for competency in competencies:
                if competency['framework'] == 'Default':
                    ext_tlo_elo.append(competency['competencyId'])
        fluent_statement['context']['extensions']['http://www.soartech.com/fluent/tlos-elos'] = ext_tlo_elo

    return fluent_statement


with open('xapi_statements_filtered_shared.json', 'r') as infile:
    statements = json.load(infile)['1']
    return_statements = [
        convert_statement(statement) for statement in statements
    ]

with open('xapi_statements_fluent.json', 'w') as outfile:
    json.dump(return_statements, outfile)