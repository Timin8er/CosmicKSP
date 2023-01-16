"""the controll loops for the commands relay pipeline"""
from typing import ByteString
from CosmicKSP.logging import get_logger
from CosmicKSP.config import config
from CosmicKSP.kos import KosConnection
from CosmicKSP.kos.commands import COMMANDS
from CosmicKSP.openc3 import OpenC3Connection


logger = get_logger(name='CosmicKSP_Commanding')
logger.setLevel(config['logging_level'])


def openc3_to_kos_command(b_command: ByteString) -> str:
    """translate the given openc3 command into a kos command"""
    for id_str, cmd in COMMANDS.items():
        if b_command.startswith(id_str):
            return cmd(b_command)

    return ''


def commands_loop():
    """loop of recieving commands from OpenC3, translating it, and sending it to KOS"""
    openc3_connection = OpenC3Connection(
        config['openc3']['host'],
        config['openc3']['commands_port'])

    kos_connection = KosConnection(
        config['kos']['host'],
        config['kos']['port'],
        config['kos']['timeout'])

    logger.info('Commands Relay Starting')

    while True:
        openc3_command = openc3_connection.recieve()
        if not openc3_command:
            continue

        try:
            kos_command = openc3_to_kos_command(openc3_command)
        except Exception:
            logger.exception('Command Translation Failed')
            continue

        if not kos_command:
            logger.error('Command unable to be translated: %s', kos_command)
            continue

        logger.info('Relaying Command: %s', kos_command)

        try:
            kos_connection.send(kos_command)
        except Exception:
            logger.exception('Unable to send command: %s', kos_command)



def main():
    """run the commands uplink relay"""
    try:
        commands_loop()

    except Exception:
        logger.exception('Main Failed')


if __name__ == '__main__':
    main()