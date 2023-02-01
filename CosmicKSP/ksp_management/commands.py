"""contains commands for controlling ksp"""
from typing import ByteString
import time
import struct
import os
import re
import keyboard
from CosmicKSP.config import config


VESSTLE_PATTERN = r"VESSEL\n\t*\{\n\t*pid = .+\n\t*persistentId = .+\n\t*name = .+\n"


def cmd_quicksave(bstr: ByteString) -> str:
    """press the f5 key to create a quicksave"""
    keyboard.press_and_release('f5')
    return ''


def cmd_quickload(bstr: ByteString) -> str:
    """press the f9 key to load the quicksave"""
    keyboard.press('f9')
    time.sleep(2)
    keyboard.release('f9')
    return ''


def cmd_switch_to_vesstle(bstr: ByteString) -> str:
    """set the current vessle in a quicksave"""
    # create the quicksave file
    cmd_quicksave(bstr)
    time.sleep(0.5) # sleep due to asyncronus nature file creation

    # the quicksave file
    qs_file = os.path.join(config['ksp']['dir'], 'saves', config['ksp']['save'], 'quicksave.sfs')
    # the string we're looking for the quicksave file
    vesstle_name_line = f"name = {bstr[2:].decode('utf-8')}"

    # check the quicksave for the active vestle
    with open(qs_file, 'r', encoding='utf-8') as file:
        qs_content = file.read()
        # check if string present or not
        if vesstle_name_line not in qs_content:
            return ""

    # fin the index of the new current vessel and set the active vessel key
    for i, match in enumerate(re.findall(VESSTLE_PATTERN, qs_content)):
        if vesstle_name_line in match:
            qs_content = re.sub(r'activeVessel = [0-9]+', f'activeVessel = {i}', qs_content, 1)
            break

    # write new quicksave content to file
    with open(qs_file, 'w', encoding='utf-8') as file:
        file.write(qs_content)

    # load the quicksave
    cmd_quickload(bstr)
    return ""



COMMANDS = {
    struct.pack('>h', 8): cmd_quicksave,
    struct.pack('>h', 9): cmd_quickload,
    struct.pack('>h', 10): cmd_switch_to_vesstle,
}
