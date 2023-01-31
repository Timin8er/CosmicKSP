"""contains commands for controlling ksp"""
from typing import ByteString
import time
import struct
import keyboard


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


COMMANDS = {
    struct.pack('>h', 8): cmd_quicksave,
    struct.pack('>h', 9): cmd_quickload,
}