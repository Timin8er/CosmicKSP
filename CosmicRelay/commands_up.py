"""the controll loops for the commands relay pipeline"""
import time
from typing import Dict, ByteString
from CosmicKSP.logging import logger
from CosmicKSP.kos_links import KosConnection
from CosmicKSP.commands import COMMANDS
from CosmicKSP.openc3_links import OpenC3CommandsLink


def openc3_to_kos_command(b_command: ByteString) -> str:
    for id, cmd in COMMANDS.items():
        if b_command.startswith(id):
            try:
                return cmd(b_command)
                
            except Exception:
                logger.exception('Error Processing Command: %s', b_command)
            
            break
    else:
        logger.error('Command recieved but not identified: %s', b_command)
        return ''


def commands_loop():
    """loop of recieving telemetry"""
    logger.info('Commands Relay Starting')

    kos = KosConnection()
    openc3 = OpenC3CommandsLink()

    while True:
        try:
            openc3_command = openc3.listen()
            if not openc3_command:
                continue
            
            kos_command = openc3_to_kos_command(openc3_command)
            logger.info('Relaying Command: %s', kos_command)
            kos.send_command_str(kos_command)

        except KeyboardInterrupt:
            logger.info('Commands Relay Stopped: Keyboard Interupt')
            break
