"""the controll loops for the commands relay pipeline"""
from typing import ByteString
from CosmicKSP.logging import get_logger
from CosmicKSP.config import config
from CosmicKSP.kos import KosConnection
from CosmicKSP.kos.commands import COMMANDS
from CosmicKSP.openc3 import OpenC3Connection
import asyncio
import telnetlib3


last_command = None

logger = get_logger(name='CosmicKSP_Commanding')
logger.setLevel(config['logging_level'])


def openc3_to_kos_command(b_command: ByteString) -> str:
    """translate the given openc3 command into a kos command"""
    for id_str, cmd in COMMANDS.items():
        if b_command.startswith(id_str):
            return cmd(b_command)

    return ''


async def commands_relay_shell(reader, writer):
    """the commanding loop"""
    outp = await reader.read(1024)
    # print(outp, flush=True)
    writer.write('1\n')

    outp = await reader.read(1024)
    # print(outp, flush=True)

    logger.info('KOS Connection Established')

    openc3_connection = OpenC3Connection(
        config['openc3']['host'],
        config['openc3']['commands_port'])

    logger.info('OpenC3 Connection Established')

    while '{Detaching from' not in outp:
        openc3_command = await openc3_connection.a_recieve()
        # openc3_command = b'\x00\x04\x00\x00\x00'
        # await asyncio.sleep(10)

        if not openc3_command:
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
            shell = commands_relay_shell)

        reader, writer = loop.run_until_complete(coroutine)

        loop.run_until_complete(writer.protocol.waiter_closed)


# def main():
#     """run the commands uplink relay"""
#     try:
#         commands_loop()

#     except Exception:
#         logger.exception('Main Failed')


if __name__ == '__main__':
    main()