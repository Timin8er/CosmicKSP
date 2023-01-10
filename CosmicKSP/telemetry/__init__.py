"""package for managing telemetry packets"""
from typing import Dict, ByteString
import struct

TELEMETRY_SUBSCIPTIONS = [
    'v.missionTime',
    't.universalTime',
    'p.paused',
    'v.altitude',
    'v.lat',
    'v.long',
    'r.resource[electricity]',
    's.sensor.acc',
    's.sensor.temp',
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


def telem_telemechus_to_openc3(d_telem: Dict) -> ByteString:
    """translate the Telemechus telemetry packet to the OpenC3 bytestring"""
    return b''


def vehicle_telemetry_bstring(data: Dict):
    return struct.pack('>hddffffff',
        1,
        data.get('v.missionTime'),
        data.get('v.altitude'),
        data.get('v.lat'),
        data.get('v.long'),
        data.get('r.resource[electricity]'),
        data.get('s.sensor.acc'),
        data.get('s.sensor.temp'),
        data.get('f.throttle'),
    )


def game_telemetry_bstring(data: Dict):
    return struct.pack('>hh',
        2,
        data.get('p.paused'),
    )


def kos_telemetry_bstring(data: Dict):
    return struct.pack('>hH',
        2,
        data.get('state'),
    ) + data.get('message')
