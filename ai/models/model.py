import torch.nn as nn
from torchvision import models


def create_model(num_classes=3, pretrained=True):
    if pretrained:
        weights = models.ResNet18_Weights.DEFAULT
    else:
        weights = None

    model = models.resnet18(weights=weights)

    model.fc = nn.Linear(
        model.fc.in_features,
        num_classes
    )

    return model