from CosmicKSP.logging import logger
from CosmicKSP.openc3_links import OpenC3TelemetryLink
import time


def main():
    """send periodic telemetry to cosmos"""
    logger.info('Cosmos Telemetry Injection Starting')

    try:
        data_link = OpenC3TelemetryLink()

        for i in range(10):
            if data_link.socket is None:
                break

            time.sleep(1)

            data_link.send_telem({})

    except KeyboardInterrupt:
        logger.info('Test Stopped: Keyboard Interupt')

    except Exception:
        """log the traceback"""
        logger.exception('Main Failed')
    
    else:
        logger.info('Cosmos Telemetry Loop Finished')


if __name__ == "__main__":
    main()