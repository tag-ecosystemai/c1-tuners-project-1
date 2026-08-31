from ai.data.dataset import create_dataloaders


train_loader, val_loader, test_loader, classes = create_dataloaders()

print("Classes:", classes)

print("Training images:", len(train_loader.dataset))
print("Validation images:", len(val_loader.dataset))
print("Test images:", len(test_loader.dataset))

images, labels = next(iter(train_loader))

print("Batch image shape:", images.shape)
print("Batch label shape:", labels.shape)