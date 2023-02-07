"""the telemetry traslation layer between Telemechus and OpenC3"""
from typing import Callable
import datetime
import threading
from CosmicKSP.logging import get_logger
from CosmicKSP.config import config
from CosmicKSP.telemachus import TelemachusConnector, STATE_FLIGHT
from CosmicKSP.telemachus.telemetry import game_telemetry_bstring, orbit_telemetry_bstring, vehicle_telemetry_bstring, \
    VEHICLE_TELEMETRY_SUBSCIPTIONS, ORBIT_TELEMETRY_SUBSCIPTIONS
from CosmicKSP.openc3 import OpenC3Connection


logger = get_logger(name='CosmicKSP_Telemetry')
logger.setLevel(config['logging_level'])

stop_event = threading.Event()


def relay_loop(subscriptions: list,
                         rate: int,
                         conversion_function: Callable,
                         title: str,
                         flight_only: bool = True) -> None:
    """loop to wait for telemetry, convert it and send it to openc3"""

    openc3_connection = OpenC3Connection(
        config['openc3']['host'],
        config['openc3']['telemetry_port'])

    telemachus_connection = TelemachusConnector(
        config['telemachus']['host'],
        config['telemachus']['port'],
        rate)

    logger.info('%s connected', title)

    for sub in subscriptions:
        telemachus_connection.subscribe(sub)

    while True:
        if stop_event.is_set():
            break

        data = telemachus_connection.recieve() # get telem data
        if not data:
            continue

        if flight_only and data.get('p.paused', False) != STATE_FLIGHT:
            continue

        data_str = conversion_function(data)
        if not data_str:
            continue

        openc3_connection.send(data_str)

        mission_time = datetime.timedelta(seconds=data.get('v.missionTime', 0))
        logger.info('T+%s Relaying Telemetry: %s', mission_time, title)


def main():
    """run the telemetry downlink relay"""
    try:
        vtt = threading.Thread(target = relay_loop,
                               daemon = True,
                               args = (VEHICLE_TELEMETRY_SUBSCIPTIONS,
                                       1000,
                                       vehicle_telemetry_bstring,
                                       "Vehicle"))
        vtt.start()

        ott = threading.Thread(target = relay_loop,
                               daemon = True,
                               args = (ORBIT_TELEMETRY_SUBSCIPTIONS,
                                       3000,
                                       orbit_telemetry_bstring,
                                       "Orbit"))
        ott.start()

        gtt = threading.Thread(target = relay_loop,
                               daemon = True,
                               args = (['p.paused'],
                                       2000,
                                       game_telemetry_bstring,
                                       "Game",
                                       False))
        gtt.start()

    except Exception:
        logger.exception('Main Failed')

    vtt.join()


if __name__ == '__main__':
    main()
