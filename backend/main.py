from fastapi import FastAPI

from backend.routes.prediction import router as prediction_router


app = FastAPI(title="Team Tuner API")

app.include_router(prediction_router)


@app.get("/")
def root():
    return {"message": "Team Tuner API is running"}