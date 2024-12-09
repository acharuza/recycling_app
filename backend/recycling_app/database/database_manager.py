import os
from recycling_app.database.constants import (
    DATABASE_DIR_PATH,
    IMAGE_LABELS,
    TIMESTAMP_FORMAT,
)
from datetime import datetime
import uuid

class DatabaseManager:

    def __init__(self):
        if not os.path.exists(DATABASE_DIR_PATH):
            os.makedirs(DATABASE_DIR_PATH)
            for label in IMAGE_LABELS:
                os.makedirs(os.path.join(DATABASE_DIR_PATH, label))

    def save_image(self, img, img_format, label):
        timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
        file_name = f"{uuid.uuid4()}_{label}_{timestamp}.{img_format}"
        file_path = os.path.join(DATABASE_DIR_PATH, label, file_name)
        try:
            with open(file_path, "wb") as f:
                f.write(img)
        except IOError as e:
            raise IOError(f"Error writing image: {str(e)}")

    def clear_database(self):
        for label in IMAGE_LABELS:
            for file in os.listdir(os.path.join(DATABASE_DIR_PATH, label)):
                file_path = os.path.join(DATABASE_DIR_PATH, label, file)
                try:
                    os.remove(file_path)
                except IOError as e:
                    raise IOError(f"Error deleting file: {str(e)}")


if __name__ == '__main__':
    DatabaseManager()