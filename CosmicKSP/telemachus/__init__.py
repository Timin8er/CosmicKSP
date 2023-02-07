"""mange the socket connection to telemechus"""
from typing import Dict
import json
import websocket

STATE_SIGNAL_LOST = -1
STATE_FLIGHT = 0
STATE_PAUSED = 1
STATE_NO_POWER = 2
STATE_OFF = 3
STATE_NOT_FOUND = 4
STATE_CONSTRUCTION = 5


class TelemachusConnector():
    """the basic connection to Telemachus"""

    def __init__(self, host:str, port:int, frequency:int):
        self.web_socket = None
        self.uri = f"ws://{host}:{port}/datalink"
        self.frequency = frequency

        self.reconnect()


    def reconnect(self):
        """reconnect to the telemachus socket"""
        self.web_socket = websocket.create_connection(self.uri)
        self.web_socket.settimeout(self.frequency / 500.0)
        self.send({'rate': self.frequency})


    def disconnect(self):
        """disconnect from the telemachus socket"""
        if self.web_socket is not None:
            self.web_socket.close()

        self.web_socket = None


    def send(self, data: Dict):
        """send a message to telemachus, data is a dict"""
        message_str = json.dumps(data)
        self.web_socket.send(message_str)


    # def recieve(self) -> Dict:
    #     """wait for a new telemetry packet and return it"""
    #     return json.loads(self.web_socket.recv())


    def recieve(self) -> Dict:
        """wait for a new telemetry packet and return it"""
        if self.web_socket is None:
            return {"p.paused": STATE_SIGNAL_LOST}

        try:
            return json.loads(self.web_socket.recv())

        except ConnectionRefusedError:
            return {"p.paused": STATE_SIGNAL_LOST}

        except websocket.WebSocketConnectionClosedException:
            return {"p.paused": STATE_SIGNAL_LOST}

        except websocket.WebSocketTimeoutException:
            return {"p.paused": STATE_PAUSED}


    def subscribe(self, key):
        """subscribe to the telemachus key"""
        self.send({'+':[key]})


    def unsubscribe(self, key):
        """unsubscribe from the telemachus key"""
        self.send({'-':[key]})


    def __del__(self):
        """ Make sure we disconnect cleanly, or telemachus gets unhappy """
        if getattr(self, 'web_socket', None) is not None:
            self.disconnect()
