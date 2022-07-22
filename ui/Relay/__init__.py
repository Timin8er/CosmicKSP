import datetime
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from CosmicKSP.ui.icons import GPS_SIGNAL, GPS_DISCONNECTED, ROCKET
from CosmicKSP.core.TelemetryDownlink import telemetryRelayThread
from CosmicKSP.core.CommandsUplink import kosConnection
from CosmicKSP import settings

from .RelayUIDesigner import Ui_RelayMainWindow


class relayWidget(QtWidgets.QWidget):

    def __init__(self, instance):
        super().__init__()
        self.settings = instance

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
        self.cmd_log_text = '' # complete log for telemetry

        self.telemetry_listener_thread = telemetryRelayThread(self.settings)
        self.telemetry_listener_thread.telemReport.connect(self.logTelemetry)
        self.telemetry_listener_thread.signalStatus.connect(self.logTelemetryStatus)
        self.telemetry_listener_thread.start()

        self.commands_uplink = kosConnection(self.settings)
        self.commands_uplink.commandSent.connect(self.logCommand)


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


    def cmdLog(self, msg):
        # append the log text
        real_time = datetime.datetime.now()
        self.cmd_log_text += f'\n[{real_time.strftime("%H:%M:%S")}] {msg}'

        # don't do that
        val = self.commandsTextBrowser.verticalScrollBar().value()
        bot = (self.commandsTextBrowser.verticalScrollBar().maximum() == self.commandsTextBrowser.verticalScrollBar().value())

        self.commandsTextBrowser.setText(self.cmd_log_text)

        if bot:
            self.commandsTextBrowser.verticalScrollBar().setValue(self.commandsTextBrowser.verticalScrollBar().maximum());
        else:
            self.commandsTextBrowser.verticalScrollBar().setValue(val);


    def logCommand(self, cmd):
        self.cmdLog(f'{cmd}')


    def reconnect(self):
        try:
            self.commands_uplink.open()
        except Exception as e:
            print('Ronnect Failed')
            print(e)


    def __del__(self):
        self.telemetry_listener_thread.exit()



class relayUIMainWindow(QtWidgets.QMainWindow, Ui_RelayMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(ROCKET))

        self.relay_widget = relayWidget(settings.REAL_GAME_INSTANCE)
        self.centralwidget.layout().addWidget(self.relay_widget)
