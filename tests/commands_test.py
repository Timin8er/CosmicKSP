from CosmicKSP.logging import logger
from CosmicKSP.openc3_links import OpenC3CommandsLink


def main():
    """wait for commands and log what is recieved"""
    logger.info('OpenC3 Commands Listener Starting')

    try:
        data_link = OpenC3CommandsLink()

        while True:
            data = data_link.listen()
            if not data:
                continue
                
            logger.info('Command recieved: %s', data)
    

    except KeyboardInterrupt:
        logger.info('Loop Stopped: Keyboard Interupt')

    except Exception:
        """log the traceback"""
        logger.exception('Main Failed')

    else:
        logger.info('OpenC3 Commands Listener Stopped')


if __name__ == "__main__":
    main()