#!/usr/bin/env python3

import connexion

from activity_index_server import encoder

app = connexion.App(__name__, specification_dir='./swagger/')
app.app.json_encoder = encoder.JSONEncoder
app.add_api('swagger.yaml', arguments={'title': 'Asset API'})

if __name__ == '__main__':
    app.run(port=8989)
