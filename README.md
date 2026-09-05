# TAG AI Engineering Bootcamp — Cohort 1

## Team Tuner — Project 1

### Agriculture Crop & Produce Image Inspector

An AI-powered computer vision system that analyzes crop images to determine whether an image contains a potato leaf and, when applicable, identify its health condition.

The system currently focuses on three potato leaf classes:

* **Healthy**
* **Early Blight**
* **Late Blight**

This project is being developed by **Team Tuner** as part of the TAG AI Engineering Bootcamp Cohort 1.

---

## Project Overview

The Agriculture Crop & Produce Image Inspector is designed to provide a simple way for users to inspect potato leaves using computer vision.

The system:

1. Accepts a crop or leaf image.
2. Determines whether the image is a potato leaf.
3. Classifies the potato leaf condition.
4. Returns a confidence score.
5. Provides a simple explanation and recommendation.
6. Supports visual model explainability through Grad-CAM (In-progress). 

---

## Tech Stack

* **Python**
* **PyTorch**
* **Torchvision**
* **ResNet18**
* **FastAPI**
* **Streamlit**
* **Pillow**
* **Git & GitHub**

---

## Project Structure

```text
c1-tuners-project-1/
│
├── ai/                    # AI/ML implementation
│   ├── data/              # Dataset and preprocessing
│   ├── inference/         # Prediction and explanations
│   ├── models/            # Model architecture and weights
│   ├── training/          # Training scripts
│   └── utils/             # Supporting utilities
│
├── backend/               # FastAPI backend
├── frontend/              # Frontend application
├── docs/                  # Project documentation
├── tests/                 # Tests
│
├── app.py                 # Streamlit application
├── requirements.txt       # Python dependencies
└── README.md              # Project overview
```

---

## Documentation

Detailed AI/ML documentation can be found in the `docs/` directory.

* [AI Documentation — Part 1](docs/AI_DOCUMENTATION%28part_1%29.md)
* [AI Documentation — Part 2](docs/AI_DOCUMENTATION%28part_2%29.md)

These documents contain the detailed information about the dataset, preprocessing, model development, experiments, evaluation, inference and other AI/ML decisions made throughout the project.

---

## Running Locally

Clone the repository:

```bash
git clone https://github.com/tag-ecosystemai/c1-tuners-project-1.git
cd c1-tuners-project-1
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it and install the dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
streamlit run app.py
```

---

## Team Workflow

1. Create a branch before working on a feature or task.
2. Do not work directly on `main`.
3. Push changes to your branch.
4. Open a pull request when the work is ready.
5. Have another team member review the pull request.
6. Merge only after review and testing.
7. Keep commit messages clear and descriptive.
8. Never commit passwords, API keys, tokens or other secrets.

---

## Team Members

* Fawaz Bello
* Emmanuel Akanbi
* Israel Adeoti
* OYETUNJI SHUKRAH
* John Confidence Bello
* Adeniran Treasure

## Mentor

**Bayzman**

---

## Programme

**TAG AI Engineering Bootcamp — Cohort 1**
