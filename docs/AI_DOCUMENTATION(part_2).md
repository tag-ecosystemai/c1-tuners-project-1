# Potato Leaf Detection & Inference Pipeline

## 1. Why We Needed a Detection Layer

The original disease classification model was trained specifically on three potato leaf classes:

* Potato Early Blight
* Potato Late Blight
* Potato Healthy

This created an important limitation.

A standard image classifier will always try to choose one of the classes it was trained on, even when the uploaded image is completely unrelated.

For example, if a user uploaded:

* A cup
* A person
* A mango leaf
* A tomato leaf

the disease classifier could still return one of the three potato classes.

This would produce a misleading result.

To address this, an additional layer was introduced before the disease classifier.

---

## 2. Initial Experiments

Several approaches were explored before settling on the final solution.

### 2.1 CLIP-Based Classification

The first approach explored using CLIP as a general-purpose image understanding model.

The idea was to compare the uploaded image against text prompts such as:

* "a clear photograph of a potato leaf"
* "a photograph of something that is not a potato leaf"

This worked reasonably well for some clearly unrelated objects.

However, it struggled with visually similar plant leaves.

Example results:

| Image       | Potato | Not Potato |
| ----------- | -----: | ---------: |
| Cup         |  8.35% |     91.65% |
| Mango leaf  | 50.04% |     49.96% |
| Person      |  8.06% |     91.94% |
| Tomato leaf | 53.84% |     46.16% |

The results showed that CLIP could distinguish obvious non-plant objects, but it was not reliable enough for distinguishing potato leaves from other plant leaves.

The mango and tomato leaf results were particularly problematic.

---

## 3. Embedding Similarity Experiment

The next approach was to use image embeddings and semantic similarity.

The idea was to create reference embeddings from potato leaf images and compare the uploaded image against those references.

A high similarity score would indicate that the image was likely a potato leaf.

However, this approach also produced unreliable results.

Some non-potato plant leaves had high similarity scores because they shared general visual characteristics with potato leaves.

For example:

* Mango leaf: `0.8633`
* Tomato leaf: `0.8984`

These scores were high enough to make similarity-based detection unreliable.

---

## 4. ResNet Embedding Experiment

A similar experiment was performed using embeddings from the ResNet18 model used for the disease classifier.

The idea was to extract visual features from the model and compare them against potato leaf reference embeddings.

This approach also failed to provide a reliable boundary between potato and non-potato leaves.

Example:

* Mango leaf: `0.8870`
* Tomato leaf: `0.9066`

The problem remained the same: visually similar plant leaves could have high similarity to potato leaves.

At this point, the embedding-based approaches were abandoned.

---

# 5. Final Approach: Dedicated Potato Leaf Detector

The final solution was to build a separate binary image classification model specifically for determining whether an uploaded image is a potato leaf.

The system now uses two independent models:

### Model 1 — Potato Leaf Detector

Classes:

```text
0 → not_potato_leaf
1 → potato_leaf
```

### Model 2 — Potato Disease Classifier

Classes:

```text
Potato___Early_blight
Potato___Late_blight
Potato___healthy
```

The two models serve different purposes.

The detector answers:

> "Is this a potato leaf?"

The disease classifier answers:

> "What condition does this potato leaf have?"

---

# 6. Detector Dataset

A separate dataset was created for the potato leaf detector.

### Potato Leaf

The potato class was created using:

* 280 Early Blight images
* 280 Late Blight images
* 152 Healthy images

Total:

```text
712 potato leaf images
```

### Not Potato Leaf

Approximately 840 non-potato images were manually collected.

These included different types of non-potato images to teach the detector what should be rejected.

The final detector dataset was split into training, validation, and test sets using stratified splitting.

---

# 7. Detector Architecture

The detector uses a pretrained ResNet18 architecture.

The ImageNet-pretrained feature extractor was frozen and the final classification layer was replaced with a binary classification head:

```text
ResNet18
   ↓
512 feature representation
   ↓
Linear(512, 2)
   ↓
not_potato_leaf / potato_leaf
```

Only the final classification layer was trained.

---

# 8. Detector Training Results

The detector was trained for 10 epochs.

The best validation accuracy achieved was:

```text
97.86%
```

The best model was saved as:

```text
ai/models/detector/potato_detector_best.pth
```

---

# 9. Held-Out Test Results

The final detector was evaluated on a held-out test set of 234 images.

Confusion matrix:

```text
[[120   7]
 [  0 107]]
```

Classification results:

| Class           | Precision |  Recall |     F1 |
| --------------- | --------: | ------: | -----: |
| Not Potato Leaf |   100.00% |  94.49% | 97.17% |
| Potato Leaf     |    93.86% | 100.00% | 96.83% |

Overall test accuracy:

```text
97.01%
```

The detector correctly identified all 107 potato leaves in the held-out test set.

It rejected 120 of 127 non-potato images.

There were:

* 7 false positives
* 0 false negatives

---

# 10. Detector Threshold

The detector uses the probability assigned to the `potato_leaf` class to determine whether the image should proceed to disease classification.

Current threshold:

```python
DETECTOR_THRESHOLD = 0.50
```

The logic is:

```text
potato_probability >= 0.50
        ↓
     Accept

potato_probability < 0.50
        ↓
     Reject
```

The 0.50 threshold was retained because it provided a strong balance between accepting genuine potato leaves and rejecting non-potato images during validation.

Higher thresholds were tested, but they caused a noticeable increase in false negatives for genuine potato leaves.

---

# 11. Final Two-Stage Inference Pipeline

The final inference pipeline is:

```text
                Uploaded Image
                      ↓
              Potato Leaf Detector
                      ↓
             Potato probability
                      ↓
              ┌───────┴───────┐
              ↓               ↓
         < 0.50            >= 0.50
              ↓               ↓
           REJECT        Disease Model
                              ↓
                    ┌─────────┼─────────┐
                    ↓         ↓         ↓
                Early      Late      Healthy
                Blight     Blight
```

The disease classifier is **only executed when the detector accepts the image as a potato leaf**.

This prevents the disease model from directly classifying obviously unrelated images.

---

# 12. Final Inference Output

The inference function is:

```python
predict(image_path)
```

For an accepted potato leaf, it returns:

```json
{
  "is_potato_leaf": true,
  "potato_probability": 0.984,
  "not_potato_probability": 0.016,
  "prediction": "Potato___Late_blight",
  "confidence": 0.978,
  "confidence_level": "high",
  "explanation": "...",
  "recommendation": "..."
}
```

For a rejected image:

```json
{
  "is_potato_leaf": false,
  "potato_probability": 0.379,
  "not_potato_probability": 0.621,
  "prediction": null,
  "confidence": null,
  "confidence_level": null,
  "explanation": "This image does not appear to be a potato leaf, so the disease classifier was not used.",
  "recommendation": "Please upload a clear photo of a potato leaf. Try to make sure the leaf is clearly visible and well lit."
}
```

---

# 13. Explanation and Recommendation Layer

The inference pipeline also provides a user-friendly explanation and recommendation based on the disease prediction and confidence score.

Confidence is divided into three levels:

```text
90% – 100%  → High
70% – 89%   → Moderate
50% – 69%   → Low
```

Each disease has different explanation and recommendation content for each confidence level.

This allows the system to communicate uncertainty appropriately.

For example, a 98% prediction can be communicated more confidently than a 55% prediction.

The explanations are rule-based and do not require an external LLM.

The current explanation system is implemented in:

```text
ai/inference/explanations.py
```

The prediction pipeline is implemented in:

```text
ai/inference/predict.py
```

---

# 14. External Testing

The final pipeline was tested against images outside the original disease dataset.

The test categories included:

```text
cup
mango_leaf
person
tomato_leaf
```

Results:

| Image       | Potato Probability | Decision |
| ----------- | -----------------: | -------- |
| Cup         |             33.84% | Rejected |
| Mango Leaf  |             62.93% | Accepted |
| Person      |             22.32% | Rejected |
| Tomato Leaf |             37.93% | Rejected |

The detector successfully rejected the cup, person, and tomato leaf.

However, the mango leaf was incorrectly accepted with a potato probability of 62.93%.

This is a known limitation of the current detector.

---

# 15. Known Limitation

The detector is designed primarily to prevent clearly unrelated images from reaching the disease classifier.

It is **not a universal plant-species identification model**.

Some visually similar plant leaves may still be classified as potato leaves.

For example, during external testing, a mango leaf was accepted by the detector.

This limitation is currently accepted for the MVP because the product is explicitly designed for **potato leaf images**.

The upload interface should therefore clearly communicate that users should submit photos of potato leaves.

The limitation should also be considered when interpreting predictions.

---

# 16. Why We Kept the Detector

Although the detector is not perfect, it significantly improves the original system architecture.

Without the detector:

```text
Any image
   ↓
Disease classifier
   ↓
Always returns one of three potato diseases
```

With the detector:

```text
Any image
   ↓
Potato detector
   ↓
Reject unrelated images
        OR
   ↓
Disease classifier
```

This prevents the disease classifier from being blindly applied to every uploaded image.

---

# 17. Current AI Pipeline Status

The following components are now complete:

* Potato disease classification
* Potato leaf detection
* Two-stage inference pipeline
* Confidence scoring
* Confidence-aware explanations
* Confidence-aware recommendations
* External inference testing

The next major AI task is **Grad-CAM explainability**.

Grad-CAM will provide a visual explanation of the disease classifier's prediction by showing the regions of the leaf that contributed most strongly to the model's decision.

The intended final system will therefore provide:

```text
Prediction
    ↓
Confidence
    ↓
Human-readable explanation
    ↓
Recommendation
    ↓
Grad-CAM visual explanation
```

---

# 18. Files Relevant to the Final Pipeline

The main files required for the current AI pipeline are:

```text
ai/
├── data/
│   ├── dataset.py
│   ├── detector_dataset.py
│   └── preprocessing.py
│
├── inference/
│   ├── explanations.py
│   └── predict.py
│
├── models/
│   ├── model.py
│   ├── weights/
│   │   └── potato_resnet18_best.pth
│   └── detector/
│       └── potato_detector_best.pth
│
└── training/
    ├── train.py
    ├── train_detector.py
    ├── evaluate.py
    ├── evaluate_detector.py
    └── analyze_detector_threshold.py
```

The CLIP and embedding-based experiments are no longer part of the production inference pipeline.
