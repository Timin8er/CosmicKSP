# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Projects\CosmicKSP\ui\MissionPlanner\MPDesigner.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MissionPlannerWindow(object):
    def setupUi(self, MissionPlannerWindow):
        MissionPlannerWindow.setObjectName("MissionPlannerWindow")
        MissionPlannerWindow.resize(900, 600)
        self.centralwidget = QtWidgets.QWidget(MissionPlannerWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.cmdSendWidget = QtWidgets.QWidget(self.centralwidget)
        self.cmdSendWidget.setObjectName("cmdSendWidget")
        self.cmdLayout = QtWidgets.QHBoxLayout(self.cmdSendWidget)
        self.cmdLayout.setObjectName("cmdLayout")
        self.commandEdit = QtWidgets.QLineEdit(self.cmdSendWidget)
        self.commandEdit.setObjectName("commandEdit")
        self.cmdLayout.addWidget(self.commandEdit)
        self.btnSend = QtWidgets.QPushButton(self.cmdSendWidget)
        self.btnSend.setText("")
        icon = QtGui.QIcon.fromTheme("media-playback-start")
        self.btnSend.setIcon(icon)
        self.btnSend.setObjectName("btnSend")
        self.cmdLayout.addWidget(self.btnSend)
        self.btnStop = QtWidgets.QPushButton(self.cmdSendWidget)
        self.btnStop.setText("")
        icon = QtGui.QIcon.fromTheme("media-playback-stop")
        self.btnStop.setIcon(icon)
        self.btnStop.setObjectName("btnStop")
        self.cmdLayout.addWidget(self.btnStop)
        self.verticalLayout.addWidget(self.cmdSendWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.commandSequencesGB = QtWidgets.QGroupBox(self.centralwidget)
        self.commandSequencesGB.setObjectName("commandSequencesGB")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.commandSequencesGB)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btnAddCommandSequence = QtWidgets.QToolButton(self.commandSequencesGB)
        icon = QtGui.QIcon.fromTheme("list-add")
        self.btnAddCommandSequence.setIcon(icon)
        self.btnAddCommandSequence.setObjectName("btnAddCommandSequence")
        self.horizontalLayout_3.addWidget(self.btnAddCommandSequence)
        self.btnAddCSFolder = QtWidgets.QToolButton(self.commandSequencesGB)
        self.btnAddCSFolder.setText("")
        self.btnAddCSFolder.setObjectName("btnAddCSFolder")
        self.horizontalLayout_3.addWidget(self.btnAddCSFolder)
        self.btnRemoveCommandSequence = QtWidgets.QToolButton(self.commandSequencesGB)
        icon = QtGui.QIcon.fromTheme("list-remove")
        self.btnRemoveCommandSequence.setIcon(icon)
        self.btnRemoveCommandSequence.setObjectName("btnRemoveCommandSequence")
        self.horizontalLayout_3.addWidget(self.btnRemoveCommandSequence)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout.addWidget(self.commandSequencesGB)
        self.commandsGB = QtWidgets.QGroupBox(self.centralwidget)
        self.commandsGB.setObjectName("commandsGB")
        self.commandToolsLayout = QtWidgets.QVBoxLayout(self.commandsGB)
        self.commandToolsLayout.setObjectName("commandToolsLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.btnAddCommand = QtWidgets.QToolButton(self.commandsGB)
        icon = QtGui.QIcon.fromTheme("list-add")
        self.btnAddCommand.setIcon(icon)
        self.btnAddCommand.setObjectName("btnAddCommand")
        self.horizontalLayout_4.addWidget(self.btnAddCommand)
        self.btnRemoveCommand = QtWidgets.QToolButton(self.commandsGB)
        icon = QtGui.QIcon.fromTheme("list-remove")
        self.btnRemoveCommand.setIcon(icon)
        self.btnRemoveCommand.setObjectName("btnRemoveCommand")
        self.horizontalLayout_4.addWidget(self.btnRemoveCommand)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.commandToolsLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout.addWidget(self.commandsGB)
        self.arguementsGB = QtWidgets.QGroupBox(self.centralwidget)
        self.arguementsGB.setObjectName("arguementsGB")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.arguementsGB)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.scrollArea = QtWidgets.QScrollArea(self.arguementsGB)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 267, 456))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_4.addWidget(self.scrollArea)
        self.horizontalLayout.addWidget(self.arguementsGB)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MissionPlannerWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MissionPlannerWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 900, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSim_State = QtWidgets.QMenu(self.menubar)
        self.menuSim_State.setObjectName("menuSim_State")
        MissionPlannerWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MissionPlannerWindow)
        self.statusbar.setObjectName("statusbar")
        MissionPlannerWindow.setStatusBar(self.statusbar)
        self.actionSave = QtWidgets.QAction(MissionPlannerWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionCopy_QuickSave = QtWidgets.QAction(MissionPlannerWindow)
        self.actionCopy_QuickSave.setObjectName("actionCopy_QuickSave")
        self.actionOther = QtWidgets.QAction(MissionPlannerWindow)
        self.actionOther.setObjectName("actionOther")
        self.menuFile.addAction(self.actionSave)
        self.menuSim_State.addAction(self.actionCopy_QuickSave)
        self.menuSim_State.addAction(self.actionOther)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSim_State.menuAction())

        self.retranslateUi(MissionPlannerWindow)
        QtCore.QMetaObject.connectSlotsByName(MissionPlannerWindow)

    def retranslateUi(self, MissionPlannerWindow):
        _translate = QtCore.QCoreApplication.translate
        MissionPlannerWindow.setWindowTitle(_translate("MissionPlannerWindow", "Cosmic KSP Sim Manager"))
        self.commandEdit.setPlaceholderText(_translate("MissionPlannerWindow", "Command"))
        self.commandSequencesGB.setTitle(_translate("MissionPlannerWindow", "Command Sequences"))
        self.btnAddCommandSequence.setText(_translate("MissionPlannerWindow", "+"))
        self.btnRemoveCommandSequence.setText(_translate("MissionPlannerWindow", "-"))
        self.commandsGB.setTitle(_translate("MissionPlannerWindow", "Commands"))
        self.btnAddCommand.setText(_translate("MissionPlannerWindow", "+"))
        self.btnRemoveCommand.setText(_translate("MissionPlannerWindow", "-"))
        self.arguementsGB.setTitle(_translate("MissionPlannerWindow", "Arguements"))
        self.menuFile.setTitle(_translate("MissionPlannerWindow", "File"))
        self.menuSim_State.setTitle(_translate("MissionPlannerWindow", "Sim State"))
        self.actionSave.setText(_translate("MissionPlannerWindow", "Save"))
        self.actionSave.setShortcut(_translate("MissionPlannerWindow", "Ctrl+S"))
        self.actionCopy_QuickSave.setText(_translate("MissionPlannerWindow", "Copy QuickSave"))
        self.actionOther.setText(_translate("MissionPlannerWindow", "Other"))
