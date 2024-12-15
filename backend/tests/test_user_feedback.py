import pytest
from fastapi.testclient import TestClient
from io import BytesIO
from unittest.mock import MagicMock, patch
from recycling_app.api.routers.user_feedback import get_db_manager
from recycling_app.api.constants import ALLOWED_LABELS

# turning off model manager initialization
with patch("recycling_app.model.model_manager.ModelManager", MagicMock()):
    from recycling_app.main import app

client = TestClient(app)

# fixtures to use in tests


@pytest.fixture
def mock_file():
    """Fixture to mock an image file with custom file type"""

    def _mock_file(
        filename: str = "test_image.jpg",
        file_content: BytesIO = BytesIO(b"test data"),
        mime_type: str = "image/jpeg",
    ):
        return [("file", (filename, file_content, mime_type))]

    return _mock_file


def mock_db_manager():
    """Mock the DatabaseManager class"""
    mock = MagicMock()
    mock.save_image = MagicMock()
    return mock


@pytest.fixture
def override_get_db_manager():
    """Override the get_db_manager dependency"""
    app.dependency_overrides[get_db_manager] = mock_db_manager
    yield
    app.dependency_overrides.clear()


# tests


@pytest.mark.parametrize(
    "filetype,label",
    [(filetype, label) for filetype in ["jpeg", "png"] for label in ALLOWED_LABELS],
)
def test_user_feedback_success(override_get_db_manager, mock_file, filetype, label):
    """Test user feedback success"""
    file = mock_file(
        filename=f"test_image.{filetype.replace('e', '')}",
        mime_type=f"image/{filetype}",
    )
    response = client.post(f"/user_feedback?label={label}", files=file)
    assert response.status_code == 200
    assert response.json() == {"message": "Feedback received successfully"}


def test_user_feedback_unsupported_file_type(override_get_db_manager, mock_file):
    """Test user feedback with unsupported file type"""
    file = mock_file(filename="test.txt", mime_type="text/plain")
    response = client.post("/user_feedback?label=plastic", files=file)
    assert response.status_code == 415
    assert response.json() == {"message": "Unsupported file type"}


def test_user_feedback_wrong_label(override_get_db_manager, mock_file):
    """Test user feedback with wrong label"""
    file = mock_file()
    response = client.post("/user_feedback?label=wrong_label", files=file)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "literal_error",
                "loc": ["query", "label"],
                "msg": "Input should be 'cardboard', 'food_organics', 'glass', 'metal', 'paper', 'plastic', 'textile', 'trash' or 'vegetation'",
                "input": "wrong_label",
                "ctx": {
                    "expected": "'cardboard', 'food_organics', 'glass', 'metal', 'paper', 'plastic', 'textile', 'trash' or 'vegetation'"
                },
            }
        ]
    }

@patch("recycling_app.api.routers.user_feedback.read_file", side_effect=IOError("Error reading image"))
def test_user_feedback_error_reading_image(mock_read, override_get_db_manager):
    """Test user feedback with error reading image"""
    response = client.post(
        "/user_feedback?label=plastic",
        files={
            "file": ("test_image.jpg", "test_content", "image/jpeg"),
        },
    )
    assert response.status_code == 500
    assert response.json() == {
        "message": "Error reading image",
        "details": "Error reading image",
    }
    mock_read.assert_called_once()

def test_user_feedback_db_save_error(override_get_db_manager, mock_file):
    """Test user feedback with error saving image"""
    db_manager_mock = mock_db_manager()
    db_manager_mock.save_image.side_effect = IOError("Error saving image")
    app.dependency_overrides[get_db_manager] = lambda: db_manager_mock

    file = mock_file()
    response = client.post("/user_feedback?label=plastic", files=file)
    assert response.status_code == 500
    assert response.json() == {
        "message": "Error writing image",
        "details": "Error saving image",
    }
    db_manager_mock.save_image.assert_called_once()
