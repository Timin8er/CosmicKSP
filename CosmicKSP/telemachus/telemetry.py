"""package for managing telemetry packets"""
from typing import Dict, ByteString
import struct
from CosmicKSP.telemachus import STATE_SIGNAL_LOST

VEHICLE_TELEMETRY_SUBSCIPTIONS = [
    'p.paused',
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
    'p.paused',
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
    'v.body',
]


def vehicle_telemetry_bstring(data: Dict) -> ByteString:
    """translate the given vehivcle telemachus data to openc3 string"""
    return struct.pack('>hdffbbbbbff',
        1,
        data.get('v.missionTime', 0.0),
        data.get('v.geeForce', 0.0),
        data.get('f.throttle', -1.0),
        data.get('v.sasValue', -1),
        data.get('v.rcsValue', -1),
        data.get('v.lightValue', -1),
        data.get('v.brakeValue', -1),
        data.get('v.gearValue', -1),
        data.get('v.atmosphericDensity', 0.0),
        data.get('v.dynamicPressure', 0.0),
    ) + data.get('v.name', 'None').encode('utf-8')


def orbit_telemetry_bstring(data: Dict) -> ByteString:
    """translate the telemetry pachet for orbit imformation"""
    return struct.pack('>hddffdddddfffdfdff',
        2,
        data.get('t.universalTime', 0.0),
        data.get('v.altitude', 0.0),
        data.get('v.lat', 0.0),
        data.get('v.long', 0.0),
        data.get('o.ApA', 0.0),
        data.get('o.PeA', 0.0),
        data.get('o.sma', 0.0),
        data.get('o.timeToAp', 0.0),
        data.get('o.timeToPe', 0.0),
        data.get('o.inclination', 0.0),
        data.get('o.eccentricity', 0.0),
        data.get('o.epoch', 0.0),
        data.get('o.period', 0.0),
        data.get('o.argumentOfPeriapsis', 0.0),
        data.get('o.timeToTransition1', 0.0),
        data.get('o.lan', 0.0),
        data.get('o.maae', 0.0),
    ) + data.get('v.body', 'None').encode('utf-8')


def game_telemetry_bstring(data: Dict):
    """translate the given game state telemachus data to openc3 string"""
    return struct.pack('>hh',
        3,
        data.get('p.paused', STATE_SIGNAL_LOST),
    )


def kos_telemetry_bstring(data: Dict):
    """translate the given kos script data to openc3 string"""
    return struct.pack('>hH',
        4,
        data.get('state', STATE_SIGNAL_LOST),
    ) + data.get('message', '')
