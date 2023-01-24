"""the controll loops for the commands relay pipeline"""
import asyncio
import re
import telnetlib3
from CosmicKSP.logging import get_logger
from CosmicKSP.config import config
from CosmicKSP.kos import kos_status_telemetry
from CosmicKSP.openc3 import OpenC3Connection

logger = get_logger(name='CosmicKSP_KOS')
logger.setLevel(config['logging_level'])


async def relay_loop(reader, writer):
    """the commanding loop"""
    # get through the startup prompt
    outp = await reader.read(1024)
    # print(outp)
    writer.write('1\n')
    outp = await reader.read(1024)
    # print(outp)

    logger.info('KOS Connection Established')

    # connect to openc3
    openc3_connection = OpenC3Connection(
        config['openc3']['host'],
        config['openc3']['telemetry_port'])

    logger.info('OpenC3 Connection Established')

    last_output = ''

    while '{Detaching from' not in outp:
        outp = await reader.read(1024)
        # outp = outp.decode('utf-8')
        outp = re.sub(r'(\x9B|\x1B\[)[0-?]*;1H', "\n", outp) # detect a "new line"
        # outp = re.sub(r'(\x9B|\x1B\[)[0-?]*H', " ", outp) # detect a "space"
        outp = re.sub(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]', "", outp) # remove remaining ansi excape codes
        # print(outp)
        if '\n' in outp:
            outps = '\n'.split(outp)
            outps[0] = last_output + outps[0]
            last_output =  outps[-1]

            for i in outps[:-1]:
                if i.startswith('//'):
                    logger.info('Message: %s', i[2:])
                    openc3_connection.send(kos_status_telemetry({'message': i[2:]}))

        else:
            last_output += outp
        # print(last_output)

    logger.info('Connection Closed')
# ←[25;5H
# ←[S←[25;1H

def main():
    """main function for telnetlib3 version"""
    loop = asyncio.get_event_loop()

    while True:
        coroutine = telnetlib3.open_connection(
            config['kos']['host'],
            config['kos']['port'],
            shell = relay_loop,
            encoding_errors = 'strict',
            term='XTERM')
            # encoding='utf8')

        reader, writer = loop.run_until_complete(coroutine)

        loop.run_until_complete(writer.protocol.waiter_closed)


if __name__ == '__main__':
    main()
