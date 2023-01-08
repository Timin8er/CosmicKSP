"""package for managing telemetry packets"""
from typing import Dict, ByteString

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