"""mange the socket connection to telemechus"""
import websocket
import socket
import json
import time
import datetime
from typing import Dict
from CosmicKSP.logging import logger
from CosmicKSP.config import config
from CosmicKSP.telemetry import *


class TelemachusSocket():
    """initially coppied from https://github.com/ec429/konrad/blob/master/downlink.py"""

    def __init__(self):
        logger.debug('Telemachus Settings: %s', config["TELEMACHUS"])
        self.web_socket = None
        self.uri = f"ws://{config['TELEMACHUS']['HOST']}:{config['TELEMACHUS']['PORT']}/datalink"
        self.rate = config["TELEMACHUS"]['FREQUENCY']
        self.timeout_interval = 5

        self.subscriptions = TELEMETRY_SUBSCIPTIONS
        self.body_ids: Dict[str, int] = {} # name => ID
        self.latest_telemetry: Dict = {}
        self.game_state: int = -1
        self.last_recieved_time = None

        self.reconnect()


    def reconnect(self):
        """reconnect to the telemachus socket"""
        try:
            self.web_socket = websocket.create_connection(self.uri)

        except socket.error:
            # Failed to connect; enter 'link down' state
            logger.exception('Failed to connect to Telemachus')
            self.web_socket = None
            raise

        else:
            logger.info('Telemachus Connected: %s', self.uri)
            self.set_rate()
            self.resubscribe()


    def disconnect(self):
        """disconnect from the telemachus socket"""
        if self.web_socket is not None:
            self.web_socket.close()

        self.web_socket = None


    def send_msg(self, data: Dict):
        """send a message to telemachus, data is a dict"""
        if self.web_socket is not None:
            message_str = json.dumps(data)
            logger.debug('Sending Message: %s', message_str)

            self.web_socket.send(message_str)

        else:
            logger.error('Telemachus Message Not Sent: %s', data)


    def set_rate(self):
        """set the data rate"""
        self.send_msg({'rate': self.rate})

        if self.web_socket is not None:
            self.web_socket.settimeout(self.rate / 500.0)


    def resubscribe(self):
        """resubscribe all"""
        for key in self.subscriptions:
            self.send_msg({'+':[key]})


    # def listen(self) -> Dict:
    #     """wait for a new telemetry packet and return it"""
    #     msg = '{}'
    #     for _ in range(3):
    #         try:
    #             if self.web_socket is None:
    #                 self.reconnect()
    #             else:
    #                 msg = self.web_socket.recv()
    #                 break

    #         except websocket.WebSocketTimeoutException:
    #             break

    #         except websocket.WebSocketConnectionClosedException:
    #             time.sleep(self.rate / 2000.0)
    #             continue

    #         except KeyboardInterrupt:
    #             self.disconnect()
    #             raise

    #     try:
    #         return json.loads(msg)

    #     except ValueError: # unparseable JSON
    #         logger.exception('Failure to parse telemetry message: %s', msg)
    #         return {}

    def listen(self) -> Dict:
        """wait for a new telemetry packet and return it"""
        msg = self.web_socket.recv()

        try:
            return json.loads(msg)

        except ValueError: # unparseable JSON
            logger.exception('Failure to parse telemetry message: %s', msg)
            return {}


    def update(self):
        """get and store the latest data"""
        new_telemetry = self.listen()
        if not new_telemetry: # Loss of Signal
            return self.latest_telemetry

        # set the p.paused (game state) to -1 if the game is paused
        if new_telemetry['p.paused'] >= 0 and \
                (datetime.datetime.now() - self.last_recieved_time).total_seconds() > self.timeout_interval:
            new_telemetry['p.paused'] = -1
            
        self.latest_telemetry.update(new_telemetry)
        self.game_state = self.latest_telemetry.get('p.paused', 4)
        self.update_bodies()

        return self.latest_telemetry


    def update_bodies(self):
        """update and subscribe to bodies as they change during mission time"""
        nbodies = self.latest_telemetry.get('b.number', 0)

        if not nbodies:
            return # can't do anything

        for i in range(nbodies):
            body_name = self.latest_telemetry.get(f'b.name[{i}]', None)

            if body_name is None:
                self.subscribe(f'b.name[{i}]')
            else:
                self.body_ids[body_name] = i


    def subscribe(self, key):
        """subscribe to the telemachus key"""
        if key not in self.subscriptions:
            self.subscriptions.append(key)
        self.send_msg({'+':[key]})


    def unsubscribe(self, key):
        """unsubscribe from the telemachus key"""
        if key in self.subscriptions:
            self.subscriptions.remove(key)
        self.send_msg({'-':[key]})


    def __del__(self):
        """ Make sure we disconnect cleanly, or telemachus gets unhappy """
        if getattr(self, 'ws', None) is not None:
            self.disconnect()




