"""the telemetry traslation layer between Telemechus and OpenC3"""
import datetime
from CosmicKSP.logging import get_logger
from CosmicKSP.config import config
from CosmicKSP.telemachus import TelemachusConnector
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

logger = get_logger(name='CosmicKSP_Telemetry')
logger.setLevel(config['logging_level'])


def telemetry_loop():
    """loop of recieving telemetry from Telemachus, translating it, and sending it to OpenC3"""
    openc3_connection = OpenC3Connection(
        config['openc3']['host'],
        config['openc3']['telemetry_port'])

    telemachus_link_vehicle = TelemachusConnector(
        config['telemachus']['host'],
        config['telemachus']['port'],
        config['telemachus']['frequency'])

    for sub in VEHICLE_TELEMETRY_SUBSCIPTIONS:
        telemachus_link_vehicle.subscribe(sub)

    logger.info('Telemetry Relay Starting')

    while True:
        if telemachus_link_vehicle.web_socket is None:
            telemachus_link_vehicle.reconnect()
            continue

        telemetry_data = telemachus_link_vehicle.recieve() # get telem data
        if not telemetry_data:
            continue

        telem = game_telemetry_bstring(telemetry_data)
        openc3_connection.send(telem)
        log_telemetry(telemetry_data)

        # if telemetry_data.get('p.paused') != game_state:
        #     game_state = telemetry_data.get('p.paused')
        #     telem = game_telemetry_bstring(telemetry_data)
        #     openc3_connection.send(telem)
        #     log_state(telemetry_data)

        # # log telemetry if not construction or paused
        # if game_state == STATE_FLIGHT:
        #     telem = vehicle_telemetry_bstring(telemetry_data)
        #     openc3_connection.send(telem)
        #     log_telemetry(telemetry_data)


def log_state(data):
    """log the connection state"""
    mission_time = datetime.timedelta(seconds=data.get('v.missionTime', 0))
    game_state = STATE_STRINGS[data['p.paused']]
    logger.info('T+%s Game State: %s', mission_time, game_state)


def log_telemetry(data):
    """log the telemetry data"""
    mission_time = datetime.timedelta(seconds=data.get('v.missionTime', 0))
    logger.info('T+%s', mission_time)


def main():
    """run the telemetry downlink relay"""
    try:
        telemetry_loop()

    except Exception:
        logger.exception('Main Failed')


if __name__ == '__main__':
    main()
