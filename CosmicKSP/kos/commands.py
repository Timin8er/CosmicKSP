"""command translation classes"""
from typing import ByteString, Dict
import struct
from CosmicKSP.config import config

# https://docs.python.org/3/library/struct.html


def cmd_abort(*_) -> ByteString:
    """returns the stop command for kos"""
    return b'SET ABORT TO TRUE.\n'


def cmd_kos_stop(*_) -> ByteString:
    """returns the stop command for kos"""
    return b'\xf4'


def cmd_stage(*_) -> ByteString:
    """returns the KOS command to stage the vehicle"""
    return b"stage.\n"


def cmd_set_system(bstr: ByteString) -> ByteString:
    """return the KOS command to set SAS on or off"""
    args = struct.unpack('>hH?', bstr)

    system = [
        'SAS',
        'RCS',
        'LIGHTS',
        'BREAKS',
        'GEAR',
        'LEGS',
        'CHUTES',
        'RADIATORS',
        'LADDERS',
        'BAYS',
    ][args[1]]

    onoff = 'ON' if args[2] else 'OFF'
    return f'{system} {onoff}.\n'.encode()


def cmd_set_action_group(bstr: ByteString) -> ByteString:
    """return the kos command to turn GEAR on or off"""
    args = struct.unpack('>hB?', bstr)
    onoff = 'ON' if args[2] else 'OFF'
    return f'AG{args[1]} {onoff}.\n'.encode()


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


def cmd_import_script(bstr: ByteString) -> ByteString: 
    """return the kos command for to copy a script to the 'internal' kos volumn """
    # args = struct.unpack('>h', bstr)
    rest = bstr.removeprefix(struct.pack('>h', 101)).decode('utf-8')
    return f'copypath("0:/{rest}.ks", "1:/{rest}.ks").\n'.encode()


# def cmd_launch_target_ap(bstr: ByteString) -> ByteString:
#     """return the kos command for the launch_target_ap.ks """
#     length = struct.calcsize('>hIffffff')
#     args = struct.unpack('>hIffffff', bstr[:length])
#     main_args = ', '.join([str(i) for i in args[1:]])
#     stage_args = bstr[length:].decode('utf-8')
#     return f'runpath("1:/launch_target_ap.ks", {main_args}, list({stage_args})).\n'.encode()


# def cmd_create_node_circularise_at_apoapsis(bstr: ByteString) -> ByteString: # pylint: disable=unused-argument
#     """return the kos command for to copy a script to the 'internal' kos volumn """
#     return b'runpath("0:/create_node_circularise_at_apoapsis.ks").\n'


# def cmd_execute_next_manuever_node(*_) -> ByteString:
#     """return the kos command for to copy a script to the 'internal' kos volumn """
#     return 'runpath("0:/execute_next_manuever_node.ks").\n'.encode()


def cmd_script(name: str, script_config: Dict):
    """returns the translation function for a kos script crom the config file"""
    # the id that the translator will look up this function by
    id_str = struct.pack(script_config['struct'][0:2], script_config['id'])

    # simple version has no trailing string argument
    if not script_config['struct'].endswith('p'):

        def _cmd_script(bstr: ByteString) -> ByteString:
            args = struct.unpack(script_config['struct'], bstr)
            args_str = ', '.join([str(i) for i in args[1:]])
            return f'runpath("1:/{name}.ks", {args_str}).\n'.encode('utf-8')

        return id_str, _cmd_script

    short_struct = script_config['struct'][0:-2]
    length = struct.calcsize(short_struct)

    def _cmd_script(bstr: ByteString) -> ByteString:
        args = struct.unpack(short_struct, bstr[:length])
        string_arg = bstr[length:].decode('utf-8')
        args_str = ', '.join([str(i) for i in args[1:]] + [string_arg])
        return f'runpath("1:/{name}.ks", {args_str}).\n'.encode()

    return id_str, _cmd_script


COMMANDS = {
    struct.pack('>h', 1): cmd_kos_stop,
    struct.pack('>h', 2): cmd_kos_stop,
    struct.pack('>h', 3): cmd_stage,
    struct.pack('>h', 4): cmd_set_system,
    struct.pack('>h', 5): cmd_set_action_group,
    struct.pack('>h', 6): cmd_direct_sas,
    struct.pack('>h', 7): cmd_import_script,
}


# for each kos script in the config file, add it to the list of commands
for name, scritp_config in config.scripts.items():
    cmd_id, funk = cmd_script(name, scritp_config)
    COMMANDS[id] = funk
