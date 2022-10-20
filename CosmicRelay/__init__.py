import os
from CosmicKSP import settings
from PyQtDataFramework.Core.Logging import logger
logger.setLevel(settings.LOGGING_LEVEL)

from PyQt5.QtWidgets import QApplication
import sys
import os
from .ui import relayUIMainWindow
from CosmicKSP.core import CommandsUplink, TelemetryDownlink
import time


def main():
    try:
        logger.info('Starting Cosmic Relay')

        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        window = relayUIMainWindow()

        window.show()

        sys.exit(app.exec_())

    except Exception as e:
        logger.exception('Main Failed')


def up_main():
    try:
        logger.info('Starting Commands Uplink')
        app = QApplication(sys.argv)

        thread = CommandsUplink.CommandsRelayThread(settings.REAL_GAME_INSTANCE['KOS'])
        thread.start()

        sys.exit(app.exec_())


    except Exception as e:
        logger.exception('Main Failed')

    logger.info('Commands Uplink Closed')



def down_main():
    try:
        app = QApplication(sys.argv)
        logger.info('Starting Telemetry Downlink Thread')

        TelemetryDownlink.run(settings.REAL_GAME_INSTANCE['TELEMACHUS'])
        # sys.exit(app.exec_())

    except Exception as e:
        logger.exception('Main Failed')

    logger.info('Relay Downlink Closed')


if __name__ == '__main__':
    main()
