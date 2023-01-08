import os
import shutil
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QAbstractListModel, QModelIndex
from PyQt5.QtGui import QIcon

from CosmicKSP import settings
from CosmicKSP.ui import icons
from CosmicKSP.core.Commands import *
from relay.ui import relayWidget

from .MPDesigner import Ui_MissionPlannerWindow
from .CommandsList import commandslistView
from .CommandSequencesTree import commandSequenceTreeView
from .ArguementsForm import generateForm


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
        self.actionReconnect.triggered.connect(self.relay_widget.reconnect)

        self.btnSend.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        self.btnStop.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaStop))

        self.btnAddCommandSequence.setIcon(QIcon(icons.NEW))
        self.btnAddCSFolder.setIcon(QIcon(icons.FOLDER))
        self.btnRemoveCommandSequence.setIcon(QIcon(icons.DELETE))

        self.btnAddCommand.setIcon(QIcon(icons.NEW))
        self.btnRemoveCommand.setIcon(QIcon(icons.DELETE))

        self.commands_sequences_view = commandSequenceTreeView(self)
        self.commands_sequences_view.model().load(load_cs())
        self.verticalLayout_3.addWidget(self.commands_sequences_view)

        self.btnAddCommandSequence.clicked.connect(self.commands_sequences_view.newCommandSequence)
        self.btnAddCSFolder.clicked.connect(self.commands_sequences_view.newCommandSequenceFolder)
        self.btnRemoveCommandSequence.clicked.connect(self.commands_sequences_view.removeSelectedCommandSequence)
        self.commands_sequences_view.selectionModel().selectionChanged.connect(self.populateCommands)

        self.commands_view = commandslistView(self)
        self.commandToolsLayout.addWidget(self.commands_view)
        self.btnAddCommand.clicked.connect(self.commands_view.newCommand)
        self.btnRemoveCommand.clicked.connect(self.commands_view.removeSelectedCommands)
        self.commands_view.selectionModel().selectionChanged.connect(self.populateArguements)

        self.arguements_form = None
        self.descriptionLabel.setText('')


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
        save_cs([i for i in self.commands_sequences_view.model().genObjs()])
        QtWidgets.QMessageBox.information(self, 'Saved', 'Command Sequences Saved')


    def populateCommands(self):
        index = self.commands_sequences_view.selectionModel().currentIndex()
        if index.isValid():
            cs = index.internalPointer().obj
            if isinstance(cs, commandSequence):
                self.commands_view.model().load(cs.commands)
                return

        self.commands_view.model().clear()


    def populateArguements(self):
        index = self.commands_view.selectionModel().currentIndex()

        if self.arguements_form is not None:
            self.verticalLayout_2.removeWidget(self.arguements_form)
            self.arguements_form.deleteLater()
            self.arguements_form = None

        if index.isValid():
            command = self.commands_view.model().cmd_list[index.row()]
            self.descriptionLabel.setText(command.description)
            self.commandEdit.setText(command.kosString())
            self.arguements_form = generateForm(command, self.commands_view.model()._editable)
            self.verticalLayout_2.insertWidget(0, self.arguements_form)

        else:
            self.commandEdit.setText('')
            self.descriptionLabel.setText('')
