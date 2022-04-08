import os
import datetime
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, pyqtSignal

from CosmicKSP.ui.icons import GPS_SIGNAL, GPS_DISCONNECTED
from CosmicKSP.core.TelemetryDownlink import tlmDownlink
from CosmicKSP import settings

from .RelayUIDesigner import Ui_RelayMainWindow


LOG_TLM = {
    # 'v.missionTime':'{:.3f} ',
    # 't.universalTime':'{} ',
    # 'v.altitude':'{:.3f} ',
    # 'r.resource[LiquidFuel]':'{:.3f}'
}


class relayUIMainWindow(QMainWindow, Ui_RelayMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(GPS_DISCONNECTED))

        self.tlm_log_text = ''

        self.telemetry_listener_thread = telemetryListenerThread()
        self.telemetry_listener_thread.telemReport.connect(self.forwardTelemetry)
        self.telemetry_listener_thread.signalStatus.connect(self.updateSignalStatus)
        self.telemetry_listener_thread.start()


    def tmlLog(self, msg):
        real_time = datetime.datetime.now()
        self.tlm_log_text += f'\n[{real_time.strftime("%H:%M:%S")}] {msg}'
        val = self.telemetryTextBrowser.verticalScrollBar().value()
        bot = (self.telemetryTextBrowser.verticalScrollBar().maximum() == self.telemetryTextBrowser.verticalScrollBar().value())

        self.telemetryTextBrowser.setText(self.tlm_log_text)

        if bot:
            self.telemetryTextBrowser.verticalScrollBar().setValue(self.telemetryTextBrowser.verticalScrollBar().maximum());
        else:
            self.telemetryTextBrowser.verticalScrollBar().setValue(val);


    def forwardTelemetry(self, data):
        mission_time = datetime.timedelta(seconds=data['v.missionTime'])

        dstring = ''
        for key, formating in LOG_TLM.items():
            dstring += formating.format(data[key])

        self.tmlLog(f'T+{mission_time} {dstring}')


    def updateSignalStatus(self, status):
        if status:
            self.setWindowIcon(QIcon(GPS_SIGNAL))
            self.tmlLog(f'Connected')
        else:
            self.setWindowIcon(QIcon(GPS_DISCONNECTED))
            self.tmlLog(f'Disconnected')


    def __del__(self):
        self.telemetry_listener_thread.exit()



class telemetryListenerThread(QThread):

    telemReport = pyqtSignal(dict)
    signalStatus = pyqtSignal(bool)

    def run(self):
        connected = False
        last_recieved = datetime.datetime.now()
        timeout_interval = (settings.TELEMACHUS_FREQUENCY * 2) / 1000

        dl = tlmDownlink(settings.TELEMACHUS_HOST, settings.TELEMACHUS_PORT, settings.TELEMACHUS_FREQUENCY)
        for key in settings.TELEMETRY_SUBSCIPTIONS:
            dl.subscribe(key)

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
