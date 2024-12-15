from fastapi import APIRouter, File, Depends
from fastapi import UploadFile
from fastapi.responses import JSONResponse
from starlette import status
from typing import Literal
from recycling_app.api.constants import ALLOWED_LABELS, FILE_TYPES
from recycling_app.database.database_manager import DatabaseManager

router = APIRouter()


def get_db_manager() -> DatabaseManager:
    from recycling_app.main import db_manager

    return db_manager


@router.post("/user_feedback")
async def user_feedback(
    label: Literal[ALLOWED_LABELS],
    file: UploadFile = File(...),
    db_manager: DatabaseManager = Depends(get_db_manager),
):
    """
    This endpoint receives user feedback in the form of an image and a label. The image and label are saved to the database for later use.
    The label must be one of the allowed labels, and the image must be of an allowed file type.
    Allowed labels: "cardboard", "food_organics", "glass", "metal", "paper", "plastic", "textile", "trash", "vegetation"
    Allowed file types: image/jpeg, image/png
    """
    if file.content_type not in FILE_TYPES:
        return JSONResponse(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            content={"message": "Unsupported file type"},
        )
    try:
        img = await read_file(file)
    except IOError as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Error reading image", "details": str(e)},
        )
    img_format = file.filename.split(".")[-1]
    try:
        db_manager.save_image(img, img_format, label)
    except IOError as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Error writing image", "details": str(e)},
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Feedback received successfully"},
    )


async def read_file(file: UploadFile):
    """Wrapper function to read the image file"""
    try:
        img = await file.read()
    except IOError as e:
        raise e
    return img
