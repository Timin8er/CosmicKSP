import datetime
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon

from CosmicKSP.ui.icons import GPS_SIGNAL, GPS_DISCONNECTED
from CosmicKSP.core.TelemetryDownlink import telemetryRelayThread
from CosmicKSP import settings

from .RelayUIDesigner import Ui_RelayMainWindow


class relayUIMainWindow(QMainWindow, Ui_RelayMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(GPS_DISCONNECTED))

        self.tlm_log_text = '' # complete log for telemetry

        self.telemetry_listener_thread = telemetryRelayThread(settings.REAL_GAME_INSTANCE)
        self.telemetry_listener_thread.telemReport.connect(self.logTelemetry)
        self.telemetry_listener_thread.signalStatus.connect(self.logTelemetryStatus)
        self.telemetry_listener_thread.start()


    def tmlLog(self, msg):
        # append the log text
        real_time = datetime.datetime.now()
        self.tlm_log_text += f'\n[{real_time.strftime("%H:%M:%S")}] {msg}'

        # don't do that
        val = self.telemetryTextBrowser.verticalScrollBar().value()
        bot = (self.telemetryTextBrowser.verticalScrollBar().maximum() == self.telemetryTextBrowser.verticalScrollBar().value())

        self.telemetryTextBrowser.setText(self.tlm_log_text)

        if bot:
            self.telemetryTextBrowser.verticalScrollBar().setValue(self.telemetryTextBrowser.verticalScrollBar().maximum());
        else:
            self.telemetryTextBrowser.verticalScrollBar().setValue(val);


    def logTelemetry(self, data):
        mission_time = datetime.timedelta(seconds=data['v.missionTime'])
        self.tmlLog(f'Telem Recieved T+{mission_time}')

        # LOG_TLM = {
        #     'v.missionTime':'{:.3f} ',
        #     't.universalTime':'{} ',
        #     'v.altitude':'{:.3f} ',
        #     'r.resource[LiquidFuel]':'{:.3f}'
        # }
        #
        # dstring = ''
        # for key, formating in LOG_TLM.items():
        #     dstring += formating.format(data[key])
        #
        # self.tmlLog(f'T+{mission_time} {dstring}')


    def logTelemetryStatus(self, status):
        if status:
            self.setWindowIcon(QIcon(GPS_SIGNAL))
            self.tmlLog(f'Connected')
        else:
            self.setWindowIcon(QIcon(GPS_DISCONNECTED))
            self.tmlLog(f'Disconnected')


    def __del__(self):
        self.telemetry_listener_thread.exit()
