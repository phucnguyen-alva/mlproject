import streamlit as st
import requests

st.title("🏈 NFL Fan Engagement Predictor")
st.write("Answer a few questions to predict your NFL engagement level!")

API_URL = "https://nflfanlevel.onrender.com/predict"

col1, col2 = st.columns(2)

with col1:
    age = st.slider("Age", 18, 80, 30)
    gender = st.selectbox("Gender", ["Female", "Male"])
    has_fav_team = st.selectbox("Do you have a favorite NFL team?", ["No", "Yes"])
    driver_game_excitement = st.selectbox("Do you enjoy the excitement of games?", ["No", "Yes"])
    driver_fantasy = st.selectbox("Do you play fantasy football?", ["No", "Yes"])

with col2:
    nfl_community_care = st.selectbox("Do you believe NFL cares about community?", ["No", "Yes"])
    player_credibility_social = st.selectbox("Do you trust players on social issues?", ["No", "Yes"])
    content_frequency_weekly = st.selectbox("Do you watch NFL content weekly?", ["No", "Yes"])
    content_watch_likelihood = st.selectbox("Are you likely to watch NFL content?", ["No", "Yes"])
    barrier_no_time = st.selectbox("Does lack of time prevent you from watching?", ["No", "Yes"])

def to_int(val):
    return 1 if val == "Yes" else 0

if st.button("Predict Engagement Level", type="primary"):
    payload = {
        "nfl_community_care": to_int(nfl_community_care),
        "player_credibility_social": to_int(player_credibility_social),
        "content_frequency_weekly": to_int(content_frequency_weekly),
        "content_watch_likelihood": to_int(content_watch_likelihood),
        "has_fav_team": to_int(has_fav_team),
        "driver_game_excitement": to_int(driver_game_excitement),
        "driver_fantasy": to_int(driver_fantasy),
        "barrier_no_time": to_int(barrier_no_time),
        "age": age,
        "gender": 1 if gender == "Male" else 0
    }
    
    with st.spinner("Predicting..."):
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

