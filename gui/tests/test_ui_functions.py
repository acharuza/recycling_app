import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import pytest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from gui.main import MainWindow
from gui.ui_function import UIFunction

TEST_IMAGE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "test_image.jpg"))
@pytest.fixture(scope="module")
def app():
    return QApplication([])

@pytest.fixture(scope="session", autouse=True)
def change_working_directory():
    os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def main_window(app):
    window = MainWindow()
    return window


def test_load_photo(main_window, mocker):
    mocker.patch("PyQt5.QtWidgets.QFileDialog.getOpenFileName", return_value=("test_image.jpg", ""))

    real_pixmap = QPixmap()
    pixmap_mock = mocker.patch("ui_function.QPixmap", return_value=real_pixmap)

    main_window.ui_function.load_photo()

    assert main_window.ui_function.selected_file_path == "test_image.jpg"
    pixmap_mock.assert_called_once_with("test_image.jpg")


def test_predict_category(main_window, mocker):
    main_window.selected_file_path = TEST_IMAGE_PATH

    mocker.patch("requests.post", return_value=mocker.Mock(status_code=200, json=lambda: {"prediction": "paper"}))

    prediction = UIFunction.predict_category(main_window)

    assert prediction == "paper"


def test_analyze_photo(main_window, mocker):
    prediction = "plastic"

    set_description_mock = mocker.patch("gui.ui_function.UIFunction.set_waste_description")

    main_window.ui_function.analyze_photo(prediction)



def test_set_waste_description(main_window, mocker):
    main_window.ui_function.category = "glass"

    mock_lab_desc_text = mocker.MagicMock()
    mock_lab_desc_photo = mocker.MagicMock()
    main_window.ui_function.ui.lab_desc_text = mock_lab_desc_text
    main_window.ui_function.ui.lab_desc_photo = mock_lab_desc_photo

    main_window.ui_function.set_waste_description()

    mock_lab_desc_text.setText.assert_called_once_with(
        "Odpad został najprawdopodobniej wykonany ze szkła. Możesz go wrzucić do zielonego kosza na szkło.\n Pamiętaj "
        "żeby do tego pojemnika nie wyrzucać szkła stołowego, ceramiki, szkła okiennego, luster, szyb, żarówek, "
        "porcelany oraz potłuczonych naczyń.")
    mock_lab_desc_photo.setPixmap.assert_called_once()


def test_stats_page(main_window, mocker):
    mock_open_image_base = mocker.patch("builtins.open",
                                        mocker.mock_open(read_data='{"2023-01-01 12:00:00": "plastic"}'))
    mock_load_image_base = mocker.patch("json.load", side_effect=[
        {"2023-01-01 12:00:00": "plastic"},
        {
            "plastic": {
                "name": "Plastik",
                "description": "Odpad wykonany z plastiku."
            }
        }
    ])

    mock_plot = mocker.patch("plotly.graph_objects.Figure.write_html")
    mock_set_url = mocker.patch.object(main_window.ui_function.ui.web_view, "setUrl")

    main_window.ui_function.stats_page()

    mock_open_image_base.assert_any_call("image_base.json", "r")
    mock_load_image_base.assert_called()
    mock_plot.assert_called_once()
    mock_set_url.assert_called_once()


def test_send_feedback(main_window, mocker):
    main_window.ui_function.selected_file_path = TEST_IMAGE_PATH
    main_window.ui_function.category = "paper"

    mock_post = mocker.patch("requests.post", return_value=mocker.Mock(status_code=200, json=lambda: {}))

    main_window.ui_function.send_feedback()

    mock_post.assert_called_once()


def test_choose_feedback(main_window):
    main_window.ui_function.choose_feedback()

    assert main_window.ui_function.ui.stackedWidget_desc.currentWidget() == main_window.ui_function.ui.page_form


def test_save_photo(main_window, mocker):
    main_window.ui_function.selected_file_path = "../../../recycling_app — kopia/gui/test_image.jpg"
    main_window.ui_function.category = "metal"

    mock_date = mocker.patch("ui_function.datetime")
    mock_date.now.return_value.strftime.return_value = "2023-01-01 12:00:00"

    mock_open = mocker.patch("builtins.open", mocker.mock_open())
    mock_json_load = mocker.patch("json.load", return_value={})
    mock_json_dump = mocker.patch("json.dump")

    mock_info = mocker.patch("PyQt5.QtWidgets.QMessageBox.information")
    mock_error = mocker.patch("PyQt5.QtWidgets.QMessageBox.critical")

    mock_stats_page = mocker.patch("ui_function.UIFunction.stats_page")

    main_window.ui_function.save_photo()

    mock_open.assert_any_call("image_base.json", "r", encoding="utf-8")
    mock_open.assert_any_call("image_base.json", "w", encoding="utf-8")
    mock_json_dump.assert_called_once_with(
        {"2023-01-01 12:00:00": "metal"}, mock_open(), ensure_ascii=False, indent=4
    )
    mock_info.assert_called_once_with(main_window.ui_function, "Sukces", "Dane zostały zapisane.")
    mock_stats_page.assert_called_once_with(main_window.ui_function)

    mock_open.side_effect = IOError("File error")
    main_window.ui_function.save_photo()
    mock_error.assert_called_once_with(main_window.ui_function, "Błąd zapisu", "Nie udało się zapisać: File error")
