import torch.nn as nn
from torchvision import models


NUM_CLASSES = 3


def create_model():

    # Load ResNet18 with pretrained ImageNet weights
    model = models.resnet18(
        weights=models.ResNet18_Weights.DEFAULT
    )

    # Get number of inputs to the final layer
    num_features = model.fc.in_features

    # Replace the original ImageNet classifier
    model.fc = nn.Linear(
        num_features,
        NUM_CLASSES
    )

    return model