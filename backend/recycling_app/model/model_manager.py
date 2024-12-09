import torch
from recycling_app.preprocessing.preprocessing import Preprocessor
from recycling_app.model.feature_extraction import FeatureExtractor
from recycling_app.constants import IMAGE_LABELS

class ModelManager:

    def __init__(self, model_path, feature_extractor):
        self.model = torch.load(model_path)
        self.preprocessor = Preprocessor()
        self.feature_extractor = FeatureExtractor(feature_extractor)

    def predict(self, image):
        image = self.preprocessor.transform_test(image)
        features = self.feature_extractor.extract_features_pred(image)
        pred, prob = self.model.predict(features)
        label = IMAGE_LABELS[pred]
        probability = torch.max(prob).item()
        return label, probability
        
