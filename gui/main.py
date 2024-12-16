import sys
import matplotlib
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QLinearGradient, QColor, QPalette, QBrush
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QWidget, QFrame, QFileDialog, QMessageBox, \
    QVBoxLayout
from PyQt5.QtGui import QFont
from ui_function import *
from collections import Counter
from datetime import datetime
import random
import json
import os


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = uic.loadUi("ui_main.ui", self)

        # Setting window title
        application_name = "Recycle App"
        self.setWindowTitle(application_name)
        UIFunction.label_title(self, application_name)

        # Initilize stacked widget
        UIFunction.init_stack_tab(self)

        # Initialize max, min, close of the title bar
        UIFunction.constant_function(self)

        UIFunction.stats_page(self)

        # Menu buttons
        self.ui.bn_home.clicked.connect(lambda: UIFunction.button_pressed(self, 'bn_home'))
        self.ui.bn_stats.clicked.connect(lambda: UIFunction.button_pressed(self, 'bn_stats'))

        # Used for stacked widgets
        UIFunction.stack_page(self)

        # Used for moving window
        self.dragPos = self.pos()

        def move_window(event):
            # if maximized back to normal
            if UIFunction.return_status() == 1:
                UIFunction.maximize_restore(self)

            # move window
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()


        # buttons
        self.ui.bn_report.setVisible(False)
        self.ui.bn_like.setVisible(False)
        self.ui.frame_appname.mouseMoveEvent = move_window
        self.ui.bn_load_photo.clicked.connect(lambda: UIFunction.load_photo(self))
        self.ui.bn_new.clicked.connect(lambda: UIFunction.load_photo(self))
        self.ui.bn_new_2.clicked.connect(lambda: UIFunction.load_photo(self))
        self.ui.bn_analyze.clicked.connect(lambda: UIFunction.waste_category(self))
        self.ui.bn_save.clicked.connect(lambda: UIFunction.save_photo(self))
        self.ui.bn_like.clicked.connect(lambda: UIFunction.send_positive_feedback(self))
        self.ui.bn_report.clicked.connect(lambda: UIFunction.choose_feedback(self))
        self.ui.bn_send.clicked.connect(lambda: UIFunction.send_negative_feedback(self))
        self.ui.bn_back.clicked.connect(lambda: UIFunction.desc_view(self))
        #self.ui.bn_sort.clicked.connect(lambda: UIFunction.toggleSortMode(self))


    def mouse_press_event(self, event):
        self.dragPos = event.globalPos()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
