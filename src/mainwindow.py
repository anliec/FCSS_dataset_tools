from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import pandas as pd

from ui.ui_mainwindow import Ui_MainWindow

from src.pair_reader import load_files

BASE_IMAGE_PATH = "/cs-share/pradalier/lake/VBags/"
OUT_FILE = "pair.csv"


class MainWindow(QMainWindow):

    images_marked = pyqtSignal()
    images_displayed = pyqtSignal()
    images_loaded = pyqtSignal()

    def __init__(self, parent=None, file_list=None):
        super().__init__()
        # setup ui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.centralwidget.setEnabled(False)
        self.change_button_state(False)
        # attributes
        self.marked_dict = {}
        self.counter_dict = {0: 0, 1: 0, 2: 0, 3: 0}
        self.df = None
        self.image1_path = ""
        self.image2_path = ""
        self.next_image1_path = ""
        self.next_image2_path = ""
        self.next_pixmap1 = None
        self.next_pixmap2 = None
        self.file_dialog = QFileDialog(self, "Pairs file to use", "/cs-share/pradalier/lake/view_set", "poses_*_*.txt")
        self.file_dialog.setFileMode(QFileDialog.ExistingFiles)
        self.shortcut_0 = QShortcut(QKeySequence('0'), self)
        self.shortcut_1 = QShortcut(QKeySequence('1'), self)
        self.shortcut_2 = QShortcut(QKeySequence('2'), self)
        self.shortcut_3 = QShortcut(QKeySequence('3'), self)
        # connections
        self.ui.actionOpen_pairs_files.triggered.connect(self.open_file_dialog)
        self.ui.actionQuit.triggered.connect(self.close)
        self.file_dialog.filesSelected.connect(self.on_file_selected)
        self.file_dialog.finished.connect(self.on_file_dialog_closed)
        self.ui.pb_diff.clicked.connect(lambda: self.write_pair(0))
        self.ui.pb_s1.clicked.connect(lambda: self.write_pair(1))
        self.ui.pb_s2.clicked.connect(lambda: self.write_pair(2))
        self.ui.pb_s3.clicked.connect(lambda: self.write_pair(3))
        self.shortcut_0.activated.connect(lambda: self.write_pair(0))
        self.shortcut_1.activated.connect(lambda: self.write_pair(1))
        self.shortcut_2.activated.connect(lambda: self.write_pair(2))
        self.shortcut_3.activated.connect(lambda: self.write_pair(3))
        self.images_displayed.connect(self.load_random_pair)
        self.images_marked.connect(self.display_new_pair)
        self.images_marked.connect(self.update_status_bar_message)
        # load parameters if given
        if file_list is not None:
            self.load_data(file_list)
        with open(OUT_FILE, 'r') as out:
            df = pd.read_csv(out,
                             sep=',',
                             comment='%',
                             header=None)
            for im1, im2, mark in zip(df.get(0), df.get(1), df.get(2)):
                self.marked_dict[(im1, im2)] = True
                self.counter_dict[mark] += 1
        self.update_status_bar_message()

    def change_button_state(self, enabled):
        self.ui.pb_diff.setEnabled(enabled)
        self.ui.pb_s1.setEnabled(enabled)
        self.ui.pb_s2.setEnabled(enabled)
        self.ui.pb_s3.setEnabled(enabled)

    def load_data(self, file_list):
        self.df = load_files(file_list)
        if len(self.df) > 0:
            self.ui.centralwidget.setEnabled(True)
            self.load_random_pair()
            self.display_new_pair()
        else:
            self.ui.centralwidget.setEnabled(False)

    def open_file_dialog(self):
        self.file_dialog.show()
        self.setEnabled(False)

    def on_file_selected(self):
        file_list = self.file_dialog.selectedFiles()
        self.load_data(file_list)

    def on_file_dialog_closed(self):
        self.setEnabled(True)

    def load_random_pair(self):
        while True:
            line = self.df.sample(n=1)
            self.next_image1_path = BASE_IMAGE_PATH + "%d/%.4d/%.4d.jpg" % (line.get('date1'), line.get('dir1'), line.get('file1'))
            self.next_image2_path = BASE_IMAGE_PATH + "%d/%.4d/%.4d.jpg" % (line.get('date2'), line.get('dir2'), line.get('file2'))
            # if picture pair is not already marked, break the loop
            if (self.next_image1_path, self.next_image2_path) not in self.marked_dict \
                    and (self.next_image2_path, self.next_image1_path) not in self.marked_dict:
                break
        self.next_pixmap1 = QPixmap(self.next_image1_path)
        self.next_pixmap1 = self.next_pixmap1.scaled(self.ui.lb_image1.size(), Qt.KeepAspectRatio)
        self.next_pixmap2 = QPixmap(self.next_image2_path)
        self.next_pixmap2 = self.next_pixmap2.scaled(self.ui.lb_image2.size(), Qt.KeepAspectRatio)
        self.images_loaded.emit()

    def display_new_pair(self):
        self.image1_path = self.next_image1_path
        self.image2_path = self.next_image2_path
        self.ui.lb_image1.setPixmap(self.next_pixmap1)
        self.ui.lb_image2.setPixmap(self.next_pixmap2)
        self.change_button_state(True)
        self.images_displayed.emit()

    @pyqtSlot(int)
    def write_pair(self, mark):
        with open(OUT_FILE, 'a') as out:
            self.change_button_state(False)
            out.write(self.image1_path + ", " + self.image2_path + ", " + str(mark) + '\n')
            self.marked_dict[(self.image1_path, self.image2_path)] = True
            self.counter_dict[mark] += 1
            self.images_marked.emit()

    def update_status_bar_message(self):
        message = "Images Discarded: " + str(self.counter_dict[0]) + " - Very Good: " + str(self.counter_dict[1])
        message += " - Good: " + str(self.counter_dict[1]) + " - Correct: " + str(self.counter_dict[2])
        self.ui.statusbar.showMessage(message)
