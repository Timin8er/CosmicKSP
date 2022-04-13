from PyQt5.QtWidgets import QTreeView, QAbstractItemView
from PyQt5.QtCore import QAbstractItemModel, Qt, QModelIndex, QItemSelectionModel
from PyQt5.QtGui import QIcon
import os

from CosmicKSP.ui import icons
from CosmicKSP.core.Commands import *


class commandSequenceTreeView(QTreeView):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.view_model = treeModel(commandSequence)

        self.setModel(self.view_model)
        self.setHeaderHidden(True)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)


    def newCommandSequence(self):
        index = self.selectionModel().currentIndex()

        if index.isValid() and isinstance(index.internalPointer().obj, commandSequence):
            index = index.parent()
            if index.internalPointer().obj is None:
                index = QModelIndex()

        cs = commandSequence()
        cs.name= 'New Sequence'
        self.view_model.addObj(cs, index)


    def removeSelectedCommandSequence(self):
        index = self.selectionModel().currentIndex()
        self.view_model.removeObj(index)


    def newCommandSequenceFolder(self):
        index = self.selectionModel().currentIndex()

        if index.isValid() and isinstance(index.internalPointer().obj, commandSequence):
            index = index.parent()
            if index.internalPointer().obj is None:
                index = QModelIndex()

        new_folder = folderItem('New Folder')
        self.view_model.addObj(new_folder, index)


    def  mousePressEvent(self, event):
        index = self.indexAt(event.pos())
        if not index.isValid():
            self.selectionModel().setCurrentIndex(QModelIndex(), QItemSelectionModel.Select)
            self.clearSelection()

        super().mousePressEvent(event)


    def dragEnterEvent(self, event):
        if event.source() is self and self.view_model.editable:
            self.drag_index = self.currentIndex()
            event.accept()

        else:
            self.parent().dragEnterEvent(event)


    def dropEvent(self, event):
        if event.source() is self:
            dest_index = self.indexAt(event.pos())

            if dest_index.isValid():
                self.model()._moveRow(self.drag_index, dest_index)
            else:
                self.model()._moveRow(self.drag_index, self.rootIndex())



class folderItem():

    def __init__(self, name):
        self.name = name


class treeNode():

    def __init__(self, obj=None):
        self.obj = obj
        self._children = []
        self._parent = None
        self._row = 0


    def childCount(self):
        return len(self._children)


    def child(self, row):
        if row >= 0 and row < self.childCount():
            return self._children[row]


    def parent(self):
        return self._parent


    def row(self):
        return self._row


    def addChild(self, child):
        if not isinstance(child, treeNode):
            child = treeNode(child)

        child._parent = self
        child._row = len(self._children)
        self._children.append(child)


    def removeChild(self, child):
        child._parent = None
        child._row = 0
        self._children.remove(child)


    def genObjs(self, path = None):
        if self.obj is not None and not isinstance(self.obj, folderItem):
            self.obj.folder = path
            yield self.obj

        if self.obj is not None:
            path = os.path.join(path, self.obj.name) if path else self.obj.name

        for c in self._children:
            yield from c.genObjs(path)


class treeModel(QAbstractItemModel):

    def __init__(self, obj_class, *args, **kwargs):
        QAbstractItemModel.__init__(self, *args, **kwargs)

        self._root = treeNode(None)
        self.obj_class = obj_class
        self.editable = True


    def clear(self):
        self.beginResetModel()
        self._root._children = []
        self.endResetModel()


    def load(self, objs=[]):
        self.clear()
        self.beginInsertRows(QModelIndex(), 0, self._root.childCount())

        # add scripts
        for obj in objs:
            folder_node = self.generateFolder(obj.folder)
            folder_node.addChild(obj)

        self.endInsertRows()


    def addObj(self, obj, index):
        if not index.isValid():
            index = QModelIndex()
            par_node = self._root
        else:
            par_node = index.internalPointer()

        row = par_node.childCount()
        self.beginInsertRows(index, row, row)
        par_node.addChild(obj)

        self.endInsertRows()


    def removeObj(self, index):
        parent_index = index.parent()
        self.beginRemoveRows(parent_index, index.row(), index.row())

        node = index.internalPointer()
        node._parent.removeChild(node)

        self.endRemoveRows()


    def generateFolder(self, path):
        if not path:
            return self._root

        dir_node = self._root
        dir_names = path.split(os.sep)
        for dir_name in dir_names:
            for child_node in dir_node._children:
                if isinstance(child.obj, folderItem) and child.obj.name == dir_name:
                    dir_node = child_node
                    break
            else:
                new_folder_node = treeNode(folderItem(dir_name))
                dir_node.addChild(new_folder_node)
                dir_node = new_folder_node

        return dir_node


    def index(self, row, column, _parent):
        if not _parent or not _parent.isValid():
            parent = self._root
        else:
            parent = _parent.internalPointer()

        if not QAbstractItemModel.hasIndex(self, row, column, _parent):
            return QModelIndex()

        child = parent.child(row)
        if child:
            return QAbstractItemModel.createIndex(self, row, column, child)
        else:
            return QModelIndex()


    def flags(self, index):
        if self.editable:
            return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled | Qt.ItemIsSelectable
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable


    def parent(self, index):
        if index.isValid():
            p = index.internalPointer().parent()
            if p:
                return QAbstractItemModel.createIndex(self, p.row(), 0, p)
        return QModelIndex()


    def rowCount(self, index):
        if index.isValid():
            return index.internalPointer().childCount()
        return self._root.childCount()


    def columnCount(self, index):
        return 1


    def data(self, index, role):
        if not index.isValid():
            return None

        obj = index.internalPointer().obj

        if role == Qt.DisplayRole or role == Qt.EditRole:
            return obj.name

        if role == Qt.DecorationRole and isinstance(obj, folderItem):
            return QIcon(icons.FOLDER)


    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            obj = index.internalPointer().obj
            obj.name = value
            return True


    def genObjs(self):
        yield from self._root.genObjs()


    def _moveRow(self, from_index, to_index):

        while to_index.internalPointer().obj is not None and not isinstance(to_index.internalPointer().obj, folderItem):
            to_index = to_index.parent()

        if from_index.parent() is to_index:
            return

        source_node = from_index.internalPointer()
        to_node = to_index.internalPointer()

        self.beginMoveRows(from_index.parent(), from_index.row(), from_index.row(), to_index, to_node.childCount())

        source_node._parent.removeChild(source_node)
        to_node.addChild(source_node)

        self.endMoveRows()
