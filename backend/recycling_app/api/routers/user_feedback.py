from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from starlette import status
import os
from recycling_app.constants import IMAGE_STORAGE_PATH
import uuid
from datetime import datetime
from typing import Literal
from recycling_app.api.constants import ALLOWED_LABELS, FILE_TYPES, TIMESTAMPT_FORMAT

router = APIRouter()


@router.post("/user_feedback")
async def user_feedback(label: Literal[ALLOWED_LABELS], file: UploadFile = File(...)):
    if file.content_type not in FILE_TYPES:
        return JSONResponse(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            content={"message": "Unsupported file type"},
        )
    try:
        img = await file.read()
    except IOError as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Error reading image", "details": str(e)},
        )

    timestamp = datetime.now().strftime(TIMESTAMPT_FORMAT)
    img_format = file.filename.split(".")[-1]
    file_name = f"{uuid.uuid4()}_{label}_{timestamp}.{img_format}"
    file_path = os.path.join(IMAGE_STORAGE_PATH, label, file_name)
    with open(file_path, "wb") as f:
        f.write(img)
    mock_write_to_db(file_path, label, timestamp)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Feedback received successfully"},
    )


# mock_write_to_db is used to simulate writing to a database.
def mock_write_to_db(file_path: str, label: str, timestamp: str) -> None:
    print(f"Writing to database: {file_path}, {label}, {timestamp}")
