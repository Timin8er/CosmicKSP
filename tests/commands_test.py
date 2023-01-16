"""openc3 commands test"""
from CosmicKSP.logging import logger
from CosmicKSP.openc3 import OpenC3CommandsLink
from CosmicKSP.kos.commands import COMMANDS


def main():
    """wait for commands and log what is recieved"""
    logger.info('OpenC3 Commands Listener Starting')

    try:
        data_link = OpenC3CommandsLink()

        while True:
            data = data_link.listen()
            if not data:
                continue

            for id, cmd in COMMANDS.items():
                if data.startswith(id):
                    try:
                        result = cmd(data)
                        logger.info(f'Command: {result}')
                    except Exception:
                        logger.exception('Error Processing Command: %s', data)
                    break
            else:
                logger.error('Command recieved but not identified: %s', data)

    except KeyboardInterrupt:
        logger.info('Loop Stopped: Keyboard Interupt')

    except Exception:
        logger.exception('Main Failed')

    else:
        logger.info('OpenC3 Commands Listener Stopped')


if __name__ == "__main__":
    main()