from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from CosmicKSP import settings
from CosmicKSP.ui.Relay import relayWidget

from .SMDesigner import Ui_SimMainWindow


class simManagerMainWindow(QtWidgets.QMainWindow, Ui_SimMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon.fromTheme('multimedia-player'))

        self.relay_widget = relayWidget(settings.SIM_GAME_INSTANCE)
        self.centralwidget.layout().insertWidget(1, self.relay_widget)

        self.sendCmdBtn.clicked.connect(self.sendCommand)


    def sendCommand(self):
        cmd_text = self.commandEdit.text()
        self.relay_widget.commands_uplink.sendCommandStr(cmd_text)
        self.commandEdit.setText('')
