from PyQtDataFramework.Core.Logging import logger
from PyQtDataFramework.Core import ConfigManager
import sys, os
import logging

config_path = os.path.expanduser(os.path.join('~', 'Documents', 'CosmicKSP.config'))

config = {
    'LOGGING_LEVEL': logging.INFO,

    'COSMOS': {
        'HOST': 'cosmos.timin8er.com',
        'PORT': 1248,
    },
    'GAME_INSTANCES': [
        {
            'NAME':'REAL',
            'DESCRIPTION':'The game instance representing the "real" world',
            'DIR':r'C:\KSP\CosmicKSP',
            'GAME_NAME': 'default',
            'TELEMACHUS':{
                'HOST':'127.0.0.1',
                'PORT':8085,
                'FREQUENCY':500,
            },
            'KOS': {
                'HOST':'127.0.0.1',
                'PORT':5410,
                'TIMEOUT':10,
            },
        },
        {
            'NAME':'SIM',
            'DESCRIPTION':'The game instance representing a simulation',
            'DIR':r'C:\KSP\CosmicKSP_Sim',
            'GAME_NAME': 'default',
            'TELEMACHUS':{
                'HOST':'127.0.0.1',
                'PORT':8086,
                'FREQUENCY':500,
            },
            'KOS': {
                'HOST':'127.0.0.1',
                'PORT':5411,
                'TIMEOUT':10,
            }
        }
    ]
}

config = ConfigManager.getConfig(config_path, config)

game_instance = config['GAME_INSTANCES'][0]
