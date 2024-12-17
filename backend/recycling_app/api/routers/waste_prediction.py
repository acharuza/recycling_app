from fastapi import APIRouter, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from starlette import status
from io import BytesIO
from recycling_app.api.constants import FILE_TYPES
from PIL import Image
from recycling_app.model.model_manager import ModelManager

router = APIRouter()


def get_model_manager() -> ModelManager:
    from recycling_app.main import model_manager

    return model_manager


@router.post("/waste_prediction")
async def waste_prediction(
    file: UploadFile = File(...),
    model_manager: ModelManager = Depends(get_model_manager),
):
    """
    This endpoint is used to predict the type of waste in the image. It takes an image as input and returns the prediction and the probability of the prediction.
    Image must be in one of the allowed formats.
    Allowed formats: ['image/jpeg', 'image/png
    """
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
    model_response = model_manager.predict(img)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"prediction": model_response[0], "probability": model_response[1]},
    )
