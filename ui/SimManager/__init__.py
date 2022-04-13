import os
import shutil
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from CosmicKSP import settings
from CosmicKSP.ui.Relay import relayWidget

from .SMDesigner import Ui_SimMainWindow
from CosmicKSP.ui.MissionPlanner import missionPlannerMainWindow


class simManagerMainWindow(missionPlannerMainWindow):

    def __init__(self):
        super().__init__()

        self.actionSave.setEnabled(False)
        self.btnAddCommandSequence.setEnabled(False)
        self.btnAddCSFolder.setEnabled(False)
        self.btnRemoveCommandSequence.setEnabled(False)
        self.btnAddCommand.setEnabled(False)
        self.btnRemoveCommand.setEnabled(False)

        self.commands_sequences_view.view_model.editable = False
        self.commands_view.view_model._editable = False
