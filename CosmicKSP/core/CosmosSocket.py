import websocket
import socket
import json
import time
import datetime
from PyQt5.QtCore import QThread, pyqtSignal


class CosmosDownlink(object):
    """initially coppied from https://github.com/ec429/konrad/blob/master/downlink.py"""

    def __init__(self, settings, logf=None):
        self.logf = logf
        self.uri = "ws://%s:%d"%(settings['COSMOS']['HOST'], settings['COSMOS']['PORT'])
        self.reconnect()


    def reconnect(self):
        try:
            self.ws = websocket.create_connection(self.uri)
        except socket.error:
            self.ws = None


    def disconnect(self):
        if self.ws is not None:
            self.ws.close()
        self.ws = None


    def log(self, s):
        now = time.time()
        nowstr = 'U%.3f'%(now,)
        msg = '%s%s\n'%(nowstr, s)
        print(msg)
        if self.logf:
            self.logf.write(msg)


    def listen(self):
        msg = None
        status = 'Waiting'
        for i in range(3):
            try:
                if self.ws is None:
                    self.reconnect()
                else:
                    msg = self.ws.recv()
                    break
            except websocket.WebSocketTimeoutException:
                status = 'WebSocketTimeoutException'
                break
            except websocket.WebSocketConnectionClosedException:
                status = 'WebSocketConnectionClosedException'
                time.sleep(self.rate / 2000.0)
                continue
            except KeyboardInterrupt:
                status = 'KeyboardInterrupt'
                self.disconnect()
                raise
        self.log('< ' + status)
        return msg


    def __del__(self):
        # Make sure we disconnect cleanly, or telemachus gets unhappy
        if getattr(self, 'ws', None) is not None:
            self.disconnect()



class CosmosRelayThread(QThread):

    telemSignal = pyqtSignal(str)
    cmdSignal = pyqtSignal(str)

    def run(self):
        last_recieved = datetime.datetime.now()
        timeout_interval = (self.telemachus_instance['FREQUENCY'] * 2) / 1000

        dl = CosmosDownlink(self.telemachus_instance)

        while True:
            data = dl.listen() # get data

            if (datetime.datetime.now() -last_recieved).total_seconds() > timeout_interval:
                self.cmdSignal.emit('hi')

            # if found data
            if data:
                last_recieved = datetime.datetime.now()
                self.telemSignal.emit(data)



if __name__ == '__main__':
    dl = CosmosDownlink(settings.REAL_GAME_INSTANCE)

    while True:
        data = dl.listen()
        if data:
            print(data)
