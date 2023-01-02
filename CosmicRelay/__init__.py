from CosmicKSP.logging import logger
from CosmicKSP.config import config
logger.setLevel(config['LOGGING_LEVEL'])

import sys
import os
from CosmicKSP.core import CommandsUplink, TelemetryDownlink


def main():
    """opens two new terminals and runs the uplink and downlink in each"""
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
        CommandsUplink.run()

    except Exception as e:
        logger.exception('Main Failed')

    logger.info('Commands Uplink Closed')


def down_main():
    """run the telemetry downlink"""
    logger.info('Starting Telemetry Downlink Thread')
    try:
        TelemetryDownlink.telemetry_loop()

    except Exception as e:
        logger.exception('Main Failed')

    logger.info('Relay Downlink Closed')


if __name__ == '__main__':
    main()
