# coding: utf-8
import sys
from random import randint, sample

from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView

from dicttreemodel import TreeModel

songs = [
    {
        "ID": "1",
        "songs": "Blurred Lines"
    },
    {
        "ID": "2",
        "songs": "Nobody wants to be lonely"
    },
    {
        "ID": "3",
        "songs": "How you remind me"
    },
    {
        "ID": "4",
        "songs": "Knocking on heavens door"
    },
    {
        "ID": "5",
        "songs": "Move to Miami"
    },
    {
        "ID": "6",
        "songs": "Blurred Lines"
    },
    {
        "ID": "7",
        "songs": "Beggin"
    },
    {
        "ID": "8",
        "songs": "Brasil"
    },
    {
        "ID": "9",
        "songs": "Rock this party"
    },
    {
        "ID": "10",
        "songs": "Mambo No. 5"
    }
]


data = {
    "members": [
        {
            "ID": "1",
            "job_title": "Associate Professor",
            "mail": "Barry_Pond247@gompie.com",
            "first_name": "Barry",
            "last_name": "Pond",
            "favorite_songs": sample(songs, k=randint(1, 4))
        },
        {
            "ID": "2",
            "job_title": "Loan Officer",
            "mail": "Fred_Ellis1472@typill.biz",
            "first_name": "Fred",
            "last_name": "Ellis",
            "favorite_songs": sample(songs, k=randint(1, 4))
        },
        {
            "ID": "3",
            "job_title": "Call Center Representative",
            "mail": "Mason_Allcott3362@tonsy.org",
            "first_name": "Mason",
            "last_name": "Allcott",
            "favorite_songs": sample(songs, k=randint(1, 4))
        },
        {
            "ID": "4",
            "job_title": "Electrician",
            "mail": "Ruth_Lloyd9545@deons.tech",
            "first_name": "Ruth",
            "last_name": "Lloyd",
            "favorite_songs": sample(songs, k=randint(1, 4))
        },
        {
            "ID": "5",
            "job_title": "Banker",
            "mail": "Benjamin_Thomson9293@elnee.tech",
            "first_name": "Benjamin",
            "last_name": "Thomson",
            "favorite_songs": sample(songs, k=randint(1, 4))
        },
        {
            "ID": "6",
            "job_title": "Electrician",
            "mail": "Barney_Phillips7310@sveldo.biz",
            "first_name": "Barney",
            "last_name": "Phillips",
            "favorite_songs": sample(songs, k=randint(1, 4))
        },
        {
            "ID": "7",
            "job_title": "Biologist",
            "mail": "Rylee_Woodcock482@extex.org",
            "first_name": "Rylee",
            "last_name": "Woodcock",
            "favorite_songs": sample(songs, k=randint(1, 4))
        },
        {
            "ID": "8",
            "job_title": "Front Desk Coordinator",
            "mail": "Ryan_Exton3112@yahoo.com",
            "first_name": "Ryan",
            "last_name": "Exton",
            "favorite_songs": sample(songs, k=randint(1, 4))
        },
        {
            "ID": "9",
            "job_title": "Auditor",
            "mail": "Tom_Knott1259@fuliss.net",
            "first_name": "Tom",
            "last_name": "Knott",
            "favorite_songs": sample(songs, k=randint(1, 4))
        },
        {
            "ID": "10",
            "job_title": "CNC Operator",
            "mail": "Stacy_Ross987@dionrab.com",
            "first_name": "Stacy",
            "last_name": "Ross",
            "favorite_songs": sample(songs, k=randint(1, 4))
        }
    ]
}


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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = TreeModel(data)
    window = MainWindow(model)
    window.show()
    sys.exit(app.exec_())
