import datetime
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from CosmicKSP.ui.icons import GPS_SIGNAL, GPS_DISCONNECTED
from CosmicKSP.core.TelemetryDownlink import telemetryRelayThread
from CosmicKSP import settings
import pyqtgraph

from .RelayUIDesigner import Ui_RelayMainWindow


class relayWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        horizontalLayout = QtWidgets.QHBoxLayout(self)
        splitter = QtWidgets.QSplitter(Qt.Horizontal)
        horizontalLayout.addWidget(splitter)

        telemetryGroupBox = QtWidgets.QGroupBox(splitter)
        telemetryGroupBox.setTitle("Telemetry")
        splitter.addWidget(telemetryGroupBox)
        self.telemLayout = QtWidgets.QVBoxLayout(telemetryGroupBox)

        self.telemetryTextBrowser = QtWidgets.QTextBrowser(telemetryGroupBox)
        self.telemLayout.addWidget(self.telemetryTextBrowser)

        commandsGroupBox = QtWidgets.QGroupBox(self)
        commandsGroupBox.setTitle("Commands")
        splitter.addWidget(commandsGroupBox)
        self.commandLayout = QtWidgets.QVBoxLayout(commandsGroupBox)

        self.commandsTextBrowser = QtWidgets.QTextBrowser(commandsGroupBox)
        self.commandLayout.addWidget(self.commandsTextBrowser)

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
        mission_time = datetime.timedelta(seconds=data.get('v.missionTime', 0))
        self.tmlLog(f'Telem Recieved T+{mission_time}')


    def logTelemetryStatus(self, status):
        if status == -1:
            self.tmlLog(f'Status: Signal Lost')
        elif status == 0:
            self.tmlLog(f'Status: Flight')
        elif status == 1:
            self.tmlLog(f'Status: Paused')
        elif status == 2:
            self.tmlLog(f'Status: No Power')
        elif status == 3:
            self.tmlLog(f'Status: Off')
        elif status == 4:
            self.tmlLog(f'Status: not found')
        elif status == 5:
            self.tmlLog(f'Status: Construction')


    def __del__(self):
        self.telemetry_listener_thread.exit()



class relayUIMainWindow(QtWidgets.QMainWindow, Ui_RelayMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(GPS_SIGNAL))

        self.relay_widget = relayWidget()
        self.centralwidget.layout().addWidget(self.relay_widget)