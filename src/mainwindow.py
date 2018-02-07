from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from pandas import *

from ui.ui_mainwindow import Ui_MainWindow

from src.pair_reader import load_files


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__()
        # setup ui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # attributes
        self.df = None
        self.file_dialog = QFileDialog(self, "Pairs file to use", "/cs-share/pradalier/lake/", ".csv")
        self.file_dialog.setFileMode(QFileDialog.ExistingFiles)

    def load_data(self, file_list):
        self.df = load_files(file_list)

    def open_file_dialog(self):
        self.file_dialog.show()
        self.setEnabled(False)

    def on_file_dialog_closed(self):
        file_list = self.file_dialog.selectedFiles()
        self.file_dialog.close()
        self.load_data(file_list)
        self.setEnabled(True)

