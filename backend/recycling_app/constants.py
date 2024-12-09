import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model', 'nn_classifier_resnet101.pth')
DATABASE_PATH = os.path.join('..', os.path.dirname(__file__), 'db')
FEATURE_EXTRACTOR = "resnet101"

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