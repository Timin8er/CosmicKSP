"""the telemetry traslation layer between Telemechus and OpenC3"""
import datetime
from PyQt5.QtCore import QThread, pyqtSignal
from CosmicKSP.logging import logger
from CosmicKSP.telemachus_links import TelemachusSocket
from CosmicKSP.telemetry import *


STATE_STRINGS = {
    STATE_SIGNAL_LOST: 'Signal Lost',
    STATE_FLIGHT: 'Flight',
    STATE_PAUSED: 'Paused',
    STATE_NO_POWER: 'No Power',
    STATE_OFF: 'Off',
    STATE_NOT_FOUND: 'Not Found',
    STATE_CONSTRUCTION: 'Construction',
}


class TelemetryRelayThread(QThread):
    """QThread loops through telemetry"""

    telemReport = pyqtSignal(dict)
    signalStatus = pyqtSignal(int)

    def run(self):
        """run thread"""
        telemetry_loop()


def telemetry_loop():
    """loop of recieving telemetry"""
    logger.info('Telemetry Relay Starting')
    game_state = -1

    data_link = TelemachusSocket()

    try:
        while True:
            if data_link.web_socket is None:
                data_link.reconnect()

            else:
                telemetry_data = data_link.listen() # get telem data
                if not telemetry_data:
                    continue

                if telemetry_data.get('p.paused') != game_state:
                    game_state = telemetry_data.get('p.paused')
                    log_state(telemetry_data)

                # log telemetry if not construction or paused
                if game_state == STATE_FLIGHT:
                    log_telemetry(telemetry_data)

    except KeyboardInterrupt:
        logger.info('Telemetry Relay Stopped: Keyboard Interupt')


def log_state(data):
    """log the connection state"""
    mission_time = datetime.timedelta(seconds=data.get('v.missionTime', 0))
    game_state = STATE_STRINGS[data['p.paused']]
    logger.info('T+%s Game State: %s', mission_time, game_state)


def log_telemetry(data):
    """log the telemetry data"""
    mission_time = datetime.timedelta(seconds=data.get('v.missionTime', 0))
    logger.info('T+%s Altitude: %s', mission_time, data.get('v.altitude'))


if __name__ == '__main__':
    telemetry_loop()
