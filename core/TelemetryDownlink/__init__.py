import websocket
import socket
import json
import time
import datetime
from PyQt5.QtCore import QThread, pyqtSignal


TELEMETRY_SUBSCIPTIONS = [
    'v.missionTime',
    't.universalTime',
    'v.altitude',
    'r.resource[LiquidFuel]'
]


class telemachusDownlink(object):
    """initially coppied from https://github.com/ec429/konrad/blob/master/downlink.py"""

    def __init__(self, telemachus_instance, logf=None):
        self.uri = "ws://%s:%d/datalink"%(telemachus_instance['HOST'], telemachus_instance['PORT'])
        self.rate = telemachus_instance['FREQUENCY']
        self.subscriptions = {}
        self.data = {}
        self.logf = logf
        self.reconnect()
        self.body_ids = {} # name => ID
        self.bodies_subscribed = False

        for key in TELEMETRY_SUBSCIPTIONS:
            self.subscribe(key)


    def reconnect(self):
        try:
            self.ws = websocket.create_connection(self.uri)
        except socket.error:
            # Failed to connect; enter 'link down' state
            self.ws = None
            self.data = {}
            return
        self.set_rate()
        self.resubscribe()


    def disconnect(self):
        if self.ws is not None:
            self.ws.close()
        self.ws = None
        self.data = {}


    def log(self, s):
        if not self.logf: return
        if 'v.missionTime' in self.data:
            now = self.data['v.missionTime']
            nowstr = 'T%.3f'%(now,)
        else:
            now = time.time()
            nowstr = 'U%.3f'%(now,)
        self.logf.write('%s%s\n'%(nowstr, s))


    def send_msg(self, d):
        s = json.dumps(d)
        self.log('> ' + s)
        if self.ws is not None:
            self.ws.send(s)


    def set_rate(self):
        self.send_msg({'rate': self.rate})
        if self.ws is not None:
            self.ws.settimeout(self.rate / 500.0)


    def resubscribe(self):
        for key in self.subscriptions:
            self._subscribe(key)


    def listen(self):
        msg = '{}'
        for i in range(3):
            try:
                if self.ws is None:
                    self.reconnect()
                else:
                    msg = self.ws.recv()
                    break
            except websocket.WebSocketTimeoutException:
                break
            except websocket.WebSocketConnectionClosedException:
                time.sleep(self.rate / 2000.0)
                continue
            except KeyboardInterrupt:
                self.disconnect()
                raise
        self.log('< ' + msg)
        try:
            return json.loads(msg)
        except ValueError: # unparseable JSON, did the link break?
            return {}


    def update(self):
        d = self.listen()
        if not d: # Loss of Signal
            self.data = {}
        self.data.update(d)
        self.update_bodies()
        return self.data


    def update_bodies(self):
        # Assumes self.data has been updated already
        self.body_ids = {} # name => ID
        nbodies = self.get('b.number')
        if nbodies is None:
            return # can't do anything
        if not self.bodies_subscribed:
            for i in range(nbodies):
                self.subscribe('b.name[%d]'%(i,))
            self.bodies_subscribed = True
            return # have to wait till next time
        for i in range(nbodies):
            n = self.get('b.name[%d]'%(i,))
            if n is not None:
                self.body_ids[n] = i


    def get(self, key, default=None):
        return self.data.get(key, default)


    def put(self, key, value):
        # Used for recording derived / calculated values
        self.data[key] = value


    def subscribe(self, key):
        self.subscriptions[key] = self.subscriptions.get(key, 0) + 1
        self._subscribe(key)


    def _subscribe(self, key):
        self.send_msg({'+':[key]})


    def unsubscribe(self, key):
        if self.subscriptions.get(key, 0) > 1:
            self.subscriptions[key] -= 1
        else:
            self.subscriptions.pop(key, None)
            self.data.pop(key, None)
            self.send_msg({'-':[key]})


    def __del__(self):
        # Make sure we disconnect cleanly, or telemachus gets unhappy
        if getattr(self, 'ws', None) is not None:
            self.disconnect()



class telemetryRelayThread(QThread):

    telemReport = pyqtSignal(dict)
    signalStatus = pyqtSignal(bool)


    def __init__(self, game_instance):
        super().__init__()
        self.telemachus_instance = game_instance['TELEMACHUS']


    def run(self):
        connected = False
        last_recieved = datetime.datetime.now()
        timeout_interval = (self.telemachus_instance['FREQUENCY'] * 2) / 1000

        dl = telemachusDownlink(self.telemachus_instance)

        while True:
            data = dl.update() # get telem data

            # if not data hase come in the last interval, emit that the connection is dead
            if connected and (datetime.datetime.now() - last_recieved).total_seconds() > timeout_interval:
                connected = False
                self.signalStatus.emit(False)

            # if found data
            if data:
                if not connected: # reset connection status
                    connected = True
                    self.signalStatus.emit(True)

                last_recieved = datetime.datetime.now()
                self.telemReport.emit(data)
