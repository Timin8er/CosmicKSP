"""connection manager for kos"""
from time import sleep, time
from typing import ByteString, Dict
import struct

def kos_status_telemetry(data: Dict) -> ByteString:
    """translate the given vehivcle telemachus data to openc3 string"""
    return struct.pack('>hHH',
        4,
        data.get('state', 0),
        data.get('cpu_id', 0)
    ) \
        + data.get('cpu_name',       'None').ljust(32)[:32].encode('utf-8')\
        + data.get('vessel_name',    'None').ljust(32)[:32].encode('utf-8')\
        + data.get('running_script', 'None').ljust(32)[:32].encode('utf-8')\
        + data.get('message',        'None').encode('utf-8')
