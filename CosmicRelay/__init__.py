from CosmicKSP.logging import logger
from CosmicKSP.config import config
logger.setLevel(config['LOGGING_LEVEL'])

import sys
import os
from CosmicRelay.telemetry_down import telemetry_loop
from CosmicRelay.commands_up import commands_loop


def main():
    """opens two new terminals and runs the uplink and downlink in each"""
    if sys.platform == "win32":
        os.system('start cmd.exe /K CosmicRelayDownlink"')
        os.system('start cmd.exe /K CosmicRelayUplink"')

    else:
        os.system('gnome-terminal --tab --title=TelemachusRelayDownlink -- CosmicRelayDownlink')
        os.system('gnome-terminal --tab --title=TelemachusRelayUplink -- CosmicRelayUplink')


def up_main():
    """run the commands uplink relay"""
    try:
        commands_loop()

    except Exception as e:
        logger.exception('Main Failed')


def down_main():
    """run the telemetry downlink relay"""
    try:
        telemetry_loop()

    except Exception as e:
        logger.exception('Main Failed')


if __name__ == '__main__':
    main()
