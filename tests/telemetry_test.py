from CosmicKSP.logging import logger
from CosmicKSP.openc3_links import OpenC3TelemetryLink
import time
from CosmicKSP.telemetry import vehicle_telemetry_bstring, game_telemetry_bstring


test_telemetry = {
    'v.missionTime': 5.5,
    'v.altitude': 1234567.9,
    'v.lat': 0.001,
    'v.long': 90.001,
    'f.throttle': 0.5,
    'p.paused':-1,
}


def main():
    """send periodic telemetry to cosmos"""
    logger.info('Cosmos Telemetry Injection Starting')

    try:
        data_link = OpenC3TelemetryLink()

        for i in range(7):
            if data_link.socket is None:
                break
                
            test_telemetry['p.paused'] = i - 1 

            time.sleep(1)

            telem = game_telemetry_bstring(test_telemetry)

            data_link.send_telem(telem)

    except KeyboardInterrupt:
        logger.info('Test Stopped: Keyboard Interupt')

    except Exception:
        """log the traceback"""
        logger.exception('Main Failed')
    
    else:
        logger.info('Cosmos Telemetry Loop Finished')


if __name__ == "__main__":
    main()