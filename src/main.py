#!/usr/bin/python3
import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
from src.mainwindow import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = MainWindow(app)

    w.show()

    sys.exit(app.exec_())
