import pytest
from fastapi.testclient import TestClient
from recycling_app.api.routers.waste_prediction import (
    waste_prediction,
    get_model_manager,
)
from unittest.mock import MagicMock, patch
from io import BytesIO
from PIL import Image

with patch("recycling_app.model.model_manager.ModelManager") as mock_model:
    from recycling_app.main import app

    mock_model.return_value.predict.return_value = ("glass", 0.9)

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


def mock_model_manager():
    """Mock the ModelManager class"""
    mock = MagicMock()
    mock.predict = MagicMock()
    mock.predict.return_value = ("glass", 0.9)
    return mock


@pytest.fixture
def override_get_model_manager():
    """Override the get_model_manager dependency"""
    app.dependency_overrides[get_model_manager] = mock_model_manager
    yield
    app.dependency_overrides.clear()


# tests


@pytest.mark.parametrize("filetype", ["jpeg", "png"])
def test_waste_prediction_success(mocker, mock_file, filetype, override_get_model_manager):
    """Test waste prediction success"""
    fake_image = Image.new("RGB", (100, 100), color="white")
    mocker.patch(
        "recycling_app.api.routers.waste_prediction.Image.open", return_value=fake_image
    )
    file = mock_file(
        filename=f"test_image.{filetype.replace('e', '')}",
        mime_type=f"image/{filetype}",
    )
    response = client.post("/waste_prediction", files=file)
    assert response.status_code == 200


def test_waste_prediction_unsupported_file_type(mock_file, override_get_model_manager):
    """Test waste prediction with unsupported file type"""
    file = mock_file(mime_type="application/json")
    response = client.post("/waste_prediction", files=file)
    assert response.status_code == 415


def test_waste_prediction_error_reading_image(
    mocker, mock_file, override_get_model_manager
):
    """Test waste prediction with error reading image"""
    mocker.patch(
        "recycling_app.api.routers.waste_prediction.BytesIO",
        side_effect=IOError("I/O operation on closed file."),
    )
    file = mock_file()
    response = client.post("/waste_prediction", files=file)
    assert response.status_code == 500
    assert response.json() == {
        "message": "Error reading image",
        "details": "I/O operation on closed file.",
    }
