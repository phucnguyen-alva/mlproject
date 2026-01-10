from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

model = joblib.load('model_20.joblib')
scaler = joblib.load('scaler_20.joblib')

class FanInput(BaseModel):
    nfl_community_care: int
    player_credibility_social: int
    content_frequency_weekly: int
    content_watch_likelihood: int
    has_fav_team: int
    has_fav_player: int
    aware_play60: int
    intro_friends: int
    driver_never_interested: int
    driver_game_excitement: int
    driver_fantasy: int
    barrier_other_sports: int
    barrier_no_time: int
    nfl_supports_mental: int
    nfl_supports_emotional: int
    watched_in_person: int
    age: float
    race_pacific_islander: int
    race_white: int
    gender: int

app = FastAPI()

@app.get("/")
def root():
    return {"message": "NFL Fan Engagement Prediction API"}

@app.post("/predict")
def predict(fan: FanInput):
    features = np.array([[
        fan.nfl_community_care, fan.player_credibility_social, fan.content_frequency_weekly,
        fan.content_watch_likelihood, fan.has_fav_team, fan.has_fav_player, fan.aware_play60,
        fan.intro_friends, fan.driver_never_interested, fan.driver_game_excitement,
        fan.driver_fantasy, fan.barrier_other_sports, fan.barrier_no_time,
        fan.nfl_supports_mental, fan.nfl_supports_emotional, fan.watched_in_person,
        fan.age, fan.race_pacific_islander, fan.race_white, fan.gender
    ]])
    
    features_scaled = scaler.transform(features)
    
    prediction = model.predict(features_scaled)[0]
    probability = model.predict_proba(features_scaled)[0].tolist()
    
    return {
        "prediction": prediction,
        "probabilities": probability
    }