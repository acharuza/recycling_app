import sys
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QWidget, QFrame

from ui_function import *


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

        #Menu buttons
        self.ui.bn_home.clicked.connect(lambda: UIFunction.buttonPressed(self, 'bn_home'))
        self.ui.bn_stats.clicked.connect(lambda: UIFunction.buttonPressed(self, 'bn_stats'))

        #Used for stacked widgets
        UIFunction.stackPage(self)

        # ---> MOVING THE WINDOW WHEN LEFT MOUSE PRESSED AND DRAGGED OVER APPNAME LABEL
        # SAME TO SAY AS IN COMMENT (C2)
        self.dragPos = self.pos()

        def moveWindow(event):
            # IF MAXIMIZED CHANGE TO NORMAL
            if UIFunction.returnStatus() == 1:
                UIFunction.maximize_restore(self)

            # MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        # WIDGET TO MOVE: WE CHOOSE THE TOPMOST FRAME WHERE THE APPLICATION NAME IS PRESENT AS THE AREA TO MOVE THE WINDOW.
        self.ui.frame_appname.mouseMoveEvent = moveWindow  # CALLING THE FUNCTION TO CJANGE THE POSITION OF THE WINDOW DURING MOUSE DRAG

    # ----> FUNCTION TO CAPTURE THE INITIAL POSITION OF THE MOUSE: NECESSERY FOR THE moveWindow FUNCTION
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
