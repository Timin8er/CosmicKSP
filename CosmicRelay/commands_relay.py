"""the controll loops for the commands relay pipeline"""
from typing import ByteString
from CosmicKSP.logging import get_logger
from CosmicKSP.config import config
from CosmicKSP.kos import KosConnection
from CosmicKSP.kos.commands import COMMANDS
from CosmicKSP.openc3 import OpenC3Connection
import asyncio, telnetlib3


logger = get_logger(name='CosmicKSP_Commanding')
logger.setLevel(config['logging_level'])


def openc3_to_kos_command(b_command: ByteString) -> str:
    """translate the given openc3 command into a kos command"""
    for id_str, cmd in COMMANDS.items():
        if b_command.startswith(id_str):
            return cmd(b_command)

    return ''


# def commands_loop():
#     """loop of recieving commands from OpenC3, translating it, and sending it to KOS"""
#     openc3_connection = OpenC3Connection(
#         config['openc3']['host'],
#         config['openc3']['commands_port'])

#     kos_connection = KosConnection(
#         config['kos']['host'],
#         config['kos']['port'],
#         config['kos']['timeout'])

#     logger.info('Commands Relay Starting')

#     while True:
#         openc3_command = openc3_connection.recieve()
#         if not openc3_command:
#             continue

#         try:
#             kos_command = openc3_to_kos_command(openc3_command)
#         except Exception:
#             logger.exception('Command Translation Failed')
#             continue

#         if not kos_command:
#             logger.error('Command unable to be translated: %s', kos_command)
#             continue

#         logger.info('Relaying Command: %s', kos_command)

#         try:
#             kos_connection.send(kos_command)
#         except Exception:
#             logger.exception('Unable to send command: %s', kos_command)


# async def kos_telemetry_shell(reader, writer):
#     """the kos telemetry loop"""
#     logger.info('starting kos telemetry')

#     await asyncio.sleep(2)

#     outp = await reader.read(1024)
#     # print(outp, flush=True)
#     writer.write('1\n')

#     outp = await reader.read(1024)
#     # print(outp, flush=True)

#     logger.info('KOS Telemetry Connection Established')

#     while True:
#         outp = await reader.read(1024)
#         if not outp or outp.isspace():
#             # End of File
#             break

#         print(outp, flush=True)

#         if '{Detaching from' in outp:
#             break


async def commands_relay_shell(reader, writer):
    """the commanding loop"""
    outp = await reader.read(1024)
    # print(outp, flush=True)
    writer.write('1\n')

    outp = await reader.read(1024)
    # print(outp, flush=True)

    logger.info('Commanding Relay Connection Established')

    openc3_connection = OpenC3Connection(
        config['openc3']['host'],
        config['openc3']['commands_port'])

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

        logger.info('Relaying Command: "%s"', kos_command)
        writer.write(kos_command)
        outp = await reader.read(1024)

        if '{Detaching from' in outp:
            break


# async def a_main():
#     """run both tasks"""
#     loop = asyncio.get_event_loop()

#     relay_coro = telnetlib3.open_connection(
#         config['kos']['host'],
#         config['kos']['port'],
#         shell=commands_relay_shell)

#     _, relay_writer = await relay_coro

#     tlem_coro = telnetlib3.open_connection(
#         config['kos']['host'],
#         config['kos']['port'],
#         shell=kos_telemetry_shell)

#     _, telem_writer = await tlem_coro

#     task_relay = loop.create_task(relay_coro)
#     task_telem = loop.create_task(tlem_coro)

#     await asyncio.wait([task_relay, task_telem])


def main():
    """main function for telnetlib3 version"""
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(a_main())
    # loop.close()

    coro = telnetlib3.open_connection(
        config['kos']['host'],
        config['kos']['port'],
        shell=commands_relay_shell)

    c_reader, c_writer = loop.run_until_complete(coro)

    loop.run_until_complete(c_writer.protocol.waiter_closed)

    logger.info('Connection Closed')


# def main():
#     """run the commands uplink relay"""
#     try:
#         commands_loop()

#     except Exception:
#         logger.exception('Main Failed')


if __name__ == '__main__':
    main()