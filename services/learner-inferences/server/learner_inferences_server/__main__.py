#!/usr/bin/env python3

import connexion

from learner_inferences_server import encoder

app = connexion.App(__name__, specification_dir='./swagger/')
app.app.json_encoder = encoder.JSONEncoder
app.add_api('swagger.yaml', arguments={'title': 'Learner API'})

if __name__ == '__main__':
    app.run(port=8999)
