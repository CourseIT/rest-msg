#!/usr/bin/env python3
import os

from swagger_server import encoder
from swagger_server.config import app, settings

app.app.json_encoder = encoder.JSONEncoder
specification = os.path.join(os.path.join(os.path.dirname(__file__), 'swagger'), 'swagger.yaml')
app.add_api('specification', arguments={'title': 'Maintenance'})

if __name__ == '__main__':
    app.run(port=settings.APP_PORT)
