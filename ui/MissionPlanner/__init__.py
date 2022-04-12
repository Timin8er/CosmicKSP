import os
import shutil
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QAbstractListModel, QModelIndex
from PyQt5.QtGui import QIcon

from CosmicKSP import settings
from CosmicKSP.ui.Relay import relayWidget
from CosmicKSP.ui import icons
from CosmicKSP.core.Commands import *

from .MPDesigner import Ui_MissionPlannerWindow
from .commandSequencesTreeModel import treeModel, folderItem


class missionPlannerMainWindow(QtWidgets.QMainWindow, Ui_MissionPlannerWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(icons.ROCKET))

        self.relay_widget = relayWidget(settings.SIM_GAME_INSTANCE)
        self.centralwidget.layout().insertWidget(1, self.relay_widget)

        self.relay_widget.commandLayout.addWidget(self.cmdSendWidget)

        self.btnSend.clicked.connect(self.sendCommand)
        self.btnStop.clicked.connect(self.sendStop)
        self.actionCopy_QuickSave.triggered.connect(self.copyQuickSave)
        self.actionOther.triggered.connect(self.copyOtherState)
        self.actionSave.triggered.connect(self.saveCommandSequences)
        self.actionSave.setIcon(QIcon(icons.SAVE))

        self.btnSend.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        self.btnStop.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaStop))

        self.btnAddCommandSequence.setIcon(QIcon(icons.NEW))
        self.btnAddCSFolder.setIcon(QIcon(icons.FOLDER))
        self.btnRemoveCommandSequence.setIcon(QIcon(icons.DELETE))

        self.btnAddCommand.setIcon(QIcon(icons.NEW))
        self.btnRemoveCommand.setIcon(QIcon(icons.DELETE))

        self.command_sequences_view_model = treeModel(commandSequence)
        self.command_sequences_view_model.load(load_cs())
        self.btnAddCommandSequence.clicked.connect(self.newCommandSequence)
        self.btnAddCSFolder.clicked.connect(self.newCommandSequenceFolder)
        self.btnRemoveCommandSequence.clicked.connect(self.removeSelectedCommandSequence)

        self.commandSequencesView.setModel(self.command_sequences_view_model)
        self.commandSequencesView.setHeaderHidden(True)
        self.commandSequencesView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.commandSequencesView.selectionModel().selectionChanged.connect(self.populateCommands)

        self.commands_view_model = commandListViewModel()
        self.commands_view_model.editable = False
        self.btnAddCommand.clicked.connect(self.newCommand)
        self.btnRemoveCommand.clicked.connect(self.removeSelectedCommands)

        self.commandsView.setModel(self.commands_view_model)
        self.commandsView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.commandsView.selectionModel().selectionChanged.connect(self.populateArguements)


    def sendCommand(self):
        cmd_text = self.commandEdit.text()
        self.relay_widget.commands_uplink.sendCommandStr(cmd_text)
        self.commandEdit.setText('')


    def sendStop(self):
        self.relay_widget.commands_uplink.stop()


    def copyGameState(self, from_instance, to_instance, from_file_name, to_file_name):
        from_p  = os.path.join(from_instance['DIR'], 'saves', from_instance['GAME_NAME'], f'{from_file_name}.sfs')
        from_pm = os.path.join(from_instance['DIR'], 'saves', from_instance['GAME_NAME'], f'{from_file_name}.loadmeta')

        to_p  = os.path.join(to_instance['DIR'], 'saves', to_instance['GAME_NAME'], f'{to_file_name}.sfs')
        to_pm = os.path.join(to_instance['DIR'], 'saves', to_instance['GAME_NAME'], f'{to_file_name}.loadmeta')

        shutil.copyfile(from_p, to_p)
        shutil.copyfile(from_pm, to_pm)


    def copyQuickSave(self):
        self.copyGameState(settings.REAL_GAME_INSTANCE, settings.SIM_GAME_INSTANCE, 'quicksave', 'quicksave')


    def copyOtherState(self):
        options = [i for i in os.listdir(os.path.join(settings.REAL_GAME_INSTANCE['DIR'], 'saves', settings.REAL_GAME_INSTANCE['GAME_NAME'])) if i.endswith('sfs')]
        option, yes = QtWidgets.QInputDialog.getItem(self, 'Select State', '', options)
        if yes:
            option = option[:-4]
            self.copyGameState(settings.REAL_GAME_INSTANCE, settings.SIM_GAME_INSTANCE, option, option)


    def saveCommandSequences(self):
        save_cs([i for i in self.command_sequences_view_model.genObjs()])
        QtWidgets.QMessageBox.information(self, 'Saved', 'Command Sequences Saved')


    def newCommandSequence(self):
        index = self.commandSequencesView.selectionModel().currentIndex()

        if index.isValid() and isinstance(index.internalPointer().obj, commandSequence):
            index = index.parent()
            if index.internalPointer().obj is None:
                index = QModelIndex()

        cs = commandSequence()
        cs.name= 'New Sequence'
        self.command_sequences_view_model.addObj(cs, index)


    def removeSelectedCommandSequence(self):
        index = self.commandSequencesView.selectionModel().currentIndex()
        self.command_sequences_view_model.removeObj(index)
        self.populateCommands()


    def newCommandSequenceFolder(self):
        index = self.commandSequencesView.selectionModel().currentIndex()

        if index.isValid() and isinstance(index.internalPointer().obj, commandSequence):
            index = index.parent()
            if index.internalPointer().obj is None:
                index = QModelIndex()

        new_folder = folderItem('New Folder')
        self.command_sequences_view_model.addObj(new_folder, index)


    def newCommand(self):
        options = [i['name'] for i in COMMANDS]
        option, yes = QtWidgets.QInputDialog.getItem(self, 'Select Command', '', options)

        if yes:
            for cmd in COMMANDS:
                if cmd['name'] == option:
                    self.commands_view_model.appendCommand(cmd)
                    break


    def removeSelectedCommands(self):
        # TODO: delete all selected
        index = self.commandsView.selectionModel().currentIndex()
        if index.isValid():
            self.commands_view_model.cmd_list.pop(index.row())
            self.commands_view_model.removeRows(index.row(), 1)


    def populateCommands(self):
        index = self.commandSequencesView.selectionModel().currentIndex()
        if index.isValid():
            cs = index.internalPointer().obj
            if isinstance(cs, commandSequence):
                self.commands_view_model.load(cs.commands)
                self.commands_view_model.editable = True
                return

        self.commands_view_model.clear()
        self.commands_view_model.editable = False


    def populateArguements(self):
        index = self.commandsView.selectionModel().currentIndex()
        if index.isValid():
            cs = self.commands_view_model.cmd_list[index.row()]
            self.commandEdit.setText(cs.kosString())



class commandListViewModel(QAbstractListModel):

    def __init__(self):
        super().__init__()
        self.cmd_list = []
        self.editable = True

    def clear(self):
        self.beginResetModel()
        self.cmd_list = []
        self.endResetModel()

    def load(self, lst):
        self.beginResetModel()
        self.cmd_list = lst
        self.endResetModel()

    def appendCommand(self, cmd):
        self.cmd_list.append(command(cmd))
        self.insertRows(len(self.cmd_list)-1, 1)

    def rowCount(self, parent=QModelIndex()):
        return len(self.cmd_list)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return self.cmd_list[index.row()].name

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            self.cmd_list[index.row()].name = value
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
        self.endRemoveRows()
