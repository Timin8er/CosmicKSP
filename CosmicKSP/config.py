"""the configuration manager for the Cosmic KSP project"""
from typing import Dict
import os
from logging import INFO
import yaml


def get_config(filepath: str, default_values: Dict) -> Dict:
    """get the config data for the given file"""
    if not os.path.isfile(filepath):
        create_config_file(filepath, default_values)

    with open(filepath, 'r', encoding="utf-8") as file:
        return yaml.safe_load(file)


def create_config_file(filepath: str, default_values: Dict) -> None:
    """create a config file with the given default values"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, 'w', encoding="utf-8") as file:
        yaml.dump(default_values, file)


config_path = os.path.expanduser(os.path.join('~', 'Documents', 'CosmicKSP', 'CosmicKSP.config'))

default_config = {
    'logging_level': INFO,
    'openc3': {
        'host': 'localhost',
        'commands_port': 8091,
        'telemetry_port': 8092,
    },
    'telemachus':{
        'host':'localhost',
        'port':8085,
        'frequency':1000,
    },
    'kos': {
        'host':'localhost',
        'port':5410,
        'timeout':10,
    },
    'scripts':{
        'launch_target_ap': {
            'id': 201,
            'struct': '>hIffffffp',
            'dependancies': [
                'dual_stage_delay',
                'create_node_circularise_at_apoapsis',
                'execute_next_manuever_node',
            ],
        },
        'create_node_circularise_at_apoapsis': {
            'id': 202,
            'struct': '>h',
            'dependancies': [],
        },
        'execute_next_manuever_node': {
            'id': 203,
            'struct': '>hp',
            'dependancies': [],
        },
    },
    'ksp':{
        'dir': 'C:\\Steam\\steamapps\\common\\Kerbal Space Program',
        'save': 'default',
    }
}

config = get_config(config_path, default_config)
