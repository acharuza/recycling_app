import os
from recycling_app.constants import (
    IMAGE_LABELS,
    TIMESTAMP_FORMAT,
)
from datetime import datetime
import uuid

class DatabaseManager:

    def __init__(self, database_path):
        self.database_path = database_path
        if not os.path.exists(database_path):
            os.makedirs(database_path)
            for label in IMAGE_LABELS:
                os.makedirs(os.path.join(database_path, label))

    def save_image(self, img, img_format, label):
        timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
        file_name = f"{uuid.uuid4()}_{label}_{timestamp}.{img_format}"
        file_path = os.path.join(self.database_path, label, file_name)
        try:
            with open(file_path, "wb") as f:
                f.write(img)
        except IOError as e:
            raise IOError(f"Error writing image: {str(e)}")

    def clear_database(self):
        for label in IMAGE_LABELS:
            for file in os.listdir(os.path.join(self.database_path, label)):
                file_path = os.path.join(self.database_path, label, file)
                try:
                    os.remove(file_path)
                except IOError as e:
                    raise IOError(f"Error deleting file: {str(e)}")


if __name__ == '__main__':
    DatabaseManager()