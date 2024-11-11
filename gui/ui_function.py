

from main import *

GLOBAL_STATE = 0 #checking if the window is full screen or not
GLOBAL_TITLE_BAR = True
init = False #for initition of the window

class UIFunction(MainWindow):

    def initStackTab(self):
        global init

    def labelTitle(self, appName):
        self.ui.lab_appname.setText(appName)

    def maximize_restore(self):
        global GLOBAL_STATE
        status = GLOBAL_STATE
        if status == 0:
            self.showMaximized()
            GLOBAL_STATE = 1
            self.ui.bn_max.setToolTip("Restore")
            self.ui.bn_max.setIcon(QtGui.QIcon("icons/restore.png"))
            self.ui.frame_drag.hide()
        else:
            GLOBAL_STATE = 0
            self.showNormal()
            self.resize(self.width() + 1, self.height() + 1)
            self.ui.bn_max.setToolTip("Maximize")
            self.ui.bn_max.setIcon(QtGui.QIcon("icons/maximize.png"))
            self.ui.frame_drag.show()

    def returnStatus():
        return GLOBAL_STATE

    def setStatus(status):
        global GLOBAL_STATE
        GLOBAL_STATE = status

    def constantFunction(self):
        #double click to maximize window
        def maxDoubleClick(stateMouse):
            if stateMouse.type() == QtCore.QEvent.MouseButtonDblClick:
                QtCore.QTimer.singleShot(250, lambda: UIFunction.maximize_restore(self))

        # Removing standard title bar
        if True:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.ui.frame_appname.mouseDoubleClickEvent = maxDoubleClick
        else:
            self.ui.frame_close.hide()
            self.ui.frame_max.hide()
            self.ui.frame_min.hide()
            self.ui.frame_drag.hide()

        self.ui.bn_min.clicked.connect(lambda: self.showMinimized())

        self.ui.bn_max.clicked.connect(lambda: UIFunction.maximize_restore(self))

        self.ui.bn_close.clicked.connect(lambda: self.close())

    def stackPage(self):
        pass
        #changing text
        #self.ui.lab_home_desc.setText("Profile")

    def buttonPressed(self, buttonName):

        default_button_style = """
                    QPushButton {
                        border: none;
                        background-color: rgb(46, 125, 50);
                        color: white;
                    }
                    QPushButton:hover {
                        background-color: rgb(129, 199, 132);
                    }
                    QPushButton:pressed {    
                        background-color: rgb(129, 199, 132);
                    }
                """

        active_button_style = """
                    QPushButton {
                        border: none;
                        background-color: rgb(129, 199, 132);
                        color: white;
                    }
                    QPushButton:hover {
                        background-color: rgb(129, 199, 132);
                    }
                    QPushButton:pressed {    
                        background-color: rgb(129, 199, 132);
                    }
                """

        self.ui.bn_home.setStyleSheet(default_button_style)
        self.ui.bn_stats.setStyleSheet(default_button_style)

        if buttonName == 'bn_home':
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
            self.ui.bn_home.setStyleSheet(active_button_style)

        elif buttonName == 'bn_stats':
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_stats)
            self.ui.bn_stats.setStyleSheet(active_button_style)

    def loadPhoto(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Wybierz zdjęcie", "", "Images (*.png *.jpg *.jpeg *.bmp)")

        if file_path:
            pixmap = QPixmap(file_path)
            self.ui.lab_photo.setPixmap(
                pixmap.scaled(self.ui.lab_photo.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_change_save)

        else:
            QMessageBox.information(self, "Brak pliku", "Nie wybrano żadnego pliku.")


    def analyzePhoto(self):
        # TODO: ogarnąć tekst do każdego rodzaju, strukturę tej funkcji, css itp, reset opisu po wczytaniu nowego zdjęcia
        file_path = "icons/bin_blue.png"

        if file_path:
            pixmap = QPixmap(file_path)

            if not pixmap.isNull():

                scaled_pixmap = pixmap.scaled(pixmap.width()*2, pixmap.height()*2, Qt.KeepAspectRatio, Qt.SmoothTransformation)

                layout = QVBoxLayout()

                text_label = QLabel("Analizowany odpad został najprawdopodniej wykonany z papieru i powinien zostać wrzucony do niebieskiego kosza.")
                text_label.setWordWrap(True)
                text_label.setAlignment(Qt.AlignCenter)
                font = QFont()
                font.setPointSize(16)
                text_label.setFont(font)


                image_label = QLabel()
                image_label.setPixmap(scaled_pixmap)
                image_label.setAlignment(Qt.AlignCenter)

                self.ui.lab_home_hed.setText("Opis")
                self.ui.lab_home_hed.setAlignment(Qt.AlignCenter)
                self.ui.lab_home_hed.setStyleSheet("color: white; "
                                                   "border-top-left-radius: "
                                                   "25%;border-top-right-radius: "
                                                   "25%;background-color: "
                                                   "rgb(46, 125, 50);")

                layout.addWidget(text_label)
                layout.addWidget(image_label)

                widget = QWidget(self)
                widget.setLayout(layout)

                self.lab_home_desc.setLayout(layout)
                self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_save)
            else:
                QMessageBox.warning(self, "Błąd", "Nie udało się załadować obrazu.")

    def savePhoto(self):
        print('save')





