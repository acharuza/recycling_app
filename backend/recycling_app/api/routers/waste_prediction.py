from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from starlette import status
from io import BytesIO
from recycling_app.api.constants import FILE_TYPES
from PIL import Image

router = APIRouter()


@router.post("/waste_prediction")
async def waste_prediction(file: UploadFile = File(...)):
    if file.content_type not in FILE_TYPES:
        return JSONResponse(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            content={"message": "Unsupported file type"},
        )
    try:
        img = BytesIO(await file.read())
    except IOError as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Error reading image", "details": str(e)},
        )
    img = Image.open(img)
    # showing image to prove that it's been sent
    img.show()
    model_response = mock_model_response(img)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"prediction": model_response},
    )


# mock_model_response is used to simulate the response of a machine learning model.
def mock_model_response(img: Image.Image) -> str:
    return "paper"
