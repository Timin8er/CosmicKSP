"""the configuration manager for the Cosmic KSP project"""
import os
from logging import INFO
from pyqt_data_framework.core import config_manager

config_path = os.path.expanduser(os.path.join('~', 'Documents', 'CosmicKSP', 'CosmicKSP.config'))


default_config = {
    'LOGGING_LEVEL': INFO,
    'OPENC3': {
        'HOST': 'localhost',
        'COMMANDS_PORT': 8091,
        'TELEMETRY_PORT': 8092,
    },
    'TELEMACHUS':{
        'HOST':'localhost',
        'PORT':8085,
        'FREQUENCY':1000,
    },
    'KOS': {
        'HOST':'localhost',
        'PORT':5410,
        'TIMEOUT':10,
    },
}

config = config_manager.get_config(config_path, default_config)
