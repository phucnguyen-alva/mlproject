# 🏈 NFL Fan Engagement Predictor

A machine learning-powered web application that predicts NFL fan engagement levels based on viewing habits, team loyalty, and league sentiment. Built as part of the MSU Foundations of AI (FoAI9) course project.

---

## 🌐 Live Demo

- **Web App:** [nflfanquiz.streamlit.app](https://nflfantype.streamlit.app)
- **API Docs:** [nflfanlevel.onrender.com/docs](https://nflfanlevel.onrender.com/docs)

---

## 📖 Project Overview

This project develops an end-to-end machine learning pipeline to classify NFL fans into three engagement tiers:

| Tier | Description |
|------|-------------|
| **Avid Fan** | Highly engaged, consumes content daily, plays fantasy football |
| **Casual Fan** | Moderate engagement, watches games socially, follows highlights |
| **Non-fan** | Low engagement, new to football, potential growth audience |

The classification model helps the NFL strategically target content and community programs to different audience segments, supporting youth health & wellness initiatives like Play 60, NFL FLAG, and Character Playbook.

---

## ✨ Features

- **Interactive Quiz Interface** — NFL broadcast-style UI with engaging questions
- **Real-time Predictions** — FastAPI backend serves predictions via REST API
- **Personalized Resources** — Curated NFL programs and content based on fan tier
- **Downloadable Results** — Export your fan profile as a report card
- **Mobile Responsive** — Optimized for all screen sizes

---

## 🛠️ Tech Stack

### Machine Learning
- **Model:** Logistic Regression with balanced class weights
- **Feature Selection:** Recursive Feature Elimination (RFE) → 10 features
- **Preprocessing:** StandardScaler normalization
- **Framework:** scikit-learn 1.6.1

### Backend
- **API:** FastAPI with Pydantic validation
- **Server:** Uvicorn ASGI
- **Hosting:** Render.com

### Frontend
- **Framework:** Streamlit
- **Styling:** Custom CSS (NFL broadcast design system)
- **Hosting:** Streamlit Cloud

---

## 📁 Project Structure

```
mlproject/
├── notebooks/                    # Jupyter notebooks for exploration & training
│   └── model_training.ipynb
├── src/                          # API source code
│   ├── server.py                 # FastAPI application
│   ├── model_10.joblib           # Trained model (10 features)
│   └── scaler_10.joblib          # Fitted StandardScaler
├── app/                          # Streamlit frontend
│   ├── app.py                    # Main application
│   └── .streamlit/
│       └── config.toml           # Streamlit configuration
├── requirements.txt              # Python dependencies
└── README.md
```

---

## 🤖 Model Details

### Selected Features (10)

| Category | Features |
|----------|----------|
| **Demographics** | `age`, `gender` |
| **Engagement** | `content_frequency_weekly`, `content_watch_likelihood` |
| **Loyalty** | `has_fav_team`, `driver_game_excitement`, `driver_fantasy` |
| **Barriers** | `barrier_no_time` |
| **Perception** | `nfl_community_care`, `player_credibility_social` |

### Performance

| Metric | Score |
|--------|-------|
| Accuracy | ~74% |
| Class Balance | Balanced weights applied |

### Class Distribution (Training Data)

| Class | Count | Percentage |
|-------|-------|------------|
| Casual Fan | 453 | 49.2% |
| Avid Fan | 311 | 33.8% |
| Non-fan | 156 | 17.0% |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/phucnguyen-alva/mlproject.git
cd mlproject

# Install dependencies
pip install -r requirements.txt
```

### Run Locally

**Terminal 1 — Start API:**
```bash
uvicorn src.server:app --reload --port 8000
```

**Terminal 2 — Start Frontend:**
```bash
streamlit run app/app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📡 API Documentation

### Base URL
```
https://nflfanlevel.onrender.com
```

### Endpoints

#### `GET /`
Health check endpoint.

**Response:**
```json
{
  "message": "NFL Fan Engagement Prediction API"
}
```

#### `POST /predict`
Predict fan engagement level.

**Request Body:**
```json
{
  "nfl_community_care": 1,
  "player_credibility_social": 1,
  "content_frequency_weekly": 3,
  "content_watch_likelihood": 4,
  "has_fav_team": 1,
  "driver_game_excitement": 1,
  "driver_fantasy": 1,
  "barrier_no_time": 0,
  "age": 28,
  "gender": 1
}
```

**Response:**
```json
{
  "prediction": "Avid Fan",
  "probabilities": [0.65, 0.25, 0.10]
}
```

**Probability Index:**
- `[0]` = Avid Fan
- `[1]` = Casual Fan
- `[2]` = Non-fan

---

## 🎯 Strategic Value

This project supports the NFL's youth health & wellness initiatives by:

1. **Segmenting Audiences** — Identify engagement levels to personalize outreach
2. **Promoting Programs** — Surface relevant NFL initiatives (Play 60, FLAG, Inspire Change)
3. **Growing the Fanbase** — Convert Non-fans and Casual Fans with targeted content
4. **Measuring Impact** — Track engagement shifts over time

### Program Allocation by Tier

| Tier | Recommended Programs |
|------|---------------------|
| **Avid Fan** | NFL Foundation, Inspire Change, Sunday Ticket |
| **Casual Fan** | NFL FLAG, Character Playbook, RedZone, Fantasy |
| **Non-fan** | Play 60, FLAG In Schools, Football 101, Top 100 Plays |

---

## 🔮 Future Improvements

- [ ] Add more demographic features (location, ethnicity)
- [ ] Implement A/B testing for resource recommendations
- [ ] Build admin dashboard for engagement analytics
- [ ] Integrate with NFL API for real-time content suggestions
- [ ] Add multilingual support (Spanish) for broader reach

---

## 📚 References

- [NFL Community Programs](https://www.nfl.com/causes/)
- [scikit-learn Documentation](https://scikit-learn.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

## 👤 Author

**Nguyen Minh Phuc (Alva)**  
January 2026

---

## 📄 License

This project is for educational purposes as part of coursework.

---

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/en/thumb/a/a2/National_Football_League_logo.svg/250px-National_Football_League_logo.svg.png" width="60" alt="NFL Logo">
</p>