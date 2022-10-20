from PyQtDataFramework.Core.Logging import logger
import datetime
import socket
import time
import websocket
from PyQt5.QtCore import QThread, pyqtSignal



class CosmosDownlink(object):
    """initially coppied from https://github.com/ec429/konrad/blob/master/downlink.py"""

    def __init__(self, settings):
        self.websockeet = None
        self.uri = "ws://%s:%d"%(settings['HOST'], settings['PORT'])
        self.reconnect()


    def reconnect(self):
        try:
            self.websockeet = websocket.create_connection(self.uri)

        except socket.error:
            self.websockeet = None


    def disconnect(self):
        if self.websockeet is not None:
            self.websockeet.close()
        self.websockeet = None


    def listen(self):
        msg = None
        status = 'Waiting'
        for i in range(3):
            try:
                if self.websockeet is None:
                    self.reconnect()
                else:
                    msg = self.websockeet.recv()
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

        logger.info(status)
        return msg


    def __del__(self):
        # Make sure we disconnect cleanly, or telemachus gets unhappy
        if getattr(self, 'ws', None) is not None:
            self.disconnect()


def run(settings):

    dl = CosmosDownlink(settings)

    while True:
        if dl.websockeet in None:
            return

        data = dl.listen() # get data
        if data:
            Logging.info('recieved data')
