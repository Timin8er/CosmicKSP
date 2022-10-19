import websocket
import socket
import json
import time
import datetime
from PyQt5.QtCore import QThread, pyqtSignal
from PyQtDataFramework.Core.Logging import logger


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

FLIGHT = 0
PAUSED = 1
NO_POWER = 2
OFF = 3
NOT_FOUND = 4


class telemachusDownlink(object):
    """initially coppied from https://github.com/ec429/konrad/blob/master/downlink.py"""

    def __init__(self, settings):
        logger.debug(f'Telemachus Settings: {settings}')
        self.web_socket = None
        self.uri = "ws://%s:%d/datalink"%(settings['HOST'], settings['PORT'])
        self.rate = settings['FREQUENCY']

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
            logger.debug('Sending Message: ' % message_str)

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
        """wait for and return the next data"""
        msg = self.web_socket.recv()

        try:
            return json.loads(msg)

        except ValueError: # unparseable JSON, did the link break?
            logger.exception('unparseable JSON')
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


    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        timeout_interval = (self.settings['FREQUENCY'] * 2) / 1000


    def run(self):
        signal_state = -1
        last_recieved = datetime.datetime.now()

        data_link = telemachusDownlink(self.settings)

        while True:
            if data_link.web_socket is None:
                return

            data = data_link.update() # get telem data

            if signal_state >= 0 and (datetime.datetime.now() - last_recieved).total_seconds() > self.timeout_interval:
                signal_state = -1
                self.signalStatus.emit(-1)

            # if found data
            if data:
                if signal_state != data['p.paused']: # reset connection status
                    signal_state = data['p.paused']
                    self.signalStatus.emit(signal_state)

                last_recieved = datetime.datetime.now()
                if signal_state != 5: # not construction
                    self.telemReport.emit(data)


if __name__ == '__main__':
    dl = telemachusDownlink(settings.REAL_GAME_INSTANCE['TELEMACHUS'])

    while True:
        data = dl.update()
        if data:
            mission_time = datetime.timedelta(seconds=data['v.missionTime'])
            logger.info(f'[{mission_time}] : {data}')
