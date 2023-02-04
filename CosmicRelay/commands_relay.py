"""the controll loops for the commands relay pipeline"""
from typing import ByteString
import asyncio
import re
import telnetlib3
from CosmicKSP.logging import get_logger
from CosmicKSP.config import config
from CosmicKSP.kos.commands import COMMANDS as kos_commands
from CosmicKSP.ksp_management.commands import COMMANDS as ksp_commands
from CosmicKSP.kos import kos_status_telemetry

logger = get_logger(name='CosmicKSP_Commanding')
logger.setLevel(config['logging_level'])

COMMANDS = kos_commands.copy()
COMMANDS.update(ksp_commands)

READY = 0
BUISY = 1
DETACHED = 2

STATE_DATA ={
    'state': DETACHED,
    'cpu_id': 0,
    'cpu_name': '',
    'vessel_name': '',
    'running_script': '',
    'message': ''
}

AVAILABLE_CPUS = []


def openc3_to_command(b_command: ByteString) -> str:
    """translate the given openc3 command into a kos command"""
    for id_str, cmd in COMMANDS.items():
        if b_command.startswith(id_str):
            return cmd(b_command)

    return ''


async def telemetry_loop(kos_reader, openc3_writer) -> None:
    """threa for listening to kos and relaying messages to openc3"""
    total_output = ''
    # in_comment = False

    while True:
        kos_message = await kos_reader.read(1024)

        if not kos_message:
            raise Exception("KOS Connection Closed")

        # detect and insert a "new line"
        kos_message = re.sub(r'(\x9B|\x1B\[)[0-?]*;1H', "\n", kos_message)
        # remove remaining ansi excape codes
        kos_message = re.sub(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]', "", kos_message)

        total_output += kos_message
        if '\n' not in total_output:
            continue

        lines = total_output.split('\n')

        # detect and report a detached state
        if 'Choose a CPU' in total_output:
            STATE_DATA['state'] = DETACHED
            STATE_DATA['cpu_id'] = 0
            STATE_DATA['cpu_name'] = ''
            STATE_DATA['vessel_name'] = ''

            del AVAILABLE_CPUS[:]

            for line in lines:
                if re.search(r'\[\d+\]', line):
                    cpu_data = re.split(r'\s+', line)

                    AVAILABLE_CPUS.append((
                        int(cpu_data[1][1:-1]),
                        ' '.join(cpu_data[4:-2]),
                        cpu_data[-2][1:-1],
                    ))

            STATE_DATA['message'] = "Choose a CPU:\n" + '\n'.join(
                [f'{avc[0]}: {avc[2]}:{avc[1]}' for avc in AVAILABLE_CPUS]
                )

            logger.info('Detached from CPU')
            openc3_writer.write(kos_status_telemetry(STATE_DATA))
            await openc3_writer.drain()
        

        elif 'kOS Operating System' in total_output:
            # get the first digit
            cpu_id = int(re.search('\d', total_output)[0])
            STATE_DATA['cpu_id'] = cpu_id

            for id, vessel_name, cpu_name in AVAILABLE_CPUS:
                if id == cpu_id:
                    STATE_DATA['state'] = READY
                    STATE_DATA['cpu_name'] = cpu_name
                    STATE_DATA['vessel_name'] = vessel_name
                    STATE_DATA['running_script'] = ''
                    STATE_DATA['message'] = ''

                    logger.info('Status Message: Attaching to CPU: %s', cpu_id)
                    openc3_writer.write(kos_status_telemetry(STATE_DATA))
                    await openc3_writer.drain()
                    break

        elif 'Program ended.' in total_output:
            STATE_DATA['state'] = READY
            STATE_DATA['running_script'] = ''
            logger.info('Status Message: Program Ended')
            openc3_writer.write(kos_status_telemetry(STATE_DATA))
            await openc3_writer.drain()

        else:
            for line in lines:
                if line.startswith('//'):
                    STATE_DATA['message'] = line[2:]

                    logger.info('Status Message: %s', line[2:])
                    openc3_writer.write(kos_status_telemetry(STATE_DATA))
                    await openc3_writer.drain()

        total_output = lines[-1]


async def commaning_loop(openc3_reader, kos_writer) -> None:
    """the commanding loop"""

    while True:
        openc3_command = await openc3_reader.read(4096)

        logger.info('Command Recieved: %s', openc3_command)

        if not openc3_command:
            logger.error('empty command: %s', openc3_command)
            continue

        kos_command = openc3_to_command(openc3_command)

        if not kos_command:
            continue

        # if not isinstance(kos_command, tuple):
        logger.info('Relaying Command: "%s"', kos_command)
        kos_writer.write(kos_command)
        await kos_writer.drain()



async def kos_init(kos_reader, kos_writer, cpu: int = 1) -> None:
    """initialize the kos connection by selecting the 1st cpu"""
    _ = await kos_reader.read(4096)
    kos_writer.write(f'{cpu}\n')
    await kos_writer.drain()
    _ = await kos_reader.read(4096)



async def relay_loop(kos_reader, kos_writer) -> None:
    """the main async function"""

    # initialize to a kos cpu
    # await kos_init(kos_reader, kos_writer)
    logger.info('KOS Connection Opened')

    # connect to the openc3 commanding port
    openc3_commands_reader, openc3_commands_writer = \
        await asyncio.open_connection(config['openc3']['host'], config['openc3']['commands_port'])

    logger.info('OpenC3 Commanding Connection Opened')

    # connect to the open c3 telemetry port
    openc3_telemetry_reader, openc3_telemetry_writer = \
        await asyncio.open_connection(config['openc3']['host'], config['openc3']['telemetry_port'])

    logger.info('OpenC3 Telemetry Connection Opened')

    # start the tasks
    commanding_task = asyncio.create_task(commaning_loop(openc3_commands_reader, kos_writer))
    telemetry_task = asyncio.create_task(telemetry_loop(kos_reader, openc3_telemetry_writer))

    await commanding_task
    await telemetry_task



def main():
    """main function for Commandig relay"""
    loop = asyncio.get_event_loop()

    coroutine = telnetlib3.open_connection(
        config['kos']['host'],
        config['kos']['port'],
        shell = relay_loop,
        encoding_errors = 'strict',
        term='XTERM')

    reader, writer = loop.run_until_complete(coroutine)

    loop.run_until_complete(writer.protocol.waiter_closed)


if __name__ == '__main__':
    main()
