import streamlit as st
import requests

st.title("🏈 NFL Fan Engagement Predictor")
st.write("Answer a few questions to predict your NFL engagement level!")

# API URL
API_URL = "https://nflfanlevel.onrender.com/predict"

# Collect inputs with friendly labels
col1, col2 = st.columns(2)

with col1:
    age = st.slider("Age", 18, 80, 30)
    gender = st.selectbox("Gender", ["Female", "Male"])
    has_fav_team = st.selectbox("Do you have a favorite NFL team?", ["No", "Yes"])
    has_fav_player = st.selectbox("Do you have a favorite NFL player?", ["No", "Yes"])
    watched_in_person = st.selectbox("Have you watched a game in person?", ["No", "Yes"])
    intro_friends = st.selectbox("Were you introduced to NFL by friends?", ["No", "Yes"])
    driver_game_excitement = st.selectbox("Do you enjoy the excitement of games?", ["No", "Yes"])
    driver_fantasy = st.selectbox("Do you play fantasy football?", ["No", "Yes"])
    driver_never_interested = st.selectbox("Have you never been interested in NFL?", ["No", "Yes"])
    aware_play60 = st.selectbox("Are you aware of NFL Play 60?", ["No", "Yes"])

with col2:
    nfl_community_care = st.selectbox("Do you believe NFL cares about community?", ["No", "Yes"])
    nfl_supports_mental = st.selectbox("Do you believe NFL supports mental health?", ["No", "Yes"])
    nfl_supports_emotional = st.selectbox("Do you believe NFL supports emotional wellbeing?", ["No", "Yes"])
    player_credibility_social = st.selectbox("Do you trust players on social issues?", ["No", "Yes"])
    content_frequency_weekly = st.selectbox("Do you watch NFL content weekly?", ["No", "Yes"])
    content_watch_likelihood = st.selectbox("Are you likely to watch NFL content?", ["No", "Yes"])
    barrier_other_sports = st.selectbox("Do other sports prevent you from watching NFL?", ["No", "Yes"])
    barrier_no_time = st.selectbox("Does lack of time prevent you from watching?", ["No", "Yes"])
    race_white = st.selectbox("Race: White?", ["No", "Yes"])
    race_pacific_islander = st.selectbox("Race: Pacific Islander?", ["No", "Yes"])

# Convert Yes/No to 1/0
def to_int(val):
    return 1 if val == "Yes" else 0

if st.button("Predict Engagement Level", type="primary"):
    payload = {
        "nfl_community_care": to_int(nfl_community_care),
        "player_credibility_social": to_int(player_credibility_social),
        "content_frequency_weekly": to_int(content_frequency_weekly),
        "content_watch_likelihood": to_int(content_watch_likelihood),
        "has_fav_team": to_int(has_fav_team),
        "has_fav_player": to_int(has_fav_player),
        "aware_play60": to_int(aware_play60),
        "intro_friends": to_int(intro_friends),
        "driver_never_interested": to_int(driver_never_interested),
        "driver_game_excitement": to_int(driver_game_excitement),
        "driver_fantasy": to_int(driver_fantasy),
        "barrier_other_sports": to_int(barrier_other_sports),
        "barrier_no_time": to_int(barrier_no_time),
        "nfl_supports_mental": to_int(nfl_supports_mental),
        "nfl_supports_emotional": to_int(nfl_supports_emotional),
        "watched_in_person": to_int(watched_in_person),
        "age": age,
        "race_pacific_islander": to_int(race_pacific_islander),
        "race_white": to_int(race_white),
        "gender": to_int(gender)
    }
    
    try:
        response = requests.post(API_URL, json=payload)
        result = response.json()
        
        st.success(f"### Predicted Engagement: {result['prediction']}")
        
        st.write("**Probabilities:**")
        probs = result['probabilities']
        st.write(f"- High: {probs[0]:.1%}")
        st.write(f"- Low: {probs[1]:.1%}")
        st.write(f"- Medium: {probs[2]:.1%}")
        
    except Exception as e:
        st.error(f"Error: {e}")
