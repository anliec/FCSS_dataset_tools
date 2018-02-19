# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(696, 414)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lb_image1 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_image1.sizePolicy().hasHeightForWidth())
        self.lb_image1.setSizePolicy(sizePolicy)
        self.lb_image1.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_image1.setObjectName("lb_image1")
        self.horizontalLayout.addWidget(self.lb_image1)
        self.lb_image2 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_image2.sizePolicy().hasHeightForWidth())
        self.lb_image2.setSizePolicy(sizePolicy)
        self.lb_image2.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_image2.setObjectName("lb_image2")
        self.horizontalLayout.addWidget(self.lb_image2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pb_diff = QtWidgets.QPushButton(self.centralwidget)
        self.pb_diff.setObjectName("pb_diff")
        self.horizontalLayout_2.addWidget(self.pb_diff)
        self.pb_s1 = QtWidgets.QPushButton(self.centralwidget)
        self.pb_s1.setObjectName("pb_s1")
        self.horizontalLayout_2.addWidget(self.pb_s1)
        self.pb_s2 = QtWidgets.QPushButton(self.centralwidget)
        self.pb_s2.setObjectName("pb_s2")
        self.horizontalLayout_2.addWidget(self.pb_s2)
        self.pb_s3 = QtWidgets.QPushButton(self.centralwidget)
        self.pb_s3.setObjectName("pb_s3")
        self.horizontalLayout_2.addWidget(self.pb_s3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 696, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionOpen_pairs_files = QtWidgets.QAction(MainWindow)
        self.actionOpen_pairs_files.setObjectName("actionOpen_pairs_files")
        self.menuFile.addAction(self.actionOpen_pairs_files)
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lb_image1.setText(_translate("MainWindow", "image 1"))
        self.lb_image2.setText(_translate("MainWindow", "image 2"))
        self.pb_diff.setText(_translate("MainWindow", "Different [0]"))
        self.pb_s1.setText(_translate("MainWindow", "Similar ++ [1]"))
        self.pb_s2.setText(_translate("MainWindow", "Similar + [2]"))
        self.pb_s3.setText(_translate("MainWindow", "Similar [3]"))
        self.menuFile.setTitle(_translate("MainWindow", "Fi&le"))
        self.actionQuit.setText(_translate("MainWindow", "&Quit"))
        self.actionOpen_pairs_files.setText(_translate("MainWindow", "&Open pairs files"))

