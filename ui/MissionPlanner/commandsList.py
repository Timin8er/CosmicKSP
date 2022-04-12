from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QAbstractListModel, QModelIndex, QItemSelectionModel
from PyQt5.QtGui import QIcon

from CosmicKSP.core.Commands import *


class commandslistView(QtWidgets.QListView):

    def __init__(self, parent):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        # self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.commands_view_model = commandListViewModel()
        self.commands_view_model.editable = False
        self.setModel(self.commands_view_model)


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
        index = self.selectionModel().currentIndex()
        if index.isValid():
            self.commands_view_model.cmd_list.pop(index.row())
            self.commands_view_model.removeRows(index.row(), 1)


    def  mousePressEvent(self, event):
        index = self.indexAt(event.pos())
        if not index.isValid():
            self.selectionModel().setCurrentIndex(QModelIndex(), QItemSelectionModel.Select)
            self.clearSelection()

        super().mousePressEvent(event)


    def dragEnterEvent(self, event):
        if event.source() is self:
            self.drag_index = self.currentIndex()
            event.accept()

        else:
            self.parent().dragEnterEvent(event)


    def dropEvent(self, event):
        if event.source() is self:
            dest_index = self.indexAt(event.pos())

            if dest_index.isValid():
                self.model()._moveRow(self.drag_index.row(), dest_index.row())
            else:
                self.model()._moveRow(self.drag_index.row(), -1)



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
            return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled | Qt.ItemIsSelectable
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable


    def insertRows(self, row, count, parent=QModelIndex()):
        self.beginInsertRows(parent, row, count)
        self.endInsertRows()


    def removeRows(self, row, count, parent=QModelIndex()):
        self.beginRemoveRows(parent, row, count)
        self.endRemoveRows()


    def _moveRow(self, from_index, to_index):
        obj = self.cmd_list[from_index]

        if to_index < 0:
            to_index = len(self.cmd_list) - 1

        self.cmd_list.remove(obj)
        self.removeRows(from_index, 1)

        self.cmd_list.insert(to_index, obj)
        self.insertRows(to_index, 1)
