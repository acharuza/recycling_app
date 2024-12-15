import pytest
from recycling_app.database.database_manager import DatabaseManager
from recycling_app.database.database_manager import IMAGE_LABELS
import os
from unittest.mock import patch


@pytest.fixture
def database_path(tmp_path):
    return tmp_path / "database"


def test_database_initialization(database_path):
    db_manager = DatabaseManager(database_path)
    assert database_path.exists()
    for label in IMAGE_LABELS:
        assert (database_path / label).exists()


def test_save_image(database_path):
    db_manager = DatabaseManager(database_path)
    img = b"image"
    img_format = "png"
    label = "glass"
    db_manager.save_image(img, img_format, label)
    assert len(os.listdir(database_path / label)) == 1


def test_clear_database(database_path):
    db_manager = DatabaseManager(database_path)
    img = b"image"
    img_format = "png"
    label = "glass"
    db_manager.save_image(img, img_format, label)
    db_manager.clear_database()
    for label in IMAGE_LABELS:
        assert len(os.listdir(database_path / label)) == 0


def test_save_image_error(mocker, database_path):
    mocker.patch("builtins.open", side_effect=IOError)
    db_manager = DatabaseManager(database_path)
    img = b"image"
    img_format = "png"
    label = "glass"
    with pytest.raises(IOError):
        db_manager.save_image(img, img_format, label)


def test_clear_database_error(mocker, database_path):
    mocker.patch("os.remove", side_effect=IOError)
    db_manager = DatabaseManager(database_path)
    img = b"image"
    img_format = "png"
    label = "glass"
    db_manager.save_image(img, img_format, label)
    with pytest.raises(IOError):
        db_manager.clear_database()
