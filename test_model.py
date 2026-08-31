import torch

from ai.models.model import create_model


model = create_model()

print(model)

print("\nFinal classification layer:")
print(model.fc)

# Test with one fake batch
x = torch.randn(2, 3, 224, 224)

output = model(x)

print("\nInput shape:", x.shape)
print("Output shape:", output.shape)