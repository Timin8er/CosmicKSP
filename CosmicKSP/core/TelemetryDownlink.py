import websocket
import socket
import json
import time
import datetime
import struct
from PyQt5.QtCore import QThread, pyqtSignal
from CosmicKSP.logging import logger
from CosmicKSP.config import config

TELEMETRY_SUBSCIPTIONS = [
    'v.missionTime',
    't.universalTime',
    'p.paused',
    'v.altitude',
    'v.lat',
    'v.long',
    'r.resource[electricity]',
    's.sensor.acc',
    's.sensor.temp',
    'f.abort',
    'f.throttle',
    'b.number',
]

STATE_SIGNAL_LOST = -1
STATE_FLIGHT = 0
STATE_PAUSED = 1
STATE_NO_POWER = 2
STATE_OFF = 3
STATE_NOT_FOUND = 4
STATE_CONSTRUCTION = 5


class telemachusDownlink(object):
    """initially coppied from https://github.com/ec429/konrad/blob/master/downlink.py"""

    def __init__(self):
        logger.debug(f'Telemachus Settings: {config["TELEMACHUS"]}')
        self.web_socket = None
        self.uri = "ws://%s:%d/datalink" % (config['TELEMACHUS']['HOST'], config['TELEMACHUS']['PORT'])
        self.rate = config["TELEMACHUS"]['FREQUENCY']

        self.subscriptions = TELEMETRY_SUBSCIPTIONS
        self.data = {}

        self.body_ids = {} # name => ID

        self.reconnect()


    def reconnect(self):
        """reconnect to the telemachus socket"""
        try:
            self.web_socket = websocket.create_connection(self.uri)

        except socket.error as e:
            # Failed to connect; enter 'link down' state
            logger.exception('Failed to connect to Telemachus')
            self.web_socket = None

        else:
            self.set_rate()
            self.resubscribe()


    def disconnect(self):
        """disconnect from the telemachus socket"""
        if self.web_socket is not None:
            self.web_socket.close()

        self.web_socket = None


    def send_msg(self, data):
        """send a message to telemachus, data is a dict"""
        if self.web_socket is not None:
            message_str = json.dumps(data)
            logger.debug(f'Sending Message: {message_str}')

            self.web_socket.send(message_str)

        else:
            logger.error(f'Telemachus Message Not Sent: {data}')


    def set_rate(self):
        """set the data rate"""
        self.send_msg({'rate': self.rate})

        if self.web_socket is not None:
            self.web_socket.settimeout(self.rate / 500.0)


    def resubscribe(self):
        """resubscribe all"""
        for key in self.subscriptions:
            self.send_msg({'+':[key]})


    def listen(self):
        msg = '{}'
        for i in range(3):
            try:
                if self.web_socket is None:
                    self.reconnect()
                else:
                    msg = self.web_socket.recv()
                    break

            except websocket.WebSocketTimeoutException:
                break

            except websocket.WebSocketConnectionClosedException:
                time.sleep(self.rate / 2000.0)
                continue

            except KeyboardInterrupt:
                self.disconnect()
                raise

        try:
            return json.loads(msg)
        except ValueError: # unparseable JSON, did the link break?
            return {}


    def update(self):
        """get and store the latest data"""
        d = self.listen()
        if not d: # Loss of Signal
            self.data = {}

        else:
            self.data.update(d)
            self.update_bodies()

        return self.data


    def update_bodies(self):
        """update and subscribe to bodies as they change during mission time"""
        nbodies = self.data.get('b.number', 0)

        if not nbodies:
            return # can't do anything

        for i in range(nbodies):
            n = self.data.get(f'b.name[{i}]', None)

            if n is None:
                self.subscribe(f'b.name[{i}]')
            else:
                self.body_ids[n] = i



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



class telemetryRelayThread(QThread):

    telemReport = pyqtSignal(dict)
    signalStatus = pyqtSignal(int)

    def run(self):
        telemetry_loop()



def telemetry_loop():
    timeout_interval = (config["TELEMACHUS"]['FREQUENCY'] * 2) / 1000
    logger.info('Thread Starting')
    signal_state = -1
    last_recieved = datetime.datetime.now()

    data_link = telemachusDownlink()

    while True:
        if data_link.web_socket is None:
            # TODO: keep trying to connect when unable
            break

        data = data_link.update() # get telem data

        if signal_state >= 0 and (datetime.datetime.now() - last_recieved).total_seconds() > timeout_interval:
            signal_state = -1
            forwardState(signal_state)

        # if found data
        if data:
            if signal_state != data['p.paused']: # reset connection status
                signal_state = data['p.paused']
                forwardState(signal_state)

            last_recieved = datetime.datetime.now()
            if signal_state != 5: # not construction
                forwardReport(data)

    logger.info('Thread Stopped')


def forwardState(state):
    if state == STATE_SIGNAL_LOST:
        logger.info(f'Status: Signal Lost')

    elif state == STATE_FLIGHT:
        logger.info(f'Status: Flight')

    elif state == STATE_PAUSED:
        logger.info(f'Status: Paused')

    elif state == STATE_NO_POWER:
        logger.info(f'Status: No Power')

    elif state == STATE_OFF:
        logger.info(f'Status: Off')

    elif state == STATE_NOT_FOUND:
        logger.info(f'Status: not found')

    elif state == STATE_CONSTRUCTION:
        logger.info(f'Status: Construction')


def forwardReport(data):
    mission_time = datetime.timedelta(seconds=data.get('v.missionTime', 0))
    logger.info(f'Telem Recieved T+{mission_time}')



if __name__ == '__main__':
    dl = telemachusDownlink()

    while True:
        data = dl.update()
        if data:
            mission_time = datetime.timedelta(seconds=data['v.missionTime'])
            logger.info(f'[{mission_time}] : {data}')
