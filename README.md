# dict-treemodel-qt5

A QT5 TreeModel to display nested dict, list and other Python types in a
QTreeView.

## Example

```python
# coding: utf-8
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView
from dicttreemodel import TreeModel


class MainWindow(QMainWindow):
    def __init__(self, model):
        super().__init__()
        self.setWindowTitle("Treeview for nested dict/list")
        self.setGeometry(300, 300, 600, 800)
        tree_view = QTreeView()
        tree_view.setModel(model)
        tree_view.expandAll()
        tree_view.resizeColumnToContents(0)
        self.setCentralWidget(tree_view)


data = {
    "students": [
        {
            "id": 1,
            "first_name": "Alex",
            "last_name": "Alligator",
            "courses": [
                {
                    "id": "CS010",
                    "title": "Computer Sciences Introduction"
                },
                {
                    "id": "MTH010",
                    "title": "Math Introduction"
                }
            ]
        }
    ]
}

if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = TreeModel(data)
    window = MainWindow(model)
    window.show()
    sys.exit(app.exec_())
```

## Example adapter

Define two new classes and define an adapter that creates TreeNodes for both.

Given some models in `model.py`:

```python
from dataclasses import dataclass

@dataclass
class Course:
    id: str
    title: str

@dataclass
class Student:
    id: int
    first_name: str
    last_name: str
    courses: list
```

Define TreeNode adapters for the models:

```python
from model import Course, Student
from dicttreemodel import TreeNode

course_attrs = ("id", "title")
student_attrs = ("id", "first_name", "last_name", "courses")
    
@TreeNode.adapter
def course_model_adapter(cls, parent, value):
    if not isinstance(value, Course):
        raise cls.Unacceptable()
    return [cls(attr, getattr(value, attr), parent, i)
        for i, attr in enumerate(course_attrs)]

@TreeNode.adapter
def student_model_adapter(cls, parent, value):
    if not isinstance(value, Student):
        raise cls.Unacceptable()
    return [cls(attr, getattr(value, attr), parent, i)
        for i, attr in enumerate(student_attrs)]
```

Since dataclasses are used, it's possible to write a more generic adapter and
fall back to the builtin Mapping adapter since dataclass instances can be
converted to dict.

```python
from dataclasses import asdict, is_dataclass
from dicttreemodel import TreeNode

@TreeNode.adapter
def dataclass_adapter(cls, parent, value):
    if not is_dataclass(value):
        raise cls.Unacceptable()
    return cls.adapt(parent, asdict(value))
```
