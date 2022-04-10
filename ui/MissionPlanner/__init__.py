import os
import shutil
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QAbstractListModel, QModelIndex
from PyQt5.QtGui import QIcon

from CosmicKSP import settings
from CosmicKSP.ui.Relay import relayWidget
from CosmicKSP.ui import icons
from CosmicKSP.core.Commands import commandSequence, command, commandArgument

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

        # self.btnAddCommandSequence.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        self.btnRemoveCommandSequence.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DialogDiscardButton))

        # self.btnAddCommand.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        self.btnRemoveCommand.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DialogDiscardButton))

        self.commandSequencesView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection);

        self.command_sequences_view_model = commandSequenceViewModel()
        self.btnAddCommandSequence.clicked.connect(self.command_sequences_view_model.newCommandList)
        self.btnRemoveCommandSequence.clicked.connect(self.removeSelectedCommandSequence)
        self.commandSequencesView.setModel(self.command_sequences_view_model)


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


    def removeSelectedCommandSequence(self):
        index = self.commandSequencesView.selectionModel().currentIndex()
        if index.isValid():
            self.command_sequences_view_model.removeRows(index.row(), 1)




class commandSequenceViewModel(QAbstractListModel):

    def __init__(self):
        super().__init__()
        self.cl_list = []
        self.editable = True

    def newCommandList(self):
        new_cl = commandSequence()
        new_cl.name = "new sequence"
        self.cl_list.append(new_cl)
        self.insertRows(len(self.cl_list)-1, 1)

    def rowCount(self, parent=QModelIndex()):
        return len(self.cl_list)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self.cl_list[index.row()].name

    def setData(self, index, value, role=Qt.EditRole):

        if role == Qt.EditRole:
            self.cl_list[index.row()].name = value
            return True

    def flags(self, index):
        if self.editable:
            return Qt.ItemIsEditable | Qt.ItemIsEnabled
        else:
            return Qt.ItemIsEnabled

    def insertRows(self, row, count, parent=QModelIndex()):
        self.beginInsertRows(parent, row, row)

        self.endInsertRows()

    def removeRows(self, row, count, parent=QModelIndex()):
        self.beginRemoveRows(parent, row, row)
        self.cl_list.pop(row)
        self.endRemoveRows()
