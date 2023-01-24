"""the controll loops for the commands relay pipeline"""
from typing import ByteString
import asyncio
from socket import timeout as TimeoutException
import telnetlib3
from CosmicKSP.logging import get_logger
from CosmicKSP.config import config
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


async def relay_loop(reader, writer):
    """the commanding loop"""
    # get through the startup prompt
    await reader.read(1024)
    writer.write('1\n')
    outp = await reader.read(1024)

    logger.info('KOS Connection Established')

    # connect to openc3
    openc3_connection = OpenC3Connection(
        config['openc3']['host'],
        config['openc3']['telemetry_port'])
    openc3_connection.socket.settimeout(15)

    logger.info('OpenC3 Connection Established')

    while '{Detaching from' not in outp:
        try:
            openc3_command = openc3_connection.recieve

        except TimeoutException:
            writer.write('.')
            await reader.read(1024)
            continue

        logger.info('Command Recieved: %s', openc3_command)

        if not openc3_command:
            logger.error('empty command: %s', openc3_command)
            continue

        kos_command = openc3_to_kos_command(openc3_command)

        if not kos_command:
            logger.error('Command unable to be translated: %s', kos_command)
            continue

        logger.info('Relaying Command: "%s"', kos_command)

        writer.write(kos_command)
        outp = await reader.read(1024)

    logger.info('Connection Closed')


def main():
    """main function for telnetlib3 version"""
    loop = asyncio.get_event_loop()

    while True:
        coroutine = telnetlib3.open_connection(
            config['kos']['host'],
            config['kos']['port'],
            shell = relay_loop)

        reader, writer = loop.run_until_complete(coroutine)

        loop.run_until_complete(writer.protocol.waiter_closed)


if __name__ == '__main__':
    main()
