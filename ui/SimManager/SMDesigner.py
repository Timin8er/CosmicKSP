# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SMDesigner.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SimMainWindow(object):
    def setupUi(self, SimMainWindow):
        SimMainWindow.setObjectName("SimMainWindow")
        SimMainWindow.resize(718, 364)
        self.centralwidget = QtWidgets.QWidget(SimMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.headerLayout = QtWidgets.QHBoxLayout()
        self.headerLayout.setObjectName("headerLayout")
        self.transferGameStateBtn = QtWidgets.QPushButton(self.centralwidget)
        self.transferGameStateBtn.setObjectName("transferGameStateBtn")
        self.headerLayout.addWidget(self.transferGameStateBtn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.headerLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.headerLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.commandEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.commandEdit.setObjectName("commandEdit")
        self.horizontalLayout.addWidget(self.commandEdit)
        self.sendCmdBtn = QtWidgets.QPushButton(self.centralwidget)
        self.sendCmdBtn.setObjectName("sendCmdBtn")
        self.horizontalLayout.addWidget(self.sendCmdBtn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        SimMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(SimMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 718, 21))
        self.menubar.setObjectName("menubar")
        SimMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(SimMainWindow)
        self.statusbar.setObjectName("statusbar")
        SimMainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(SimMainWindow)
        QtCore.QMetaObject.connectSlotsByName(SimMainWindow)

    def retranslateUi(self, SimMainWindow):
        _translate = QtCore.QCoreApplication.translate
        SimMainWindow.setWindowTitle(_translate("SimMainWindow", "Cosmic KSP Sim Manager"))
        self.transferGameStateBtn.setText(_translate("SimMainWindow", "Transfer Game State"))
        self.label.setText(_translate("SimMainWindow", "Command:"))
        self.sendCmdBtn.setText(_translate("SimMainWindow", "Send"))
