import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes.prediction import router as prediction_router

app = FastAPI(title="Team Tuner API")

default_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

allowed_origins_env = os.getenv("CORS_ALLOW_ORIGINS")
allowed_origins = default_origins
if allowed_origins_env:
    parsed_origins = [
        origin.strip()
        for origin in allowed_origins_env.split(",")
        if origin.strip()
    ]
    if parsed_origins:
        allowed_origins = parsed_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prediction_router)


@app.get("/")
def root():
    return {"message": "Team Tuner API is running"}