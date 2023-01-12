"""package for managing telemetry packets"""
from typing import Dict
import struct

TELEMETRY_SUBSCIPTIONS = [
    'v.missionTime',
    't.universalTime',
    'p.paused',
    'v.altitude',
    'v.lat',
    'v.long',
    'f.abort',
    'f.throttle',
    'b.number',
]

STATE_SIGNAL_LOST = -1
STATE_FLIGHT = 0
STATE_PAUSED = 1
STATE_NO_POWER = 2
STATE_OFF = 3
STATE_NOT_FOUND = 4
STATE_CONSTRUCTION = 5


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
        data.get('p.paused'),
    )


def kos_telemetry_bstring(data: Dict):
    """translate the given kos script data to openc3 string"""
    return struct.pack('>hH',
        3,
        data.get('state'),
    ) + data.get('message')
