import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QAbstractListModel, QModelIndex, QItemSelectionModel
from PyQt5.QtGui import QIcon

from CosmicKSP.core.Commands import FLOAT, STRING, ENUM

def generateForm(command, editable):

    form_widget = QtWidgets.QWidget()
    form = QtWidgets.QFormLayout()
    form_widget.setLayout(form)

    for arg in command.arguements:
        if arg.type == FLOAT:
            widget = getFloatWidget(arg)
            widget.setEnabled(editable)

        elif arg.type == STRING:
            widget = getStringWidget(arg)
            widget.setEnabled(editable)

        elif arg.type == ENUM:
            widget = getEnumWidget(arg)
            widget.setEnabled(editable)

        form.addRow(arg.name, widget)

    return form_widget


def getFloatWidget(arg):
    widget = QtWidgets.QDoubleSpinBox()
    widget.setValue(arg.value)
    widget.setRange(-1000000000000000000000000000, sys.float_info.max)
    widget.valueChanged.connect(lambda: setattr(arg, 'value', widget.value()))
    return widget


def getStringWidget(arg):
    widget = QtWidgets.QLineEdit()
    widget.setText(arg.value)
    widget.editingFinished.connect(lambda: setattr(arg, 'value', widget.text()))
    return widget


def getEnumWidget(arg):
    widget = QtWidgets.QComboBox()
    widget.addItems(arg.options)
    widget.setCurrentText(arg.value)
    widget.currentIndexChanged.connect(lambda x: setattr(arg, 'value', widget.currentText()))
    return widget
