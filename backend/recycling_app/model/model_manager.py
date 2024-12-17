from recycling_app.preprocessing.preprocessing import Preprocessor
from recycling_app.model.feature_extraction import FeatureExtractor
from recycling_app.constants import IMAGE_LABELS
from recycling_app.model.soft_voting import SoftVoting
from recycling_app.constants import (
    FEATURE_EXTRACTOR_RESNET101,
    FEATURE_EXTRACTOR_RESNET152,
    FEATURE_EXTRACTOR_VGG19,
)
import torch


class ModelManager:

    def __init__(self) -> None:
        """Class to manage the model"""
        self.model = SoftVoting()
        self.preprocessor = Preprocessor()
        self.feature_extractor_resnet101 = FeatureExtractor(FEATURE_EXTRACTOR_RESNET101)
        self.feature_extractor_resnet152 = FeatureExtractor(FEATURE_EXTRACTOR_RESNET152)
        self.feature_extractor_vgg19 = FeatureExtractor(FEATURE_EXTRACTOR_VGG19)

    def predict(self, image) -> tuple[str, float]:
        image = self.preprocessor.transform_test(image)
        features_resnet101 = self.feature_extractor_resnet101.extract_features_pred(
            image
        )
        features_resnet152 = self.feature_extractor_resnet152.extract_features_pred(
            image
        )
        features_vgg19 = self.feature_extractor_vgg19.extract_features_pred(image)
        features_vgg19 = features_vgg19.reshape(1, -1)
        input = {
            "resnet101": features_resnet101,
            "resnet152": features_resnet152,
            "vgg19": features_vgg19,
        }
        pred, prob = self.model.predict(input)
        prob = torch.max(prob, 1).values.item()
        label = IMAGE_LABELS[pred]
        return label, prob
