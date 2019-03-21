# coding: utf-8
from collections import Sequence, Mapping, Iterable
from functools import partial

from PyQt5.QtCore import QAbstractItemModel, QModelIndex, Qt


def is_char_sequence(value) -> bool:
    """
    In most instances testing for Sequence or Iterable, these string types are undesirable.
    """
    return isinstance(value, (bytes, bytearray, str))


def is_sequence(value) -> bool:
    """
    Is value a sequence (and also not a string type).
    """
    return isinstance(value, Sequence) and not is_char_sequence(value)


def is_iterable(value) -> bool:
    """
    Is value an iterable (and also not a string or mapping type).
    """
    return (
        isinstance(value, Iterable)
        and not is_char_sequence(value)
        and not isinstance(value, Mapping)
    )


class TreeNode:
    """
    TreeNode adapts Python data types to QTreeModel.

    Provide adapter callables to convert Python types to TreeNode. Comes with
    adapters for Iterable and Mapping. See ref:`TreeNode.adapter` for more.
    """
    class Unacceptable(Exception):
        """
        TreeNode adapters must raise this exception for types they don't handle.
        """
        pass

    adapters = []

    def __init__(self, key, value, parent=None, row=0):
        self.key = key
        self.value = self.adapt(self, value)
        self.parent = parent
        self.row = row

    @property
    def has_children(self):
        return is_sequence(self.value)

    def __len__(self):
        if self.has_children:
            return len(self.value)
        return 1

    def __getitem__(self, idx):
        if self.has_children:
            return self.value[idx]

    def data(self, col):
        if col == 0:
            return self.key
        elif col == 1:
            return self.value

    @classmethod
    def adapt(cls, parent, value):
        for adapter in cls.adapters:
            try:
                return adapter(cls, parent, value)
            except cls.Unacceptable:
                continue
        return value

    @classmethod
    def adapter(cls, fn):
        """
        Decorator to add value-to-TreeNode adapters.
        Adapters must return a list of TreeNode, or must raise
        TreeNode.Unacceptable for types they don't adapt.

        Adapters have a signature of:

        ```python
            def adapter(cls: Type[TreeNode],
                        parent: TreeNode,
                        value: Any) -> Sequence[TreeNode]:
                pass
        ```

        Example adapter for Iterable (builtin):

        ```python
            @TreeNode.adapter
            def iterable_adapter(cls, parent, value):
                if not is_iterable(value):
                    raise cls.Unacceptable()
                return [cls(i, value, parent, i)
                        for i, value in enumerate(value)]
        ```

        Example adapter for Mapping (builtin):

        ```python
            @TreeNode.adapter
            def mapping_adapter(cls, parent, value):
                if not isinstance(value, Mapping):
                    raise cls.Unacceptable()
                return [cls(key, value, parent, i)
                        for i, (key, value) in enumerate(value.items())]
        ```
        """
        cls.adapters.append(fn)
        return fn


@TreeNode.adapter
def iterable_adapter(cls, parent, value):
    """
    TreeNode adapter for Iterable (excluding Mappings and string types).
    """
    if not is_iterable(value):
        raise cls.Unacceptable()
    return [cls(i, item_value, parent, i)
            for i, item_value in enumerate(value)]


@TreeNode.adapter
def mapping_adapter(cls, parent, value):
    """
    TreeNode adapter for Mapping.
    """
    if not isinstance(value, Mapping):
        raise cls.Unacceptable()
    return [cls(item_key, item_value, parent, i)
            for i, (item_key, item_value) in enumerate(value.items())]


class TreeModel(QAbstractItemModel):
    COLUMN_HEADERS = ("Key", "Value")

    def __init__(self, data, parent_widget=None):
        super().__init__(parent_widget)
        self.root = TreeNode("__root__", data, None)

    def check_for_root(self, parent: QModelIndex):
        return self.root if not parent.isValid() else parent.internalPointer()

    def columnCount(self, parent: QModelIndex=None):
        return len(self.COLUMN_HEADERS)

    def headerData(self, section, orient, role=None):
        if orient == Qt.Horizontal and role == Qt.DisplayRole:
            return self.COLUMN_HEADERS[section]

    def rowCount(self, parent: QModelIndex):
        node = self.check_for_root(parent)
        return len(node)

    def index(self, row, col, parent: QModelIndex):
        node = self.check_for_root(parent)
        child = node[row]
        return self.createIndex(row, col, child) if child else QModelIndex()

    def parent(self, index: QModelIndex):
        if not index.isValid():
            return QModelIndex()
        child = index.internalPointer()
        parent = child.parent
        if parent is self.root:
            return QModelIndex()
        return self.createIndex(parent.row, 0, parent)

    def hasChildren(self, parent: QModelIndex):
        node = self.check_for_root(parent)
        return node is not None and node.has_children

    def data(self, index: QModelIndex, role):
        if index.isValid() and role == Qt.DisplayRole:
            node = index.internalPointer()
            return node.data(index.column())
