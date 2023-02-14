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


async def report_cpu_detachment(openc3_writer, kos_output: str) -> None:
    """report to openc3 that kos is detached from a cpu"""
    STATE_DATA['state'] = DETACHED
    STATE_DATA['cpu_id'] = 0
    STATE_DATA['cpu_name'] = ''
    STATE_DATA['vessel_name'] = ''

    del AVAILABLE_CPUS[:]

    for line in kos_output.split('\n'):
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


async def report_cpu_attachment(openc3_writer, kos_output: str) -> None:
    """report to openc3 that a cpu has been attached"""
    # get the first digit
    cpu_id = int(re.search(r'\d', kos_output)[0])

    for cpuid, vessel_name, cpu_name in AVAILABLE_CPUS:
        if cpuid == cpu_id:
            STATE_DATA['state'] = READY
            STATE_DATA['cpu_id'] = cpu_id
            STATE_DATA['cpu_name'] = cpu_name
            STATE_DATA['vessel_name'] = vessel_name
            STATE_DATA['running_script'] = ''
            STATE_DATA['message'] = ''

            logger.info('Status Message: Attaching to CPU: %s', cpu_id)
            openc3_writer.write(kos_status_telemetry(STATE_DATA))
            await openc3_writer.drain()
            return


async def report_script_ended(openc3_writer, kos_output) -> None:
    """report to openc3 that the running kos script has ended"""
    STATE_DATA['state'] = READY
    STATE_DATA['message'] = f'Program Ended: {STATE_DATA["running_script"]}\n{kos_output}'
    STATE_DATA['running_script'] = ''

    logger.info('Status Message: Program Ended')
    openc3_writer.write(kos_status_telemetry(STATE_DATA))
    await openc3_writer.drain()


async def report_script_start(openc3_writer, kos_output) -> None:
    """report that a script has started running"""
    for line in kos_output.split('\n'):
        if line.startswith('runpath'):
            STATE_DATA['running_script'] = re.findall(r'\w+\.ks', line)[0]
            break

    STATE_DATA['state'] = BUISY
    STATE_DATA['message'] = kos_output

    logger.info('Status Message: Script Starting')
    openc3_writer.write(kos_status_telemetry(STATE_DATA))
    await openc3_writer.drain()


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
        # print(kos_message)

        total_output += kos_message
        if '\n' not in total_output:
            continue

        # detect and report a detached state
        if 'Choose a CPU' in total_output:
            await report_cpu_detachment(openc3_writer, total_output)

        # detect and report and attached state
        elif 'kOS Operating System' in total_output:
            await report_cpu_attachment(openc3_writer, total_output)

        # detent the end of a script
        elif 'Program ended.' in total_output or 'Program aborted.' in total_output:
            await report_script_ended(openc3_writer, total_output)

        # detect the start of a script
        elif 'runpath' in total_output:
            await report_script_start(openc3_writer, total_output)

        else:
            STATE_DATA['message'] = total_output

            logger.info('KOS Message: %s', total_output)
            openc3_writer.write(kos_status_telemetry(STATE_DATA))
            await openc3_writer.drain()

        total_output = total_output.split('\n')[-1]


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


async def relay_loop(kos_reader, kos_writer) -> None:
    """the main async function"""

    # initialize to a kos cpu
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

    kos_reader, kos_writer = loop.run_until_complete(coroutine)

    loop.run_until_complete(kos_writer.protocol.waiter_closed)


if __name__ == '__main__':
    main()
