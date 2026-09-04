# Team Tuner API — Backend

This directory contains the FastAPI backend for the Team Tuner potato leaf classification application.

The backend exposes the AI inference pipeline through a REST API, allowing the frontend application to upload an image and receive a structured prediction response.

## Overview

The backend connects the React frontend to the existing AI inference pipeline:

```text
Frontend
   │
   │ POST /predict
   │ image file
   ▼
FastAPI Backend
   │
   ▼
AI Inference Pipeline
   │
   ├── Potato Leaf Detector
   │       │
   │       ├── Not a potato leaf → Reject
   │       │
   │       └── Potato leaf
   │              ↓
   │        Disease Classifier
   │
   ▼
Prediction Response
   │
   ├── Detection result
   ├── Probabilities
   ├── Disease prediction
   ├── Confidence
   ├── Confidence level
   ├── Explanation
   └── Recommendation
```

## Project Structure

The relevant backend structure is:

```text
backend/
├── routes/
│   ├── __init__.py
│   └── prediction.py
├── schemas/
│   ├── __init__.py
│   └── prediction.py
├── __init__.py
└── main.py
```

The backend uses the existing AI modules under `ai/` for model inference. The backend does not retrain or modify the models.

## Requirements

The backend requires:

- Python 3.10+
- The dependencies listed in the project's `requirements.txt`

The trained model weights required for inference are included in the repository as part of the AI pipeline.

## Running the Backend Locally

### 1. Clone the repository

If you do not already have the project locally:

```bash
git clone <repository-url>
cd c1-tuners-project-1
```

If you already have the repository, simply navigate to the project root:

```bash
cd c1-tuners-project-1
```

### 2. Create a virtual environment

From the project root:

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

On Windows:

```bash
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

### 4. Install dependencies

From the project root:

```bash
pip install -r requirements.txt
```

### 5. Start the FastAPI server

Run the following command from the **project root**:

```bash
uvicorn backend.main:app --reload
```

The `--reload` option automatically restarts the server when backend source files are changed during development.

Once the server starts successfully, the API will be available at:

```text
http://127.0.0.1:8000
```

> **Important:** Run the command from the project root rather than from inside the `backend/` directory. The backend imports modules from the project's `ai/` package.

## API Documentation

FastAPI automatically provides interactive API documentation through Swagger UI.

Once the backend is running, open:

```text
http://127.0.0.1:8000/docs
```

You can use the Swagger interface to inspect the available endpoints and send test requests directly to the API.

The alternative ReDoc documentation is available at:

```text
http://127.0.0.1:8000/redoc
```

## Prediction Endpoint

### `POST /predict`

The `/predict` endpoint accepts an image file and passes it through the two-stage AI inference pipeline.

The endpoint expects:

```text
multipart/form-data
```

with an image uploaded through the `file` field.

Supported image formats:

- JPEG
- PNG
- WebP

### Request flow

```text
Uploaded Image
      │
      ▼
Potato Leaf Detector
      │
      ├── Not a potato leaf
      │       ↓
      │     Reject
      │
      └── Potato leaf
              ↓
       Disease Classifier
              ↓
       Prediction Response
```

### Response

A successful response contains information such as:

```json
{
  "is_potato_leaf": true,
  "potato_probability": 0.66,
  "not_potato_probability": 0.34,
  "prediction": "Potato___healthy",
  "confidence": 0.98,
  "confidence_level": "high",
  "explanation": "The model is highly confident that this potato leaf appears healthy.",
  "recommendation": "Continue monitoring the plant regularly."
}
```

For an image rejected by the potato leaf detector, the disease classifier is not run. The response instead contains the detection probabilities together with an explanation and recommendation:

```json
{
  "is_potato_leaf": false,
  "potato_probability": 0.32,
  "not_potato_probability": 0.68,
  "prediction": null,
  "confidence": null,
  "confidence_level": null,
  "explanation": "This image does not appear to be a potato leaf, so the disease classifier was not used.",
  "recommendation": "Please upload a clear photo of a potato leaf."
}
```

## Testing the API Locally

### Using Swagger UI

1. Start the backend:

   ```bash
   uvicorn backend.main:app --reload
   ```

2. Open:

   ```text
   http://127.0.0.1:8000/docs
   ```

3. Expand `POST /predict`.

4. Click **Try it out**.

5. Upload a JPEG, PNG, or WebP image.

6. Click **Execute**.

7. Inspect the returned prediction response.

A potato leaf image should proceed through the disease classifier.

A non-potato image should be rejected by the potato leaf detector without proceeding to disease classification.

### Using the API from the frontend

The React frontend will communicate with the backend through:

```text
POST http://127.0.0.1:8000/predict
```

The frontend should send the selected image as multipart form data using the field name:

```text
file
```

The returned JSON response can then be used to display the prediction, confidence, explanation, recommendation, and image acceptance status.

## Running the Backend with the Frontend

During local development, the backend and frontend run as separate applications.

The backend runs on:

```text
http://127.0.0.1:8000
```

The React development server will run on its own local port, typically:

```text
http://localhost:5173
```

Both applications should be running simultaneously for the complete application to work end-to-end.

Start the backend from the project root:

```bash
uvicorn backend.main:app --reload
```

Then start the frontend using the frontend project's configured development command.

## Stopping the Backend

To stop the local FastAPI server, return to the terminal running Uvicorn and press:

```text
CTRL + C
```

## Notes

The backend is responsible for exposing the existing AI inference pipeline through an HTTP API. The current inference pipeline first determines whether an uploaded image is a potato leaf. Disease classification is performed only when the image is accepted by the detector.

Likewise, the backend currently exposes the AI prediction functionality required for frontend integration. 