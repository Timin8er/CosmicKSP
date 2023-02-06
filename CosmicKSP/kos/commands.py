"""command translation classes"""
from typing import ByteString, Dict
import struct
from CosmicKSP.config import config


def cmd_abort(*_) -> ByteString:
    """returns the stop command for kos"""
    return 'ABORT ON.\n'


def cmd_kos_stop(*_) -> ByteString:
    """returns the stop command for kos"""
    return '\xf4'


def cmd_generic(bstr: ByteString) -> ByteString:
    """extract and return the command within"""
    return bstr[2:].decode('utf-8')


def cmd_attach_cpu(bstr: ByteString) -> ByteString:
    """return ctrl+d command to reattach to a cpu"""
    args = struct.unpack('>hH', bstr)
    # return ('\u0004\n', f'{args[1]}\n')
    return f'{args[1]}\n'


def cmd_stage(*_) -> ByteString:
    """returns the KOS command to stage the vehicle"""
    return "stage.\n"


def cmd_set_system_power(bstr: ByteString) -> ByteString:
    """return the KOS command to set SAS on or off"""
    args = struct.unpack('>hH?', bstr)

    system = [
        'SAS',
        'RCS',
        'LIGHTS',
        'BRAKES',
        'GEAR',
        'LEGS',
        'CHUTES',
        'RADIATORS',
        'LADDERS',
        'BAYS',
    ][args[1]]

    onoff = 'ON' if args[2] else 'OFF'
    return f'{system} {onoff}.\n'


def cmd_set_action_group(bstr: ByteString) -> ByteString:
    """return the kos command to turn GEAR on or off"""
    args = struct.unpack('>hB?', bstr)
    onoff = 'ON' if args[2] else 'OFF'
    return f'AG{args[1]} {onoff}.\n'


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
    return f'set SASMODE to "{direction}".\n'


def cmd_import_script(bstr: ByteString) -> ByteString:
    """return the kos command for to copy a script to the 'internal' kos volumn """
    script_name = bstr[2:].decode('utf-8')

    if script_name not in config['scripts']:
        return _cmd_import(script_name)

    scripts = [script_name] + config['scripts'][script_name]['dependancies']

    return (' '.join([_cmd_import(i) for i in scripts]))


def _cmd_import(script_name: str) -> str:
    return f'copypath("0:/{script_name}.ks", "1:/{script_name}.ks").\n'


def cmd_script(script_name: str, script_config: Dict):
    """returns the translation function for a kos script crom the config file"""
    # the id that the translator will look up this function by
    id_str = struct.pack(script_config['struct'][0:2], script_config['id'])

    if len(script_config['struct']) <= 2:
        def _cmd_script(*_) -> ByteString:
            return f'runpath("1:/{script_name}.ks").\n'
        return id_str, _cmd_script

    # simple version has no trailing string argument
    if not script_config['struct'].endswith('p'):

        def _cmd_script(bstr: ByteString) -> ByteString:
            args = struct.unpack(script_config['struct'], bstr)
            args_str = ', '.join([str(i) for i in args[1:]])
            return f'runpath("1:/{script_name}.ks", {args_str}).\n'

        return id_str, _cmd_script

    short_struct = script_config['struct'][0:-1]
    length = struct.calcsize(short_struct)

    def _cmd_script(bstr: ByteString) -> ByteString:
        args = struct.unpack(short_struct, bstr[:length])
        string_arg = bstr[length:].decode('utf-8')
        args_str = ', '.join([str(i) for i in args[1:]] + [string_arg])
        return f'runpath("1:/{script_name}.ks", {args_str}).\n'

    return id_str, _cmd_script


COMMANDS = {
    struct.pack('>h', 100): cmd_attach_cpu,
    struct.pack('>h', 101): cmd_kos_stop,
    struct.pack('>h', 102): cmd_generic,
    struct.pack('>h', 103): cmd_abort,
    struct.pack('>h', 104): cmd_stage,
    struct.pack('>h', 105): cmd_set_system_power,
    struct.pack('>h', 106): cmd_set_action_group,
    struct.pack('>h', 107): cmd_direct_sas,
    struct.pack('>h', 200): cmd_import_script,
}

# for each kos script in the config file, add it to the list of commands
for name, scritp_config in config['scripts'].items():
    cmd_id, funk = cmd_script(name, scritp_config)
    COMMANDS[cmd_id] = funk
