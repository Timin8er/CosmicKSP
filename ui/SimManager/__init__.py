import os
import shutil
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
        self.transferGameStateBtn.clicked.connect(self.transferQuicksave)


    def sendCommand(self):
        cmd_text = self.commandEdit.text()
        self.relay_widget.commands_uplink.sendCommandStr(cmd_text)
        self.commandEdit.setText('')


    def transferQuicksave(self):
        real_qs  = os.path.join(settings.REAL_GAME_INSTANCE['DIR'], 'saves', settings.REAL_GAME_INSTANCE['GAME_NAME'], 'quicksave.sfs')
        real_qsm = os.path.join(settings.REAL_GAME_INSTANCE['DIR'], 'saves', settings.REAL_GAME_INSTANCE['GAME_NAME'], 'quicksave.loadmeta')

        sim_qs  = os.path.join(settings.SIM_GAME_INSTANCE['DIR'], 'saves', settings.SIM_GAME_INSTANCE['GAME_NAME'], 'quicksave.sfs')
        sim_qsm = os.path.join(settings.SIM_GAME_INSTANCE['DIR'], 'saves', settings.SIM_GAME_INSTANCE['GAME_NAME'], 'quicksave.loadmeta')

        shutil.copyfile(real_qs, sim_qs)
        shutil.copyfile(real_qsm, sim_qsm)
