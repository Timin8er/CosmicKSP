"""command translation classes"""
from typing import ByteString
import struct

# https://docs.python.org/3/library/struct.html


def cmd_kos_stop(bstr: ByteString) -> ByteString: # pylint: disable=unused-argument
    """returns the stop command for kos"""
    return b'\xf4'


def cmd_stage(bstr: ByteString) -> ByteString: # pylint: disable=unused-argument
    """returns the KOS command to stage the vehicle"""
    return b"stage.\n"


def cmd_set_sas(bstr: ByteString) -> ByteString:
    """return the KOS command to set SAS on or off"""
    args = struct.unpack('>h?', bstr)
    onoff = 'ON' if args[1] else 'OFF'
    return f'SAS {onoff}.\n'.encode()


def cmd_direct_sas(bstr: ByteString) -> ByteString:
    """return the KOS command to set the SAS to a direction"""
    args = struct.unpack('>hB', bstr)
    direction = ["PROGRADE",
        "RETROGRADE",
        "NORMAL",
        "ANTINORMAL",
        "RADIALOUT",
        "RADIALIN",
        "TARGET",
        "ANTITARGET",
        "MANEUVER",
        "STABILITYASSIST",
        "STABILITY"][args[1]]
    return f'set SAS to {direction}.\n'.encode()


def cmd_set_rcs(bstr: ByteString) -> ByteString:
    """return the kos command to turn RCS on or off"""
    args = struct.unpack('>h?', bstr)
    onoff = 'ON' if args[1] else 'OFF'
    return f'RCS {onoff}.\n'.encode()


def cmd_set_lights(bstr: ByteString) -> ByteString:
    """return the kos command to turn LIGNTS on or off"""
    args = struct.unpack('>h?', bstr)
    onoff = 'ON' if args[1] else 'OFF'
    return f'LIGNTS {onoff}.\n'.encode()


def cmd_set_brakes(bstr: ByteString) -> ByteString:
    """return the kos command to turn BRAKES on or off"""
    args = struct.unpack('>h?', bstr)
    onoff = 'ON' if args[1] else 'OFF'
    return f'BRAKES {onoff}.\n'.encode()


def cmd_set_gear(bstr: ByteString) -> ByteString:
    """return the kos command to turn GEAR on or off"""
    args = struct.unpack('>h?', bstr)
    onoff = 'ON' if args[1] else 'OFF'
    return f'GEAR {onoff}.\n'.encode()


def cmd_set_action_group(bstr: ByteString) -> ByteString:
    """return the kos command to turn GEAR on or off"""
    args = struct.unpack('>hB?', bstr)
    onoff = 'ON' if args[2] else 'OFF'
    return f'AG{args[1]} {onoff}.\n'.encode()


def cmd_set_legs(bstr: ByteString) -> ByteString:
    """return the kos command to turn LEGS on or off"""
    args = struct.unpack('>h?', bstr)
    onoff = 'ON' if args[1] else 'OFF'
    return f'LEGS {onoff}.\n'.encode()


def cmd_set_chutes(bstr: ByteString) -> ByteString:
    """return the kos command to turn CHUTES on or off"""
    args = struct.unpack('>h?', bstr)
    onoff = 'ON' if args[1] else 'OFF'
    return f'CHUTES {onoff}.\n'.encode()


def cmd_set_radiators(bstr: ByteString) -> ByteString:
    """return the kos command to turn RADIATORS on or off"""
    args = struct.unpack('>h?', bstr)
    onoff = 'ON' if args[1] else 'OFF'
    return f'RADIATORS {onoff}.\n'.encode()


def cmd_set_ladders(bstr: ByteString) -> ByteString:
    """return the kos command to turn LADDERS on or off"""
    args = struct.unpack('>h?', bstr)
    onoff = 'ON' if args[1] else 'OFF'
    return f'LADDERS {onoff}.\n'.encode()


def cmd_set_bays(bstr: ByteString) -> ByteString:
    """return the kos command to turn BAYS on or off"""
    args = struct.unpack('>h?', bstr)
    onoff = 'ON' if args[1] else 'OFF'
    return f'BAYS {onoff}.\n'.encode()


COMMANDS = {
    struct.pack('>h', 1): cmd_kos_stop,
    struct.pack('>h', 2): cmd_stage,
    struct.pack('>h', 3): cmd_set_sas,
    struct.pack('>h', 4): cmd_direct_sas,
    struct.pack('>h', 5): cmd_set_rcs,
    struct.pack('>h', 6): cmd_set_lights,
    struct.pack('>h', 7): cmd_set_brakes,
    struct.pack('>h', 8): cmd_set_gear,
    struct.pack('>h', 9): cmd_set_action_group,
    struct.pack('>h', 10): cmd_set_legs,
    struct.pack('>h', 11): cmd_set_chutes,
    struct.pack('>h', 12): cmd_set_radiators,
    struct.pack('>h', 13): cmd_set_ladders,
    struct.pack('>h', 14): cmd_set_bays,
}
