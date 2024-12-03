from PyQt5.QtCore import QUrl
import plotly.graph_objects as go

from main import *

GLOBAL_STATE = 0  # checking if the window is full screen or not
GLOBAL_TITLE_BAR = True
init = False  # for initition of the window


class UIFunction(MainWindow):
    sort_mode = 'quantity'

    def init_stack_tab(self):
        global init

    def label_title(self, appName):
        self.ui.lab_appname.setText(appName)

    def maximize_restore(self):
        # min/max screen
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

    def return_status():
        return GLOBAL_STATE

    def set_status(status):
        global GLOBAL_STATE
        GLOBAL_STATE = status

    def constant_function(self):
        # double click to maximize window
        def max_double_click(stateMouse):
            if stateMouse.type() == QtCore.QEvent.MouseButtonDblClick:
                QtCore.QTimer.singleShot(250, lambda: UIFunction.maximize_restore(self))

        # Removing standard title bar
        if True:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.ui.frame_appname.mouseDoubleClickEvent = max_double_click
        else:
            self.ui.frame_close.hide()
            self.ui.frame_max.hide()
            self.ui.frame_min.hide()
            self.ui.frame_drag.hide()

        self.ui.bn_min.clicked.connect(lambda: self.showMinimized())
        self.ui.bn_max.clicked.connect(lambda: UIFunction.maximize_restore(self))
        self.ui.bn_close.clicked.connect(lambda: self.close())

    def stack_page(self):
        pass

    def button_pressed(self, button_name):
        # changing styles of buttons
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

        if button_name == 'bn_home':
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
            self.ui.bn_home.setStyleSheet(active_button_style)

        elif button_name == 'bn_stats':
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_stats)
            self.ui.bn_stats.setStyleSheet(active_button_style)

    def load_photo(self):
        # function for loading photos
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

    def analyze_photo(self):
        # function for analyzing photos

        try:
            with open("waste_desc.json", "r", encoding="utf-8") as file:
                waste_data = json.load(file)
        except Exception as e:
            QMessageBox.warning(self, "Błąd", f"Nie udało się odczytać pliku JSON: {e}")
            return

        # --------------- #losowy wybór kategorii z dostępnych jako analiza zdjęcia
        categories = list(waste_data.keys())
        category = random.choice(categories)
        self.category = category
        # ------------------

        category_info = waste_data.get(category)
        description = category_info.get("description", "Brak opisu")
        file_path = category_info.get("icon_big", "")

        if file_path:
            pixmap = QPixmap(file_path)

            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(pixmap.width() * 2, pixmap.height() * 2, Qt.KeepAspectRatio,
                                              Qt.SmoothTransformation)

                self.ui.lab_desc_photo.setPixmap(scaled_pixmap)
                self.ui.lab_desc_photo.setAlignment(Qt.AlignCenter)

                self.ui.lab_desc_text.setText(description)
                self.ui.lab_desc_text.setWordWrap(True)

                self.ui.lab_home_hed.setText(category_info['name'])
                self.ui.lab_home_hed.setAlignment(Qt.AlignCenter)
                self.ui.lab_home_hed.setStyleSheet("color: white; "
                                                   "border-top-left-radius: 25%;"
                                                   "border-top-right-radius: 25%;"
                                                   "background-color: rgb(46, 125, 50);"
                                                   "font-size: 38px;")

                self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_save)
                self.ui.bn_report.setVisible(True)
                self.ui.bn_like.setVisible(True)
            else:
                QMessageBox.warning(self, "Błąd", "Nie udało się załadować obrazu.")

    def save_photo(self):
        # function for saving photos

        if hasattr(self, 'selected_file_path') and self.selected_file_path:
            current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            new_data = {current_date: self.category}

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

    def stats_page(self):
        with open('image_base.json', 'r') as file:
            data = json.load(file)

        categories = list(data.values())
        category_counts = Counter(categories)

        with open('waste_desc.json', 'r') as file:
            waste_data = json.load(file)

        key_to_name = {key: value['name'] for key, value in waste_data.items()}
        most_common_categories = [(key_to_name[key], count) for key, count in category_counts.most_common(3)]
        labels = [self.ui.lab_number1, self.ui.lab_number2, self.ui.lab_number3]

        # top 3 categories
        for i, (category_name, count) in enumerate(most_common_categories):
            result_text = f"{category_name} \n{count}"
            labels[i].setText(result_text)
            labels[i].setWordWrap(True)

        for i in range(len(most_common_categories), 3):
            labels[i].setText("")

        all_categories = [value['name'] for value in waste_data.values()]
        category_counts_with_names = {key_to_name[key]: category_counts.get(key, 0) for key in waste_data}

        # plot
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=all_categories,
            y=[category_counts_with_names[category] for category in all_categories],
            hoverinfo='text',
            marker=dict(color='#2E7D32')
        ))

        fig.update_layout(
            title='Liczba odpadów w poszczególnych kategoriach',
            template='plotly_white',
            showlegend=False,
            paper_bgcolor='#C8E6C9',
            plot_bgcolor='#C8E6C9',
            autosize=True
        )

        fig.write_html("plot.html")
        html_path = os.path.abspath("plot.html")
        url = QUrl.fromLocalFile(html_path)
        self.ui.web_view.setUrl(url)

        # os.remove('plot.html')
