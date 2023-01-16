"""the telemetry traslation layer between Telemechus and OpenC3"""
import datetime
from CosmicKSP.logging import get_logger
from CosmicKSP.config import config
from CosmicKSP.telemachus.telemachus import TelemachusConnector
from CosmicKSP.telemachus.telemetry import *
from CosmicKSP.openc3 import OpenC3Connection


STATE_STRINGS = {
    STATE_SIGNAL_LOST: 'Signal Lost',
    STATE_FLIGHT: 'Flight',
    STATE_PAUSED: 'Paused',
    STATE_NO_POWER: 'No Power',
    STATE_OFF: 'Off',
    STATE_NOT_FOUND: 'Not Found',
    STATE_CONSTRUCTION: 'Construction',
}


openc3_connection = OpenC3Connection(config['OPENC3']['HOST'], config['OPENC3']['TELEMETRY_PORT'])
telemachus_link = TelemachusConnector(config['TELEMACHUS']['HOST'], config['TELEMACHUS']['PORT'], config['TELEMACHUS']['FREQUENCY'])


logger = get_logger(name='CosmicKSP_Telemetry')
logger.setLevel(config['LOGGING_LEVEL'])


def telemetry_loop():
    """loop of recieving telemetry from Telemachus, translating it, and sending it to OpenC3"""
    logger.info('Telemetry Relay Starting')
    game_state = -1

    try:
        while True:
            if telemachus_link.web_socket is None:
                telemachus_link.reconnect()
                continue

            telemetry_data = telemachus_link.get_telemetry() # get telem data
            if not telemetry_data:
                continue

            if telemetry_data.get('p.paused') != game_state:
                game_state = telemetry_data.get('p.paused')
                telem = game_telemetry_bstring(telemetry_data)
                openc3_connection.send(telem)
                log_state(telemetry_data)

            # log telemetry if not construction or paused
            if game_state == STATE_FLIGHT:
                telem = vehicle_telemetry_bstring(telemetry_data)
                openc3_connection.send(telem)
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


def main():
    """run the telemetry downlink relay"""
    try:
        telemetry_loop()

    except Exception:
        logger.exception('Main Failed')


if __name__ == '__main__':
    main()
