"""contains the socket link managers for the OpenC3 connections"""
import socket


class OpenC3Connection():
    """manages the socket connection to the OpenC3 telemetry"""

    def __init__(self, host: str, port: int):
        self.socket = None
        self.host = host
        self.port = port
        self.reconnect()


    def reconnect(self):
        """reconnect to the telemachus socket"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.host, self.port)
        self.socket.connect(server_address)


    def disconnect(self):
        """disconnect from the cosmos socket"""
        if self.socket is not None:
            self.socket.close()

        self.socket = None


    def send(self, message_str):
        """send a message to cosmos, data is a byte string"""
        self.socket.sendall(message_str)


    def recieve(self):
        """wait for the next command and return the contents"""
        return self.socket.recv(1024)


    def __del__(self):
        """ Make sure we disconnect cleanly"""
        if getattr(self, 'socket', None) is not None:
            self.disconnect()
