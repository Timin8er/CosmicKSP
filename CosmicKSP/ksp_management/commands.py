"""contains commands for controlling ksp"""
from typing import ByteString
import time
import struct
import os
import re
import shutil
import keyboard
from CosmicKSP.config import config


VESSTLE_PATTERN = r"VESSEL\n\t*\{\n\t*pid = .+\n\t*persistentId = .+\n\t*name = .+\n"
SAVES_DIR = os.path.join(config['ksp']['dir'], 'saves', config['ksp']['save'])


def quicksave(name: str = None) -> None:
    """press the f5 key to create a quicksave"""
    keyboard.press_and_release('f5')

    if name:
        shutil.copy(
            os.path.join(SAVES_DIR, 'quicksave.sfs'),
            os.path.join(SAVES_DIR, f'{name}_quicksave.sfs')
            )
        shutil.copy(
            os.path.join(SAVES_DIR, 'quicksave.loadmeta'),
            os.path.join(SAVES_DIR, f'{name}_quicksave.loadmeta')
            )



def quickload(name: str = None) -> None:
    """press the f9 key to load the quicksave"""
    if name:
        shutil.copy(
            os.path.join(SAVES_DIR, f'{name}_quicksave.sfs'),
            os.path.join(SAVES_DIR, 'quicksave.sfs')
            )
        shutil.copy(
            os.path.join(SAVES_DIR, f'{name}_quicksave.loadmeta'),
            os.path.join(SAVES_DIR, 'quicksave.loadmeta')
            )

    keyboard.press('f9')
    time.sleep(2)
    keyboard.release('f9')


def cmd_quicksave(bstr: ByteString) -> str:
    """press the f5 key to create a quicksave"""
    print('quicksave')
    name = bstr[2:].decode('utf-8').strip()
    quicksave(name)
    return ''


def cmd_quickload(bstr: ByteString) -> str:
    """press the f9 key to load the quicksave"""
    print('quickload')
    name = bstr[2:].decode('utf-8')
    quickload(name)
    return ''


def cmd_switch_to_vesstle(bstr: ByteString) -> str:
    """set the current vessle in a quicksave"""
    # create the quicksave file
    quicksave()
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
    quickload()
    return ""



COMMANDS = {
    struct.pack('>h', 3): cmd_quicksave,
    struct.pack('>h', 4): cmd_quickload,
    struct.pack('>h', 5): cmd_switch_to_vesstle,
}
