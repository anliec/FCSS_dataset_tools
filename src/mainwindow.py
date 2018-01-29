from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from ui.ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__()
        # setup ui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

