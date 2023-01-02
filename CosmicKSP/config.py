import os
from logging import INFO, DEBUG
from pyqt_data_framework.core import config_manager
from CosmicKSP.logging import logger

config_path = os.path.expanduser(os.path.join('~', 'Documents', 'CosmicKSP.config'))

default_config = {
    'LOGGING_LEVEL': INFO,
    'COSMOS': {
        'HOST': 'localhost',
        'TELEMETRY_PORT': 8081,
        'COMMANDS_PORT': 8080,
    },
    'TELEMACHUS':{
        'HOST':'localhost',
        'PORT':8085,
        'FREQUENCY':500,
    },
    'KOS': {
        'HOST':'localhost',
        'PORT':5410,
        'TIMEOUT':10,
    },
    # 'GAME_INSTANCES': [
    #     {
    #         'NAME':'REAL',
    #         'DESCRIPTION':'The game instance representing the "real" world',
    #         'DIR':'',
    #         'GAME_NAME': 'default',
    #         'TELEMACHUS':{
    #             'HOST':'localhost',
    #             'PORT':8085,
    #             'FREQUENCY':500,
    #         },
    #         'KOS': {
    #             'HOST':'localhost',
    #             'PORT':5410,
    #             'TIMEOUT':10,
    #         },
    #     },
    #     {
    #         'NAME':'SIM',
    #         'DESCRIPTION':'The game instance representing a simulation',
    #         'DIR':'',
    #         'GAME_NAME': 'default',
    #         'TELEMACHUS':{
    #             'HOST':'localhost',
    #             'PORT':8086,
    #             'FREQUENCY':500,
    #         },
    #         'KOS': {
    #             'HOST':'localhost',
    #             'PORT':5411,
    #             'TIMEOUT':10,
    #         }
    #     }
    # ]
}

config = config_manager.get_config(config_path, default_config)