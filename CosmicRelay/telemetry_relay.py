"""the telemetry traslation layer between Telemechus and OpenC3"""
import datetime
import threading
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

stop_event = threading.Event()

def vehicle_telemetry_loop():
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

    logger.info('Vehicle Telemetry Starting')

    while True:
        if stop_event.is_set():
            break

        if telemachus_link_vehicle.web_socket is None:
            telemachus_link_vehicle.reconnect()
            continue

        telemetry_data = telemachus_link_vehicle.recieve() # get telem data
        if not telemetry_data:
            continue

        if telemetry_data['p.paused'] != STATE_FLIGHT:
            continue

        telem = vehicle_telemetry_bstring(telemetry_data)
        openc3_connection.send(telem)

        mission_time = datetime.timedelta(seconds=telemetry_data.get('v.missionTime', 0))
        logger.info('T+%s Vehicle: %s', mission_time, telemetry_data.get('v.name', 'None'))


def orbit_telemetry_loop():
    """loop of recieving telemetry from Telemachus, translating it, and sending it to OpenC3"""
    openc3_connection = OpenC3Connection(
        config['openc3']['host'],
        config['openc3']['telemetry_port'])

    telemachus_link_vehicle = TelemachusConnector(
        config['telemachus']['host'],
        config['telemachus']['port'],
        10_000)

    for sub in ORBIT_TELEMETRY_SUBSCIPTIONS:
        telemachus_link_vehicle.subscribe(sub)

    logger.info('Orbit Telemetry Starting')

    while True:
        if stop_event.is_set():
            break

        if telemachus_link_vehicle.web_socket is None:
            telemachus_link_vehicle.reconnect()
            continue

        telemetry_data = telemachus_link_vehicle.recieve() # get telem data
        if not telemetry_data:
            continue

        if telemetry_data['p.paused'] != STATE_FLIGHT:
            continue

        telem = orbit_telemetry_bstring(telemetry_data)
        openc3_connection.send(telem)

        mission_time = datetime.timedelta(seconds=telemetry_data.get('v.missionTime', 0))
        logger.info('T+%s Orbit: %s', mission_time, telemetry_data.get('v.body', 'None'))


def game_telemetry_loop():
    """loop of recieving telemetry from Telemachus, translating it, and sending it to OpenC3"""
    openc3_connection = OpenC3Connection(
        config['openc3']['host'],
        config['openc3']['telemetry_port'])

    telemachus_link_vehicle = TelemachusConnector(
        config['telemachus']['host'],
        config['telemachus']['port'],
        1_000)

    telemachus_link_vehicle.subscribe('p.paused')

    logger.info('Orbit Telemetry Starting')

    game_state = None

    while True:
        if stop_event.is_set():
            break

        if telemachus_link_vehicle.web_socket is None:
            telemachus_link_vehicle.reconnect()
            continue

        telemetry_data = telemachus_link_vehicle.recieve() # get telem data
        if not telemetry_data:
            continue

        telem = game_telemetry_bstring(telemetry_data)
        openc3_connection.send(telem)

        if game_state != telemetry_data['p.paused']:
            game_state = telemetry_data['p.paused']

            mission_time = datetime.timedelta(seconds=telemetry_data.get('v.missionTime', 0))
            logger.info('T+%s Game: %s', mission_time, STATE_STRINGS[telemetry_data['p.paused']])


def main():
    """run the telemetry downlink relay"""
    try:
        vtt = threading.Thread(target = vehicle_telemetry_loop, daemon = True)
        vtt.start()

        ott = threading.Thread(target = orbit_telemetry_loop, daemon = True)
        ott.start()

        gtt = threading.Thread(target = game_telemetry_loop, daemon = True)
        gtt.start()

    except Exception:
        logger.exception('Main Failed')

    vtt.join()


if __name__ == '__main__':
    main()
