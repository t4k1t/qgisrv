"""Default settings."""

import logging

settings = {
    'log': {
        'level': "debug",  # log level
    },
    'auth': {
        'required': False,  # set to `True` to enable authentication
        'basic_auth': {
            'path': '/dev/null',  # path to htpasswd file
        },
    },
    'server': {
        'port': 1779,  # port :-P
    },
    'staticpath': '/dev/null',  # path to static files
    'packagepath': '/dev/null',  # path to qgis plugins
}

logging.basicConfig(
    level=getattr(logging, settings['log']['level'].upper()),
)
