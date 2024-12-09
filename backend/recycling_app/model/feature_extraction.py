import torch
from torchvision import models
import torch.nn as nn
import numpy as np
from tqdm import tqdm


class FeatureExtractor:

    def __init__(self, model_name):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        if model_name == "resnet101":
            self.model = models.resnet101(weights=models.ResNet101_Weights.DEFAULT)
        elif model_name == "resnet152":
            self.model = models.resnet152(weights=models.ResNet152_Weights.DEFAULT)
        elif model_name == "alexnet":
            self.model = models.alexnet(weights=models.AlexNet_Weights.DEFAULT)
        elif model_name == "googlenet":
            self.model = models.googlenet(weights=models.GoogLeNet_Weights.DEFAULT)
        elif model_name == "vgg19":
            self.model = models.vgg19(weights=models.VGG19_Weights.DEFAULT)
        else:
            raise ValueError(f"Model {model_name} is not supported")

        self.model = nn.Sequential(*list(self.model.children())[:-1])
        self.model.to(self.device)
        self.model.eval()

    def extract_features(self, data_loader) -> tuple[np.ndarray, np.ndarray]:
        features = []
        labels = []
        with torch.no_grad():
            for inputs, targets in tqdm(
                data_loader, desc="Extracting features", unit="batch"
            ):
                inputs = inputs.to(self.device)
                output = self.model(inputs).squeeze()
                features.append(output.cpu().numpy())
                labels.append(targets.numpy())
        return np.vstack(features), np.hstack(labels)
    
    def extract_features_pred(self, image) -> np.ndarray:
        with torch.no_grad():
            image = image.unsqueeze(0).to(self.device)
            output = self.model(image).squeeze()
        return output.cpu().numpy()
