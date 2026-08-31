# AI Documentation — Potato Leaf Health Classifier

## 1. Overview

This folder contains the AI/ML component for the **Team Tunners Agriculture Crop/Produce Image Inspector**.

The current AI implementation focuses on **potato leaf health classification**.

Given an image of a potato leaf, the model predicts one of three classes:

1. Potato Early Blight
2. Potato Late Blight
3. Potato Healthy

The model also returns a confidence score for the prediction.

The final selected model is a **fine-tuned pretrained ResNet18** implemented with PyTorch.

---

# 2. AI Pipeline

The current AI pipeline is:

```text
Potato Leaf Image
       ↓
Image Preprocessing
       ↓
Fine-tuned ResNet18
       ↓
Class Probabilities
       ↓
Predicted Class
       ↓
Confidence Score
```

The inference pipeline is implemented in:

```text
ai/inference/predict.py
```

---

# 3. Dataset

The dataset used for the project contains **2,152 potato leaf images** across three classes.

| Class               | Number of Images |
| ------------------- | ---------------: |
| Potato Early Blight |            1,000 |
| Potato Late Blight  |            1,000 |
| Potato Healthy      |              152 |
| **Total**           |        **2,152** |

### Dataset characteristics

During dataset validation, the following checks were performed:

* Image format
* Image dimensions
* Corrupt images
* Duplicate images
* Class distribution

Results:

```text
Image format: JPEG
Image dimensions: 256 × 256
Corrupt images: 0
Duplicate images: 0
```

The dataset is **not committed to GitHub**.

The raw dataset is excluded through `.gitignore`.

Expected local location:

```text
ai/data/raw/Dataset/
```

---

# 4. Dataset Split

The dataset was divided into three subsets:

```text
Training:    1,506 images
Validation:    323 images
Testing:      323 images
```

Total:

```text
1,506 + 323 + 323 = 2,152
```

The validation and test sets are kept separate from model training.

The test set is used only for final performance evaluation.

---

# 5. Class Distribution and Imbalance

The dataset contains a significant class imbalance.

```text
Early Blight → 1,000 images
Late Blight  → 1,000 images
Healthy      →   152 images
```

The Healthy class represents a much smaller portion of the dataset.

This became an important consideration during experimentation because a model can achieve high overall accuracy while still performing poorly on the minority class.

For this reason, **Healthy recall** was tracked alongside overall validation accuracy during model experimentation.

---

# 6. Image Preprocessing

The original dataset images are:

```text
256 × 256
```

The model receives images in the following format:

```text
3 × 224 × 224
```

Images are:

1. Loaded as RGB
2. Resized/cropped to the required input dimensions
3. Converted to PyTorch tensors
4. Normalized using the project's preprocessing pipeline

The preprocessing implementation is located at:

```text
ai/data/preprocessing.py
```

### Important

The preprocessing used during inference must remain consistent with the preprocessing expected by the trained model.

The inference module already handles the required preprocessing.

---

# 7. Data Augmentation

Data augmentation was used during model training to improve generalization.

Augmentation creates different transformed versions of training images through transformations such as:

* Random horizontal flipping
* Rotation
* Cropping/resizing
* Other image appearance variations

Augmentation is applied to the **training data only**.

Validation and test images are not augmented.

### Important clarification about class imbalance

Data augmentation does not permanently increase the number of stored images in the dataset.

For example, the Healthy class still contains:

```text
152 original images
```

Augmentation creates different variations of those images during training, but it does not change the underlying dataset count to something like 500 or 1,000 Healthy images.

Therefore, augmentation helps the model see more varied training examples, but **does not by itself solve the class imbalance problem**.

This was one of the reasons class weighting was investigated as a separate experiment.

---

# 8. Model Experimentation

Model selection was performed experimentally rather than choosing an architecture arbitrarily.

Google Colab was used as the experimentation environment to determine the final modeling direction.

Four experiments were conducted.

The final approach was then rebuilt and retrained from scratch in the VS Code project.

---

## Experiment 001 — CNN Baseline

### Objective

The first experiment established a baseline using a custom Convolutional Neural Network (CNN).

Data augmentation was included during training.

### Result

```text
Best Validation Accuracy: 98.76%
Healthy Recall:            83%
```

The model achieved strong overall performance.

However, the Healthy class remained the main weakness.

The model correctly identified 83% of Healthy images in the validation set.

This established the baseline against which subsequent experiments were compared.

### Decision

**Baseline**

The model was retained as a reference point but further improvement was investigated.

---

# 9. Experiment 002 — CNN + Class Weighting

### Objective

The second experiment investigated whether class imbalance could be addressed by assigning different weights to the classes during loss calculation.

Because the Healthy class had significantly fewer examples, a larger loss weight was assigned to it.

The objective was to encourage the model to pay more attention to mistakes involving the minority class.

### Result

```text
Best Validation Accuracy: 97.21%
Healthy Recall:            83%
```

Compared with Experiment 001:

```text
Validation Accuracy:
98.76% → 97.21%

Healthy Recall:
83% → 83%
```

Class weighting therefore did not improve Healthy recall and resulted in lower overall validation accuracy.

### Decision

**Rejected**

Class weighting was not selected for the final model.

---

# 10. Experiment 003 — ResNet18 Feature Extraction

### Objective

The third experiment introduced a pretrained **ResNet18** architecture.

Instead of training a CNN completely from scratch, ResNet18 provided pretrained visual representations that could be used as a feature extractor for the potato leaf classification task.

The final classification layer was adapted for our three classes.

### Result

```text
Best Validation Accuracy: 99.38%
Healthy Recall:            91%
```

This represented a significant improvement over the previous experiments.

Comparison:

```text
Experiment 001 → 98.76% validation accuracy
Experiment 002 → 97.21% validation accuracy
Experiment 003 → 99.38% validation accuracy
```

Healthy recall also improved:

```text
Experiment 001 → 83%
Experiment 002 → 83%
Experiment 003 → 91%
```

### Decision

**Improved**

ResNet18 clearly demonstrated stronger performance than the custom CNN approaches.

However, the experiment used ResNet18 primarily as a feature extractor.

The next question was whether allowing the pretrained network itself to adapt further to the potato leaf dataset could produce an additional improvement.

This led to Experiment 004.

---

# 11. Experiment 004 — Fine-Tuned ResNet18

### Objective

The fourth experiment fine-tuned the pretrained ResNet18 specifically for the potato leaf classification task.

Instead of relying only on the pretrained feature representations, the model weights were allowed to adapt to the visual characteristics of the potato leaf dataset.

The final classification layer produces three outputs:

```text
Linear(in_features=512, out_features=3)
```

The class mapping is:

```text
0 → Potato___Early_blight
1 → Potato___Late_blight
2 → Potato___healthy
```

### Result

```text
Best Validation Accuracy: 100.00%
Healthy Recall:           100.00%
Test Accuracy:            100.00%
```

The final test-set confusion matrix was:

```text
[[150   0   0]
 [  0 150   0]
 [  0   0  23]]
```

This means:

```text
Early Blight → 150/150 correctly classified
Late Blight  → 150/150 correctly classified
Healthy      →  23/23 correctly classified
```

### Decision

🏆 **Selected as the final model**

---

# 12. Experiment Comparison

| Experiment | Approach                    | Best Val. Accuracy | Healthy Recall | Decision    |
| ---------- | --------------------------- | -----------------: | -------------: | ----------- |
| **001**    | CNN baseline                |             98.76% |            83% | Baseline    |
| **002**    | CNN + class weighting       |             97.21% |            83% | Rejected    |
| **003**    | ResNet18 feature extraction |             99.38% |            91% | Improved    |
| **004**    | **Fine-tuned ResNet18**     |           **100%** |       **100%** | 🏆 Selected |

---

# 13. Why Fine-Tuned ResNet18 Was Selected

The final model was selected based on the results of the experiments.

### 1. Highest validation performance

Fine-tuned ResNet18 achieved:

```text
100.00% validation accuracy
```

compared with:

```text
98.76% → CNN baseline
97.21% → CNN + class weighting
99.38% → ResNet18 feature extraction
```

---

### 2. Strong performance on the minority class

One of the main problems identified during experimentation was the Healthy class.

Healthy recall progressed from:

```text
83%
 ↓
83%
 ↓
91%
 ↓
100%
```

The fine-tuned ResNet18 therefore addressed the weakness that motivated much of the experimentation.

---

### 3. Transfer learning

ResNet18 starts from pretrained visual representations rather than learning all visual features from scratch.

This is useful for our relatively small specialized dataset.

The pretrained model already contains useful general visual features, which can then be adapted to the potato leaf classification task.

---

### 4. Good balance between performance and complexity

ResNet18 provides a strong balance between:

```text
Model performance
       +
Transfer learning capability
       +
Computational requirements
       +
Implementation simplicity
```

For the current MVP, a significantly larger architecture would add complexity without being necessary based on our experimental results.

---

### 5. Evidence-based model selection

The final model was not selected simply because ResNet18 is a popular architecture.

The decision was driven by experimentation:

```text
Custom CNN
    ↓
Identify weaknesses
    ↓
Class weighting
    ↓
Evaluate alternative architecture
    ↓
ResNet18 feature extraction
    ↓
Fine-tuning
    ↓
Best overall result
    ↓
FINAL MODEL
```

---

# 14. Final Model Performance

The final fine-tuned ResNet18 achieved:

```text
Best Validation Accuracy: 100.00%
Test Accuracy:            100.00%
```

### Test Set Classification Report

```text
                       precision    recall    f1-score   support

Potato___Early_blight       1.00      1.00      1.00       150
Potato___Late_blight        1.00      1.00      1.00       150
Potato___healthy            1.00      1.00      1.00        23

accuracy                                      1.00       323
macro avg                   1.00      1.00      1.00       323
weighted avg                1.00      1.00      1.00       323
```

### Confusion Matrix

```text
[[150   0   0]
 [  0 150   0]
 [  0   0  23]]
```

---

# 15. Interpreting the 100% Test Accuracy

The 100% test accuracy is a significant result and is the strongest result obtained across all four experiments.

It means that the final model correctly classified **all 323 images in the held-out test set**.

Specifically:

```text
150/150 Early Blight  → Correct
150/150 Late Blight   → Correct
23/23 Healthy         → Correct
```

This provides strong evidence that the model has learned features that distinguish the three classes within the dataset distribution.

However, the result should be interpreted correctly.

The test set was created from the same overall dataset used during model development. Although the test images were held out from training, they still come from the same underlying data distribution.

Therefore:

> **100% test accuracy demonstrates excellent performance on our held-out dataset; it does not guarantee 100% accuracy on arbitrary real-world potato leaf images.**

Real-world images may contain conditions that are not adequately represented in the current dataset, including:

* Different cameras and image quality
* Different lighting conditions
* Complex backgrounds
* Different leaf orientations
* Partially visible leaves
* Multiple leaves in one image
* Different potato varieties
* Different disease severity
* Disease symptoms not represented in the dataset
* Non-potato images

For this reason, further testing on **external, real-world images** is recommended before making claims about generalization beyond the current dataset.

This limitation does not reduce the significance of the 100% result. It simply defines **what the result actually demonstrates**.

For the current MVP, the result provides strong evidence that the selected architecture and training approach are highly effective for the target classification task.

---

# 16. Final Model Configuration

```text
Model:              ResNet18
Framework:          PyTorch
Task:               3-class image classification
Input:              RGB potato leaf image
Input dimensions:   224 × 224
Output classes:     3
Optimizer:          Adam
Loss function:      CrossEntropyLoss
Training epochs:    10
Device:             CPU
```

---

# 17. Model Weights

The final best model checkpoint is stored at:

```text
ai/models/weights/potato_resnet18_best.pth
```

This is the checkpoint that should be used for inference.

The model weights are generated by the local VS Code training pipeline.

The production project does **not depend on the Google Colab runtime or Colab session**.

---

# 18. Inference

The inference logic is located at:

```text
ai/inference/predict.py
```

The primary function is:

```python
predict(image_path)
```

It accepts the path to an image and returns the prediction and confidence.

Example:

```python
from ai.inference.predict import predict

result = predict("path/to/potato_leaf.jpg")

print(result)
```

Expected output:

```python
{
    "prediction": "Potato___Early_blight",
    "confidence": 0.9916
}
```

---

# 19. Inference Output

The inference function returns:

```text
prediction
confidence
```

Example:

```json
{
    "prediction": "Potato___Early_blight",
    "confidence": 0.9916
}
```

Confidence is represented as a decimal between `0` and `1`.

For example:

```text
0.9916 = 99.16%
```

The backend or frontend can convert the confidence value to a percentage for display.

---

# 20. Tested Inference Results

The inference pipeline was manually tested using images from all three classes.

Results:

```text
==================================================
Expected: Early Blight
Prediction: Potato___Early_blight
Confidence: 99.16%

==================================================
Expected: Late Blight
Prediction: Potato___Late_blight
Confidence: 99.91%

==================================================
Expected: Healthy
Prediction: Potato___healthy
Confidence: 99.87%
```

All three manually tested images were correctly classified.

---

# 21. Class Mapping

The model uses the following class mapping:

```text
0 → Potato___Early_blight
1 → Potato___Late_blight
2 → Potato___healthy
```

For user-facing applications, these can be displayed as:

```text
Potato___Early_blight → Early Blight
Potato___Late_blight  → Late Blight
Potato___healthy      → Healthy
```

### Important

The numerical class mapping should not be changed without also updating the model/inference configuration.

---

# 22. Important Files

```text
ai/
│
├── AI_DOCUMENTATION.md
│
├── data/
│   ├── dataset.py
│   ├── preprocessing.py
│   └── raw/
│       └── Dataset/
│
├── models/
│   ├── model.py
│   └── weights/
│       └── potato_resnet18_best.pth
│
├── training/
│   ├── train.py
│   └── evaluate.py
│
└── inference/
    └── predict.py
```

### Responsibilities

| File                                      | Responsibility                             |
| ----------------------------------------- | ------------------------------------------ |
| `data/dataset.py`                         | Dataset loading, splitting and DataLoaders |
| `data/preprocessing.py`                   | Image preprocessing and transformations    |
| `models/model.py`                         | ResNet18 architecture                      |
| `models/weights/potato_resnet18_best.pth` | Trained model checkpoint                   |
| `training/train.py`                       | Model training and checkpoint saving       |
| `training/evaluate.py`                    | Test-set evaluation                        |
| `inference/predict.py`                    | Prediction on new images                   |
| `AI_DOCUMENTATION.md`                     | AI documentation and integration reference |

---

# 23. Getting Started — Reproducing the AI Pipeline

The dataset is not included in GitHub, so anyone cloning the repository must obtain it separately before training.

### 1. Clone and set up the project

```bash
git clone <REPOSITORY_URL>
cd c1-tuners-project-1

python -m venv .venv
```

Activate the environment:

**Windows**

```powershell
.venv\Scripts\activate
```

**macOS/Linux**

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

### 2. Add the dataset

Place the dataset at:

```text
ai/data/raw/Dataset/
├── Potato___Early_blight/
├── Potato___Late_blight/
└── Potato___healthy/
```

The expected dataset contains:

```text
Early Blight → 1,000 images
Late Blight  → 1,000 images
Healthy      →   152 images
Total        → 2,152 images
```

**Do not rename the class folders**, as the training pipeline expects these exact names.

---

### 3. Verify the setup

Run:

```bash
python test_data.py
```

You should see:

```text
Training images: 1506
Validation images: 323
Test images: 323
```

You can also verify the ResNet18 architecture:

```bash
python test_model.py
```

Expected output includes:

```text
Linear(in_features=512, out_features=3, bias=True)
```

---

### 4. Train the model

From the project root:

```bash
python -m ai.training.train
```

The training script trains the fine-tuned ResNet18 and automatically saves the best validation checkpoint to:

```text
ai/models/weights/potato_resnet18_best.pth
```

---

### 5. Evaluate the model

After training:

```bash
python -m ai.training.evaluate
```

This generates the test accuracy, classification report, and confusion matrix.

Current result:

```text
Test Accuracy: 100.00%
```

---

### 6. Test inference

To test the model on individual images:

```bash
python test_prediction.py
```

The model returns:

```text
Prediction: Potato___Early_blight
Confidence: 99.16%
```

---

### Reproducing the Experiments

The four experiments were conducted in Google Colab to determine the final approach:

```text
001 → CNN baseline
002 → CNN + class weighting
003 → ResNet18 feature extraction
004 → Fine-tuned ResNet18
```

The Colab notebook contains the detailed experimentation. The final model was **retrained locally in VS Code**, so Colab is not required to run the project.

### Important

The dataset is intentionally excluded from GitHub. A fresh clone therefore requires the dataset to be added manually at:

```text
ai/data/raw/Dataset/
```

The trained model checkpoint may be used directly if it is included in the repository; otherwise, the model must be trained locally before inference.


# 24. Backend Integration Guide

The backend does not need to reproduce the training process.

The backend's primary interaction with the AI component is through the inference layer.

Conceptually:

```text
User
  │
  │ Upload potato leaf image
  ▼
Backend
  │
  │ Image
  ▼
AI Inference
  │
  ▼
ResNet18
  │
  ▼
Prediction + Confidence
  │
  ▼
Backend
  │
  ▼
Frontend
```

The AI component expects an image and produces a result equivalent to:

```json
{
    "prediction": "Potato___Early_blight",
    "confidence": 0.9916
}
```

The backend can then expose this result through whatever API structure the team decides to use.

---

# 25. Backend Integration Notes

### Load the model once

The model should ideally be loaded once when the application starts rather than loading the `.pth` file for every prediction request.

### Do not train during inference

Training and inference are separate operations.

The backend should use the existing trained checkpoint:

```text
ai/models/weights/potato_resnet18_best.pth
```

### Keep preprocessing consistent

The image preprocessing used by the inference pipeline should remain consistent with the preprocessing used when training the model.

### Validate uploaded files

The backend should validate that the uploaded file is an image before passing it to the AI inference layer.

### Handle inference errors

Invalid or corrupted images should result in a controlled API error rather than causing the application to crash.

---

# 26. Current Model Scope

The current model is a **three-class potato leaf classifier**.

It can classify:

```text
Early Blight
Late Blight
Healthy
```

It does not currently provide:

* Disease severity estimation
* Treatment recommendations
* Multiple disease detection in one image
* Explicit "Not a potato leaf" classification
* General classification of other crops
* Explicit out-of-distribution detection

These can be considered future improvements.

---

# 27. Current AI Status

```text
Dataset validation           ✅
EDA                          ✅
Dataset splitting            ✅
Image preprocessing          ✅
Data augmentation            ✅
CNN baseline                 ✅
Class imbalance experiment   ✅
ResNet18 feature extraction  ✅
ResNet18 fine-tuning         ✅
Final model selection        ✅
VS Code retraining           ✅
Model checkpoint             ✅
Test evaluation              ✅
Inference pipeline            ✅
Manual inference testing     ✅
Backend integration           ⏳
Frontend integration          ⏳
External real-world testing  ⏳
```

---

# 28. Final AI Summary

```text
FINAL MODEL
────────────────────────────────
Architecture:       Fine-tuned ResNet18
Framework:          PyTorch
Classes:            3
Input:              224 × 224 RGB image
Best Val Accuracy:  100%
Test Accuracy:      100%
Test Samples:       323
Model Weights:
ai/models/weights/potato_resnet18_best.pth
```

The model was selected after four experiments:

```text
001 → CNN baseline
      98.76% Val Accuracy
      83% Healthy Recall

002 → CNN + class weighting
      97.21% Val Accuracy
      83% Healthy Recall
      Rejected

003 → ResNet18 feature extraction
      99.38% Val Accuracy
      91% Healthy Recall
      Improved

004 → Fine-tuned ResNet18
      100% Val Accuracy
      100% Healthy Recall
      100% Test Accuracy
      🏆 Selected
```

The final AI component is ready for integration with the team's backend and frontend components.
