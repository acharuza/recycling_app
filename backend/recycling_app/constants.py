import os

MODEL_PATH_RESNET101 = os.path.join(
    os.path.dirname(__file__), "model", "nn_classifier_resnet101.pth"
)

MODEL_PATH_RESNET152 = os.path.join(
    os.path.dirname(__file__), "model", "nn_classifier_resnet152.pth"
)

MODEL_PATH_VGG19 = os.path.join(
    os.path.dirname(__file__), "model", "nn_classifier_vgg19.pth"
)

DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "db")
FEATURE_EXTRACTOR_RESNET101 = "resnet101"
FEATURE_EXTRACTOR_RESNET152 = "resnet152"
FEATURE_EXTRACTOR_VGG19 = "vgg19"

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

if __name__ == "__main__":
    print(DATABASE_PATH)
    print(IMAGE_LABELS)
    print(TIMESTAMP_FORMAT)
