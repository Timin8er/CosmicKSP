import os
import shutil
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from CosmicKSP import settings
from CosmicKSP.ui.Relay import relayWidget
from CosmicKSP.ui import icons

from .MPDesigner import Ui_MissionPlannerWindow

class missionPlannerMainWindow(QtWidgets.QMainWindow, Ui_MissionPlannerWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(icons.ROCKET))

        self.relay_widget = relayWidget(settings.SIM_GAME_INSTANCE)
        self.centralwidget.layout().insertWidget(1, self.relay_widget)

        self.relay_widget.commandLayout.addWidget(self.cmdSendWidget)

        self.btnSend.clicked.connect(self.sendCommand)
        # self.btnStop.clicked.connect(self.sendStop)
        self.transferGameStateBtn.clicked.connect(self.transferQuicksave)

        self.btnSend.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        self.btnStop.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaStop))

        # self.btnAddCommandList.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        self.btnRemoveCommandList.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DialogDiscardButton))

        # self.btnAddCommand.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        self.btnRemoveCommand.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DialogDiscardButton))


    def sendCommand(self):
        cmd_text = self.commandEdit.text()
        self.relay_widget.commands_uplink.sendCommandStr(cmd_text)
        self.commandEdit.setText('')


    def sendStop(self):
        self.relay_widget.commands_uplink.stop()


    def transferQuicksave(self):
        real_qs  = os.path.join(settings.REAL_GAME_INSTANCE['DIR'], 'saves', settings.REAL_GAME_INSTANCE['GAME_NAME'], 'quicksave.sfs')
        real_qsm = os.path.join(settings.REAL_GAME_INSTANCE['DIR'], 'saves', settings.REAL_GAME_INSTANCE['GAME_NAME'], 'quicksave.loadmeta')

        sim_qs  = os.path.join(settings.SIM_GAME_INSTANCE['DIR'], 'saves', settings.SIM_GAME_INSTANCE['GAME_NAME'], 'quicksave.sfs')
        sim_qsm = os.path.join(settings.SIM_GAME_INSTANCE['DIR'], 'saves', settings.SIM_GAME_INSTANCE['GAME_NAME'], 'quicksave.loadmeta')

        shutil.copyfile(real_qs, sim_qs)
        shutil.copyfile(real_qsm, sim_qsm)
