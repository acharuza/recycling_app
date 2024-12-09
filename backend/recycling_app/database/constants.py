import os

DATABASE_DIR_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'db')
IMAGE_LABELS = [
    "cardboard",
    "food_organics",
    "glass",
    "metal",
    "paper",
    "plastic",
    "textile",
    "trash",
    "vegetation",
]
TIMESTAMP_FORMAT = "%Y-%m-%d_%H-%M-%S"