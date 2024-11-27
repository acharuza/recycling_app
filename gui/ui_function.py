from main import *

GLOBAL_STATE = 0  # checking if the window is full screen or not
GLOBAL_TITLE_BAR = True
init = False  # for initition of the window


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
        # double click to maximize window
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
        # changing text
        # self.ui.lab_home_desc.setText("Profile")

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
            self.selected_file_path = file_path
            self.ui.lab_home_hed.setText("")
            self.ui.lab_desc_text.setText("Analizuj obraz, aby poznać kategorię odpadu lub wczytaj nowy.")
            self.ui.lab_desc_photo.setPixmap(QPixmap())
            self.ui.bn_report.setVisible(False)
            self.ui.bn_like.setVisible(False)
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_change_save)

        else:
            QMessageBox.information(self, "Brak pliku", "Nie wybrano żadnego pliku.")

    def analyzePhoto(self):

        try:
            with open("waste_desc.json", "r", encoding="utf-8") as file:
                waste_data = json.load(file)
        except Exception as e:
            QMessageBox.warning(self, "Błąd", f"Nie udało się odczytać pliku JSON: {e}")
            return

        # ---------------
        categories = list(waste_data.keys())
        category = random.choice(categories)
        self.category = category
        # ------------------
        category_info = waste_data.get(category)
        description = category_info.get("description", "Brak opisu")
        file_path = category_info.get("icon", "")

        if file_path:
            pixmap = QPixmap(file_path)

            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(pixmap.width() * 2, pixmap.height() * 2, Qt.KeepAspectRatio,
                                              Qt.SmoothTransformation)

                self.ui.lab_desc_photo.setPixmap(scaled_pixmap)
                self.ui.lab_desc_photo.setAlignment(Qt.AlignCenter)

                self.ui.lab_desc_text.setText(description)
                self.ui.lab_desc_text.setWordWrap(True)

                self.ui.lab_home_hed.setText("Opis")
                self.ui.lab_home_hed.setAlignment(Qt.AlignCenter)
                self.ui.lab_home_hed.setStyleSheet("color: white; "
                                                   "border-top-left-radius: 25%;"
                                                   "border-top-right-radius: 25%;"
                                                   "background-color: rgb(46, 125, 50);")

                self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_save)
                self.ui.bn_report.setVisible(True)
                self.ui.bn_like.setVisible(True)
            else:
                QMessageBox.warning(self, "Błąd", "Nie udało się załadować obrazu.")

    def savePhoto(self):
        if hasattr(self, 'selected_file_path') and self.selected_file_path:
            new_data = {self.selected_file_path: self.category}

            try:
                try:
                    with open("image_base.json", "r", encoding="utf-8") as json_file:
                        data = json.load(json_file)
                except (FileNotFoundError, json.JSONDecodeError):
                    data = {}

                data.update(new_data)

                with open("image_base.json", "w", encoding="utf-8") as json_file:
                    json.dump(data, json_file, ensure_ascii=False, indent=4)

                QMessageBox.information(self, "Sukces", "Dane zostały zapisane.")
            except Exception as e:
                QMessageBox.critical(self, "Błąd zapisu", f"Nie udało się zapisać: {e}")
        else:
            QMessageBox.warning(self, "Brak danych", "Nie wybrano pliku do zapisania.")

    def statsPage(self):
        with open('image_base.json', 'r') as file:
            data = json.load(file)

        categories = list(data.values())
        category_counts = Counter(categories)

        most_common_categories = category_counts.most_common(3)

        labels = [self.ui.lab_number1, self.ui.lab_number2, self.ui.lab_number3]

        for i, (category, count) in enumerate(most_common_categories):
            result_text = f"{category} \n{count}"
            labels[i].setText(result_text)
            labels[i].setWordWrap(True)

        for i in range(len(most_common_categories), 3):
            labels[i].setText("")

        all_categories = ["Papier", "Odpady organiczne", "Metal", "Szkło", "Tworzywa sztuczne", "Tekstylia", "Karton",
                          "Odpady zmieszane"]
        category_counts = {category: category_counts.get(category, 0) for category in all_categories}
        print(category_counts)

        sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
        sorted_categories, sorted_values = zip(*sorted_categories)

        with open('waste_desc.json', 'r', encoding='utf-8') as file:
            waste_data = json.load(file)

        image_paths = {category: data["icon"] for category, data in waste_data.items()}

        sorted_image_paths = [image_paths[category] for category in sorted_categories]

        fig, ax = plt.subplots(figsize=(9, 3.5))
        bars = ax.bar(range(len(sorted_categories)), sorted_values, color='#2E7D32', width=0.4)

        for i, (bar, image_path) in enumerate(zip(bars, sorted_image_paths)):
            img = mpimg.imread(image_path)
            imagebox = OffsetImage(img, zoom=0.60)
            ab = AnnotationBbox(imagebox, (bar.get_x() + bar.get_width() / 2, 0.165),
                                frameon=False, box_alignment=(0.5, 1))
            ax.add_artist(ab)

        ax.set_xticks([])
        ax.set_ylim(0, max(sorted_values) + 1)
        plt.subplots_adjust(bottom=0.2)

        ax.set_ylabel('Ilość')
        fig.patch.set_facecolor('none')
        ax.set_facecolor('none')
        ax.yaxis.set_major_locator(plt.MultipleLocator(1))
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(2)
        ax.spines['bottom'].set_linewidth(2)

        fig.savefig('plot.png', format='png', bbox_inches='tight')

        pixmap = QPixmap('plot.png')

        self.ui.lab_graph.setGeometry(0, 0, 938, 500)
        self.ui.lab_graph.setAlignment(Qt.AlignCenter)

        self.ui.lab_graph.setPixmap(pixmap)

        os.remove('plot.png')
