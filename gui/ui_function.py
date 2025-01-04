from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QRadioButton
import requests
import mimetypes
import plotly.graph_objects as go
from collections import Counter
import os
from datetime import datetime

from main import *
from constants import *

GLOBAL_STATE = 0  # checking if the window is full screen or not
GLOBAL_TITLE_BAR = True
init = False  # for initition of the window


class UIFunction():
    sort_state = False

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
            self.ui.lab_desc_photo.clear()
            self.ui.bn_report.setVisible(False)
            self.ui.bn_like.setVisible(False)
            self.ui.bn_save.setEnabled(True)
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_change_save)

        else:
            QMessageBox.information(self, "Brak pliku", "Nie wybrano żadnego pliku.")

    def predict_category(self):
        #
        if not hasattr(self, 'selected_file_path') or not self.selected_file_path:
            QMessageBox.warning(self, "Brak zdjęcia", "Nie wybrano zdjęcia. Proszę najpierw załadować zdjęcie.")
            return

        url = f"{URL}waste_prediction"

        with open(self.selected_file_path, "rb") as file:
            mime_type, _ = mimetypes.guess_type(self.selected_file_path)
            files = {"file": (self.selected_file_path, file, mime_type)}
            try:
                response = requests.post(url, files=files, timeout=10)
                if response.status_code == 200:
                    prediction = response.json().get("prediction")
                    return prediction
                else:
                    QMessageBox.warning(self, "Błąd", f"Serwer zwrócił błąd: {response.status_code} - {response.text}")
            except requests.exceptions.Timeout:
                QMessageBox.warning(self, "Błąd", "Serwer nie odpowiada. Proszę spróbować ponownie później.")
            except Exception as e:
                QMessageBox.warning(self, "Błąd", f"Nie udało się połączyć z serwerem: {str(e)}")
                return None

    def analyze_photo(self, prediction):
        # function for showing result in UI

        self.category = prediction
        UIFunction.set_waste_description(self)
        self.ui.bn_like.setEnabled(True)
        self.ui.bn_report.setEnabled(True)

    def set_waste_description(self):
        category_info = WASTE_DESC.get(self.category)
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
                self.ui.bn_like.setIcon(QtGui.QIcon("icons/like.png"))
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

        self.ui.bn_save.setEnabled(False)
        UIFunction.stats_page(self)

    def stats_page(self):
        with open('image_base.json', 'r') as file:
            data = json.load(file)

        categories = list(data.values())
        category_counts = Counter(categories)

        key_to_name = {key: value['name'] for key, value in WASTE_DESC.items()}
        most_common_categories = [(key_to_name[key], count) for key, count in category_counts.most_common(3)]
        labels = [self.ui.lab_number1, self.ui.lab_number2, self.ui.lab_number3]

        # Wyświetlanie top 3 kategorii
        for i, (category_name, count) in enumerate(most_common_categories):
            result_text = f"{category_name} \n{count}"
            labels[i].setText(result_text)
            labels[i].setWordWrap(True)

        for i in range(len(most_common_categories), 3):
            labels[i].setText("")

        # Sortowanie danych na podstawie stanu sortowania
        all_categories = [value['name'] for value in WASTE_DESC.values()]
        category_counts_with_names = {key_to_name[key]: category_counts.get(key, 0) for key in WASTE_DESC}

        if UIFunction.sort_state:
            sorted_data = sorted(category_counts_with_names.items(), key=lambda x: x[1], reverse=True)
        else:
            sorted_data = sorted(category_counts_with_names.items())

        all_categories = [item[0] for item in sorted_data]
        counts = [item[1] for item in sorted_data]

        # Tworzenie wykresu
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=all_categories,
            y=counts,
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

    def waste_category(self):
        prediction = UIFunction.predict_category(self)
        if prediction is None:
            return
        UIFunction.analyze_photo(self, prediction)

    def send_feedback(self):

        url = f"{URL}user_feedback?label={self.category}"

        with open(self.selected_file_path, "rb") as file:
            mime_type, _ = mimetypes.guess_type(self.selected_file_path)
            mime_type = mime_type or "image/jpeg"
            files = {"file": (self.selected_file_path, file, mime_type)}

            try:
                response = requests.post(url, files=files)
                if response.status_code == 200:
                    print(f"Feedback sent: {response.json()}")
                    self.ui.bn_like.setToolTip("Przesłano potwierdzenie kategorii")
                    self.ui.bn_like.setEnabled(False)
                    self.ui.bn_like.setIcon(QtGui.QIcon("icons/like_green.png"))

                else:
                    QMessageBox.warning(self, "Błąd", f"Serwer zwrócił błąd: {response.status_code} - {response.text}")
            except Exception as e:
                QMessageBox.critical(self, "Błąd", f"Nie udało się połączyć z serwerem: {str(e)}")

    def send_positive_feedback(self):
        if not hasattr(self, 'selected_file_path') or not self.selected_file_path:
            QMessageBox.warning(self, "Brak zdjęcia", "Nie wybrano zdjęcia. Proszę najpierw załadować zdjęcie.")
            return

        if not hasattr(self, 'category') or not self.category:
            QMessageBox.warning(self, "Brak kategorii", "Nie określono kategorii. Wykonaj analizę zdjęcia.")
            return

        UIFunction.send_feedback(self)

        self.ui.bn_report.setEnabled(False)

    def choose_feedback(self):
        self.ui.stackedWidget_desc.setCurrentWidget(self.ui.page_form)

    def send_negative_feedback(self):
        for button in self.groupBox.findChildren(QRadioButton):
            if button.isChecked():
                name = button.text()
                x = WASTE_DESC.items()
                for key, value in WASTE_DESC.items():
                    print(value)
                    if value.get('name') == name:
                        self.category = key

        UIFunction.send_feedback(self)

        UIFunction.set_waste_description(self)
        self.ui.stackedWidget_desc.setCurrentWidget(self.page_desc)
        self.ui.bn_like.setEnabled(False)
        self.ui.bn_report.setEnabled(False)

    def desc_view(self):
        self.ui.stackedWidget_desc.setCurrentWidget(self.ui.page_desc)

    def toggle_sort_and_refresh(self):
        try:
            UIFunction.sort_state = not UIFunction.sort_state
            UIFunction.stats_page(self)

            if UIFunction.sort_state:
                self.ui.bn_sort.setText("Sortuj alfabetycznie")
            else:
                self.ui.bn_sort.setText("Sortuj malejąco")

        except Exception as e:
            print(f"Wystąpił błąd: {e}")

    def reset_data(self):

        confirmation = QMessageBox.question(
            self,
            "Potwierdzenie",
            "Czy na pewno chcesz zresetować dane?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if confirmation == QMessageBox.Yes:
            try:

                with open("image_base.json", "w", encoding="utf-8") as file:
                    json.dump({}, file, ensure_ascii=False, indent=4)
                QMessageBox.information(self, "Sukces", "Dane zostały zresetowane.")
                UIFunction.stats_page(self)
            except Exception as e:
                QMessageBox.critical(self, "Błąd", f"Nie udało się zresetować danych: {e}")
