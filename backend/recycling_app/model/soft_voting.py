import torch
import os
from recycling_app.constants import MODEL_PATH_RESNET101, MODEL_PATH_RESNET152, MODEL_PATH_VGG19

class SoftVoting:
    def __init__(self):
        self.resnet101 = torch.load(os.path.join(os.path.dirname(__file__), "nn_classifier_resnet101.pth"))
        self.resnet152 = torch.load(os.path.join(os.path.dirname(__file__), "nn_classifier_resnet152.pth"))
        self.vgg19 = torch.load(os.path.join(os.path.dirname(__file__), "nn_classifier_vgg19.pth"))

    def predict(self, input):
        pred_resnet101, prob_resnet101 = self.resnet101.predict(input['resnet101'])
        pred_resnet152, prob_resnet152 = self.resnet152.predict(input['resnet152'])
        pred_vgg19, prob_vgg19 = self.vgg19.predict(input['vgg19'])

        avg_output = torch.stack([0.4*prob_resnet101, 0.4*prob_resnet152, 0.2*prob_vgg19]).sum(dim=0)
        _, predicted = torch.max(avg_output, 1)
        probabilities = torch.max(avg_output, 1).values
        return predicted, probabilities

