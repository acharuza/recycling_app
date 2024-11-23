from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from starlette import status
from recycling_app.preprocessing.Preprocessing import Preprocessor
import torch
from io import BytesIO
from recycling_app.api.constants import FILE_TYPES

router = APIRouter()
img_preprocessor = Preprocessor()


@router.post("/waste_prediction")
async def waste_prediction(file: UploadFile = File(...)):
    if file.content_type not in FILE_TYPES:
        return JSONResponse(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            content={"message": "Unsupported file type"},
        )
    try:
        raw_img = BytesIO(await file.read())
    except IOError as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Error reading image", "details": str(e)},
        )
    preprocessed_img = img_preprocessor(raw_img)
    model_response = mock_model_response(preprocessed_img)

    # returning tensor_shape to check if the image was preprocessed correctly
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"prediction": model_response, "tensor_shape": preprocessed_img.shape},
    )


# mock_model_response is used to simulate the response of a machine learning model.
def mock_model_response(preprocessed_img: torch.Tensor) -> str:
    return "paper"
