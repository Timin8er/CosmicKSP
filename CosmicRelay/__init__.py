from PyQtDataFramework.Core.Logging import logger
from CosmicKSP.Config import config, game_instance
logger.setLevel(config['LOGGING_LEVEL'])

from PyQt5.QtWidgets import QApplication
import sys
import os
from .ui import relayUIMainWindow
from CosmicKSP.core import CommandsUplink, TelemetryDownlink
import time


def main():
    """opens two new terminals and ruuns the uplink and downlink in each"""
    if sys.platform == "win32":
        os.system('start cmd.exe /K CosmicRelayDownlink"')
        os.system('start cmd.exe /K CosmicRelayUplink"')

    else:
        os.system('gnome-terminal --tab --title=TelemachusRelayDownlink -- CosmicRelayDownlink')
        os.system('gnome-terminal --tab --title=TelemachusRelayUplink -- CosmicRelayUplink')


def up_main():
    """run the commands uplink"""
    logger.info('Starting Commands Uplink')
    try:
        CommandsUplink.run(game_instance['KOS'])

    except Exception as e:
        logger.exception('Main Failed')

    logger.info('Commands Uplink Closed')


def down_main():
    """run the telemetry downlink"""
    logger.info('Starting Telemetry Downlink Thread')
    try:
        TelemetryDownlink.run(game_instance['TELEMACHUS'])

    except Exception as e:
        logger.exception('Main Failed')

    logger.info('Relay Downlink Closed')


if __name__ == '__main__':
    main()
