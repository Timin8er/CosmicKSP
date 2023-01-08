"""package for managing telemetry packets"""
from typing import Dict, ByteString


def telem_telemechus_to_openc3(d_telem: Dict) -> ByteString:
    """translate the Telemechus telemetry packet to the OpenC3 bytestring"""
    return b''