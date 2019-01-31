#!/usr/bin/env python3

from swagger_server import config, encoder

config.app.app.json_encoder = encoder.JSONEncoder
config.app.add_api('swagger.yaml', arguments={'title': 'Maintenance'})

if __name__ == '__main__':
    config.app.run(port=config.settings.APP_PORT)
