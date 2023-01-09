"""contains the socket link managers for the OpenC3 connections"""
import socket
import struct

from CosmicKSP.config import config
from CosmicKSP.logging import logger


class OpenC3TelemetryLink():
    """manages the socket connection to the OpenC3 telemetry"""

    def __init__(self):
        logger.debug("OpenC3 Telemetry Port: %s:%s",
            config['OPENC3']['HOST'], config['OPENC3']['TELEMETRY_PORT'])
        self.socket = None
        self.reconnect()


    def reconnect(self):
        """reconnect to the telemachus socket"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (config['OPENC3']['HOST'], config['OPENC3']['TELEMETRY_PORT'])
            self.socket.connect(server_address)

        except socket.error:
            logger.exception('Failed to connect to OpenC3')
            self.socket = None


    def disconnect(self):
        """disconnect from the cosmos socket"""
        if self.socket is not None:
            self.socket.close()

        self.socket = None


    def send_telem(self, data):
        """send a message to cosmos, data is a byte string"""
        if self.socket is not None:
            message_str = struct.pack('>hf?', 1, 5.2, True) + b'Hello World'
            logger.debug('Sending OpenC3 Message: %s', message_str.hex())

            self.socket.sendall(message_str)

        else:
            logger.error('OpenC3 Message Not Sent: %s', data)


    def __del__(self):
        """ Make sure we disconnect cleanly, or telemachus gets unhappy """
        if getattr(self, 'ws', None) is not None:
            self.disconnect()


class OpenC3CommandsLink():
    """manages the socket link to the OpenC3 commands"""

    def __init__(self):
        self.socket = None
        self.reconnect()


    def reconnect(self):
        """reconnect to the telemachus socket"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (config['OPENC3']['HOST'], config['OPENC3']['COMMANDS_PORT'])
            self.socket.connect(server_address)

        except socket.error:
            # Failed to connect
            logger.exception('Failed to connect to OpenC3')
            self.socket = None
            raise
        
        else:
            logger.info("OpenC3 Connection: %s:%s", *server_address)


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
