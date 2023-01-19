"""the controll loops for the commands relay pipeline"""
from typing import ByteString
import asyncio
import telnetlib3
import socket
from socket import timeout as TimeoutException
from CosmicKSP.logging import get_logger
from CosmicKSP.config import config
from CosmicKSP.kos.commands import COMMANDS

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
    openc3_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    openc3_connection.settimeout(15)
    server_address = (config['openc3']['host'], config['openc3']['commands_port'])
    openc3_connection.connect(server_address)

    logger.info('OpenC3 Connection Established')

    while '{Detaching from' not in outp:
        try:
            openc3_command = openc3_connection.recv(1024)

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
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    telnet_coroutine = telnetlib3.open_connection(
        config['kos']['host'],
        config['kos']['port'],
        shell = relay_loop)

    reader, writer = loop.run_until_complete(telnet_coroutine)

    loop.run_until_complete(writer.protocol.waiter_closed)


if __name__ == '__main__':
    main()
