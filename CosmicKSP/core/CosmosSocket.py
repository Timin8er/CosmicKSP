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



class CosmosRelayThread(QThread):

    telemSignal = pyqtSignal(str)
    cmdSignal = pyqtSignal(str)

    def run(self):
        # last_recieved = datetime.datetime.now()
        # timeout_interval = (self.telemachus_instance['FREQUENCY'] * 2) / 1000

        dl = CosmosDownlink(self.telemachus_instance)

        while True:
            data = dl.listen() # get data

            # if (datetime.datetime.now() - last_recieved).total_seconds() > timeout_interval:
            #     self.cmdSignal.emit('hi')

            # if found data
            if data:
                # last_recieved = datetime.datetime.now()
                self.telemSignal.emit(data)



if __name__ == '__main__':
    dl = CosmosDownlink(settings.REAL_GAME_INSTANCE)

    while True:
        data = dl.listen()
        if data:
            logger.info(data)
