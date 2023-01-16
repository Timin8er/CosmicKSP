"""package for managing telemetry packets"""
from typing import Dict
import struct

STATE_SIGNAL_LOST = -1
STATE_FLIGHT = 0
STATE_PAUSED = 1
STATE_NO_POWER = 2
STATE_OFF = 3
STATE_NOT_FOUND = 4
STATE_CONSTRUCTION = 5


VEHICLE_TELEMETRY_SUBSCIPTIONS = [
    'v.missionTime',
    'v.geeForce',
    'f.throttle',
    'v.sasValue',
    'v.rcsValue',
    'v.lightValue',
    'v.brakeValue',
    'v.gearValue',
    'v.atmosphericDensity',
    'v.dynamicPressure',
    'v.name',
]


ORBIT_TELEMETRY_SUBSCIPTIONS = [
    't.universalTime',
    'v.altitude',
    'v.lat',
    'v.long',
    'o.ApA',
    'o.PeA',
    'o.sma',
    'o.timeToAp',
    'o.timeToPe',
    'o.inclination',
    'o.eccentricity',
    'o.epoch',
    'o.period',
    'o.argumentOfPeriapsis',
    'o.timeToTransition1'
    'o.lan',
    'o.maae',
    'b.name',
]


def vehicle_telemetry_bstring(data: Dict):
    """translate the given vehivcle telemachus data to openc3 string"""
    return struct.pack('>hddfff',
        1,
        data.get('v.missionTime', 0.0),
        data.get('v.altitude', 0.0),
        data.get('v.lat', 0.0),
        data.get('v.long', 0.0),
        data.get('f.throttle', -1.0),
    )


def game_telemetry_bstring(data: Dict):
    """translate the given game state telemachus data to openc3 string"""
    return struct.pack('>hh',
        2,
        data.get('p.paused', STATE_SIGNAL_LOST),
    )


def kos_telemetry_bstring(data: Dict):
    """translate the given kos script data to openc3 string"""
    return struct.pack('>hH',
        3,
        data.get('state', STATE_SIGNAL_LOST),
    ) + data.get('message', '')
