import socket
import time
import struct

from CosmicKSP.config import config
from CosmicKSP.logging import logger


class CosmosTelemetryLink(object):

    def __init__(self):
        logger.debug(f'Cosmos Settings: {config["COSMOS"]}')
        self.socket = None
        self.uri = "ws://%s:%d/datalink"%(config["COSMOS"]['HOST'], config["COSMOS"]['TELEMETRY_PORT'])

        self.reconnect()


    def reconnect(self):
        """reconnect to the telemachus socket"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (config['COSMOS']['HOST'], config['COSMOS']['TELEMETRY_PORT'])
            self.socket.connect(server_address)

        except socket.error as e:
            logger.exception('Failed to connect to Cosmos')
            self.socket = None


    def disconnect(self):
        """disconnect from the cosmos socket"""
        if self.socket is not None:
            self.socket.close()

        self.socket = None


    def send_telem(self, data):
        """send a message to cosmos, data is a byte string"""
        if self.socket is not None:
            message_str = struct.pack('hf?', 1, 5.2, True)
            logger.debug(f'Sending Cosmos Message: {message_str}')

            self.socket.sendall(message_str)

        else:
            logger.error(f'Cosmos Message Not Sent: {data}')


    def __del__(self):
        """ Make sure we disconnect cleanly, or telemachus gets unhappy """
        if getattr(self, 'ws', None) is not None:
            self.disconnect()


def cosmos_telemetry_loop():
    """send periodic telemetry to cosmos"""
    logger.info('Cosmos Telemetry Loop Starting')
    data_link = CosmosTelemetryLink()

    while True:
        if data_link.socket is None:
            break

        time.sleep(1)

        data_link.send_telem({})

    logger.info('Cosmos Telemetry Loop Stopped')
