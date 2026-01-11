from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import os

# Get the directory where server.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(os.path.join(BASE_DIR, 'logistic_regression_model.pkl'))
scaler = joblib.load(os.path.join(BASE_DIR, 'scaler_10.joblib'))

class FanInput(BaseModel):
    nfl_community_care: int
    player_credibility_social: int
    content_frequency_weekly: int  # 1-5
    content_watch_likelihood: int  # 1-4
    has_fav_team: int
    driver_game_excitement: int
    driver_fantasy: int
    barrier_no_time: int
    age: float
    gender: int

app = FastAPI()

@app.get("/")
def root():
    return {"message": "NFL Fan Engagement Prediction API"}

@app.post("/predict")
def predict(fan: FanInput):
    features = np.array([[
        fan.nfl_community_care, fan.player_credibility_social, fan.content_frequency_weekly,
        fan.content_watch_likelihood, fan.has_fav_team, fan.driver_game_excitement,
        fan.driver_fantasy, fan.barrier_no_time, fan.age, fan.gender
    ]])
    
    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)[0]
    probability = model.predict_proba(features_scaled)[0].tolist()
    
    return {
        "prediction": prediction,
        "probabilities": probability
    }