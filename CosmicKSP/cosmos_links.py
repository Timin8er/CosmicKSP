"""contains the socket link managers for the OpenC3 connections"""
import socket
import struct

from CosmicKSP.config import config
from CosmicKSP.logging import logger


class OpenC3TelemetryLink():
    """manages the socket connection to the OpenC3 telemetry"""

    def __init__(self):
        logger.debug("Cosmos Telemetry Port: %s:%s",
            config['COSMOS']['HOST'], config['COSMOS']['TELEMETRY_PORT'])
        self.socket = None
        self.reconnect()


    def reconnect(self):
        """reconnect to the telemachus socket"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (config['COSMOS']['HOST'], config['COSMOS']['TELEMETRY_PORT'])
            self.socket.connect(server_address)

        except socket.error:
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
            message_str = struct.pack('>hf', 1, 5.2)
            # message_str = struct.pack('>hf?', 1, 5.2, True)
            # message_str = bytes.fromhex('0100001')
            logger.debug('Sending Cosmos Message: %s', message_str)

            self.socket.sendall(message_str)

        else:
            logger.error('Cosmos Message Not Sent: %s', data)


    def __del__(self):
        """ Make sure we disconnect cleanly, or telemachus gets unhappy """
        if getattr(self, 'ws', None) is not None:
            self.disconnect()


class OpenC3CommandsLink():
    """manages the socket link to the OpenC3 commands"""

    def __init__(self):
        logger.debug("Cosmos Commands Port Settings: %s:%s",
            config['COSMOS']['HOST'], config['COSMOS']['COMMANDS_PORT'])
        self.socket = None
        self.reconnect()


    def reconnect(self):
        """reconnect to the telemachus socket"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (config['COSMOS']['HOST'], config['COSMOS']['COMMANDS_PORT'])
            self.socket.connect(server_address)

        except socket.error:
            # Failed to connect
            logger.exception('Failed to connect to Cosmos')
            self.socket = None


    def disconnect(self):
        """disconnect from the cosmos socket"""
        if self.socket is not None:
            self.socket.close()

        self.socket = None


    def listen(self):
        """wait for the next command and return the contents"""
        return self.socket.recv(1024)


    def __del__(self):
        """ Make sure we disconnect cleanly"""
        if getattr(self, 'socket', None) is not None:
            self.disconnect()
