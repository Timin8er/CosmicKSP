"""the telemetry traslation layer between Telemechus and OpenC3"""
import datetime
from typing import Dict
from PyQt5.QtCore import QThread, pyqtSignal
from CosmicKSP.logging import logger
from CosmicKSP.telemachus_links import TelemachusSocket
from CosmicKSP.telemetry import *


class TelemetryRelayThread(QThread):
    """QThread loops through telemetry"""

    telemReport = pyqtSignal(dict)
    signalStatus = pyqtSignal(int)

    def run(self):
        telemetry_loop()


def telemetry_loop():
    """loop of recieving telemetry"""
    logger.info('Telemetry Relay Starting')
    game_state = -1

    data_link = TelemachusSocket()

    while True:
        try:
            telemetry_data = data_link.update() # get telem data

            if data_link.game_state != game_state:
                log_state(game_state)

            if not telemetry_data:
                continue

            if data_link.game_state != 5: # not construction
                log_telemetry(telemetry_data)

        except KeyboardInterrupt:
            logger.info('Telemetry Relay Stopped: Keyboard Interupt')
            break


def log_state(state):
    """log the connection state"""
    if state == STATE_SIGNAL_LOST:
        logger.info('Status: Signal Lost')

    elif state == STATE_FLIGHT:
        logger.info('Status: Flight')

    elif state == STATE_PAUSED:
        logger.info('Status: Paused')

    elif state == STATE_NO_POWER:
        logger.info('Status: No Power')

    elif state == STATE_OFF:
        logger.info('Status: Off')

    elif state == STATE_NOT_FOUND:
        logger.info('Status: not found')

    elif state == STATE_CONSTRUCTION:
        logger.info('Status: Construction')


def log_telemetry(data):
    """log the telemetry data"""
    mission_time = datetime.timedelta(seconds=data.get('v.missionTime', 0))
    logger.info('Telem Recieved T+%s', mission_time)


if __name__ == '__main__':
    telemetry_loop()