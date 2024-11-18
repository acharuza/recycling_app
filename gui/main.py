import sys
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QLinearGradient, QColor, QPalette, QBrush
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QWidget, QFrame, QFileDialog, QMessageBox, QVBoxLayout
from PyQt5.QtGui import QFont
from ui_function import *
from collections import Counter
import json
import os


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = uic.loadUi("ui_main.ui", self)

        #Setting window title
        applicationName = "Recycle App"
        self.setWindowTitle(applicationName)
        UIFunction.labelTitle(self, applicationName)

        #Initilize stacked widget
        UIFunction.initStackTab(self)

        #Initialize max, min, close of the title bar
        UIFunction.constantFunction(self)

        UIFunction.stackPage(self)

        #Menu buttons
        self.ui.bn_home.clicked.connect(lambda: UIFunction.buttonPressed(self, 'bn_home'))
        self.ui.bn_stats.clicked.connect(lambda: (
            UIFunction.buttonPressed(self, 'bn_stats'),
            UIFunction.statsPage(self)
        ))

        #Used for stacked widgets
        UIFunction.stackPage(self)

        #Used for moving window
        self.dragPos = self.pos()

        def moveWindow(event):
            # if maximized back to normal
            if UIFunction.returnStatus() == 1:
                UIFunction.maximize_restore(self)

            # move window
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()


        self.ui.frame_appname.mouseMoveEvent = moveWindow
        self.ui.bn_load_photo.clicked.connect(lambda: UIFunction.loadPhoto(self))
        self.ui.bn_new.clicked.connect(lambda: UIFunction.loadPhoto(self))
        self.ui.bn_new_2.clicked.connect(lambda: UIFunction.loadPhoto(self))
        self.ui.bn_analyze.clicked.connect(lambda: UIFunction.analyzePhoto(self))
        self.ui.bn_save.clicked.connect(lambda: UIFunction.savePhoto(self))

        


    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
