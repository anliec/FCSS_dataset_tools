#!/usr/bin/python3
import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
from src.mainwindow import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    if len(sys.argv) > 1:
        file_list = sys.argv[1:]
    else:
        file_list = None

    w = MainWindow(app, file_list)
    w.show()

    sys.exit(app.exec_())
