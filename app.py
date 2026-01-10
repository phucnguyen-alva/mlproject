import streamlit as st
st.set_page_config(
    page_title="NFL Fan Quiz",
    page_icon="🏈",
    layout="centered"
)

import requests
import time

# -----------------------------------------------------------------------------
# NFL BROADCAST DESIGN SYSTEM (CSS)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Import Sports Broadcast Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;700&family=Roboto+Condensed:wght@400;700&family=Teko:wght@300;400;600;700&display=swap');
    :root {
        --nfl-blue: #013369;
        --nfl-red: #D50A0A;
        --bg-dark: #0b0f19;
    }

    /* Global Reset */
    * {
        font-family: 'Roboto Condensed', sans-serif;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Oswald', sans-serif;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Main App Background - Stadium Night Feel */
    .stApp {
        background-color: var(--bg-dark);
        background-image: 
            radial-gradient(circle at 50% 0%, #1a2c4e 0%, transparent 60%),
            linear-gradient(0deg, rgba(0,0,0,0.8) 0%, transparent 100%),
            url("data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23ffffff' fill-opacity='0.03' fill-rule='evenodd'%3E%3Cpath d='M0 40L40 0H20L0 20M40 40V20L20 40'/%3E%3C/g%3E%3C/svg%3E");
    }

    .block-container {
        max-width: 900px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* --- HERO HEADER --- */
    .nfl-header-container {
        /* Flexbox aligns them side-by-side */
        display: flex;
        align-items: center; /* Vertically centers them */
        justify-content: center; /* Horizontally centers the whole unit */
        
        padding: 2rem 0;
        border-bottom: 2px solid var(--nfl-blue);
        margin-bottom: 2rem;
        background: linear-gradient(180deg, rgba(1,51,105,0.2) 0%, transparent 100%);
    }

    .nfl-logo-img {
        width: 90px; /* Slightly larger to anchor the unit */
        height: auto;
        z-index: 2; /* IMPORTANT: sits ON TOP of the text bar */
        filter: drop-shadow(0 0 10px rgba(0,0,0,0.5)); /* darker shadow for pop */
    }

    .nfl-subtitle-broadcast {
        /* 1. Typography */
        font-family: 'Oswald', sans-serif;
        font-size: 2rem; 
        font-weight: 700;
        text-transform: uppercase;
        color: white;
        font-style: italic;
        letter-spacing: 1px;
        
        /* 2. The "Fade From Left" Effect */
        /* Starts transparent, goes to red at 15%, stays red */
        background: linear-gradient(90deg, 
            transparent 0%, 
            var(--nfl-red) 25% 
        );
        
        /* 3. Positioning & Shape */
        padding: 5px 40px 5px 60px; /* Big left padding pushes text past the fade area */
        margin-left: -40px; /* Pulls the bar underneath the Logo */
        
        transform: skewX(-15deg); /* The sporty angle */
        
        /* 4. Polish */
        border-bottom: 2px solid rgba(0,0,0,0.3); /* dark line under bar */
        text-shadow: 2px 2px 0px rgba(0,0,0,0.5); /* readable text */
        }
        
        /* 2. The Shape & Angle */
        transform: skewX(-20deg); /* Matches the angle in your image */
        padding: 5px 30px; /* More breathing room on sides */
        display: inline-block;
        
        /* 3. The "Sleek" Texture (The Fix) */
        /* Instead of flat red, use a gradient to look like glossy plastic/metal */
        background: linear-gradient(170deg, #ff1a1a 0%, #a60000 80%);
        
        /* 4. The Finish */
        border-top: 2px solid rgba(255,255,255,0.3); /* Top highlight */
        border-bottom: 2px solid rgba(0,0,0,0.3); /* Bottom shadow */
        box-shadow: 5px 5px 0px rgba(0,0,0,0.8); /* Hard drop shadow for depth */
        }

    /* Un-skew the text so it's readable */
    .nfl-subtitle-broadcast span { 
        display: block;
        transform: skewX(20deg); 
    }

    /* --- SECTION HEADERS --- */
    /* Fixed alignment issue here by increasing padding-left */
    h3 {
        color: white !important;
        background: linear-gradient(90deg, var(--nfl-blue) 0%, transparent 90%);
        padding: 10px 15px 10px 25px !important; /* Increased left padding */
        border-left: 6px solid var(--nfl-red);
        font-size: 1.2rem !important;
        clip-path: polygon(0 0, 95% 0, 100% 100%, 0% 100%);
        margin-top: 2rem !important;
        margin-bottom: 1.5rem !important;
    }

    /* --- INPUT WIDGETS --- */
    .stSlider label, .stSelectbox label {
        color: #a0c0e0 !important;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.9rem !important;
        margin-bottom: 0.5rem;
    }

    /* Customizing the slider track */
    .stSlider > div > div > div > div {
        background-color: var(--nfl-blue) !important;
    }
    .stSlider > div > div > div > div > div {
        background-color: var(--nfl-red) !important;
    }
    
    /* Dropdown text color fix */
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #151b2b !important;
        border: 1px solid #2d3b55 !important;
        color: white !important;
    }

    /* --- ACTION BUTTON --- */
    .stButton > button {
        background: linear-gradient(92deg, var(--nfl-blue) 0%, #004aad 100%);
        color: white;
        font-family: 'Oswald', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        padding: 0.75rem 2rem;
        border: 2px solid transparent;
        border-radius: 4px;
        box-shadow: 0 4px 15px rgba(1, 51, 105, 0.5);
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 1.5rem;
        clip-path: polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px);
    }
    
    .stButton > button:hover {
        background: var(--nfl-red);
        box-shadow: 0 0 25px rgba(213, 10, 10, 0.6);
        transform: scale(1.02);
        border-color: white;
    }

    /* --- PLAYER CARD RESULT --- */
    @keyframes cardReveal {
        0% { opacity: 0; transform: perspective(1000px) rotateX(20deg) translateY(50px); }
        100% { opacity: 1; transform: perspective(1000px) rotateX(0deg) translateY(0); }
    }

    .player-card {
        background: linear-gradient(135deg, #1a1f2e 0%, #0e121b 100%);
        border: 1px solid #333;
        border-top: 4px solid var(--card-accent);
        border-radius: 8px;
        padding: 0;
        margin-top: 2rem;
        position: relative;
        overflow: hidden;
        animation: cardReveal 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    }

    .card-header {
        padding: 2rem;
        text-align: center;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        z-index: 1;
        position: relative;
    }

    .card-rank {
        font-family: 'Teko', sans-serif;
        font-size: 1.2rem;
        letter-spacing: 0.3em;
        color: #888;
        text-transform: uppercase;
        display: block;
        margin-bottom: 0.5rem;
    }

    .card-title {
        font-family: 'Oswald', sans-serif;
        font-size: 3.5rem;
        line-height: 1;
        font-weight: 700;
        text-transform: uppercase;
        margin: 0;
        background: linear-gradient(180deg, #fff 0%, #ccc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Tiers Colors */
    .tier-high { --card-accent: #FFD700; }
    .tier-high .card-title { background: linear-gradient(180deg, #FFD700 0%, #B8860B 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    
    .tier-medium { --card-accent: #C0C0C0; }
    .tier-medium .card-title { background: linear-gradient(180deg, #fff 0%, #aaa 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    
    .tier-low { --card-accent: #CD7F32; }
    .tier-low .card-title { background: linear-gradient(180deg, #CD7F32 0%, #8B4513 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

    .card-body {
        padding: 2rem;
        color: #ccc;
        font-size: 1rem;
        line-height: 1.6;
        background: rgba(0,0,0,0.2);
    }

    /* --- STAT BARS --- */
    .stat-row {
        display: flex;
        align-items: center;
        margin-bottom: 0.8rem;
    }
    .stat-label {
        width: 80px;
        font-family: 'Oswald', sans-serif;
        color: #666;
        font-size: 0.9rem;
    }
    .stat-track {
        flex-grow: 1;
        height: 8px;
        background: #000;
        margin: 0 15px;
        transform: skewX(-20deg);
    }
    .stat-fill {
        height: 100%;
        background: var(--card-accent);
        box-shadow: 0 0 10px var(--card-accent);
    }
    .stat-val {
        width: 40px;
        text-align: right;
        font-family: 'Teko', sans-serif;
        font-size: 1.2rem;
        color: white;
    }

    /* --- RESOURCES --- */
    .resource-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 15px;
        margin-top: 1.5rem;
    }
    .resource-box {
        background: linear-gradient(135deg, #151b2b 0%, #0b0f19 100%);
        border: 1px solid #2d3b55;
        padding: 1rem;
        transition: transform 0.2s;
        border-left: 3px solid transparent;
    }
    .resource-box:hover {
        transform: translateY(-3px);
        border-left: 3px solid var(--nfl-red);
        border-color: white;
    }
    .resource-title {
        color: white;
        font-family: 'Oswald', sans-serif;
        font-size: 1.1rem;
        margin-bottom: 0.3rem;
    }
    .resource-link {
        color: var(--nfl-red);
        font-weight: 700;
        text-transform: uppercase;
        font-size: 0.8rem;
        text-decoration: none;
        display: block;
        margin-top: 0.5rem;
    }

    /* --- MOBILE RESPONSIVENESS --- */
    @media (max-width: 640px) {
        .nfl-logo-img { width: 60px; }
        .nfl-subtitle-broadcast { font-size: 1.1rem; letter-spacing: 0.1rem; }
        .card-title { font-size: 2.5rem; }
        .player-card::before { font-size: 2rem; }
        .resource-container { grid-template-columns: 1fr; }
        h3 { font-size: 1rem !important; padding-left: 20px !important; }
    }

    /* Hide standard streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# APP LAYOUT
# -----------------------------------------------------------------------------

# Broadcast Header with Logo
st.markdown("""
<div class='nfl-header-container'>
    <img src="https://upload.wikimedia.org/wikipedia/en/thumb/a/a2/National_Football_League_logo.svg/250px-National_Football_League_logo.svg.png" class="nfl-logo-img">
    <div class='nfl-subtitle-broadcast'>What kind of NFL Fan are you?</div>
</div>
""", unsafe_allow_html=True)

API_URL = "https://nflfanlevel.onrender.com/predict"

# Use columns for desktop, stacks automatically on mobile
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### Player Stats")
    age = st.slider("How old are you?", 18, 80, 30)
    gender = st.selectbox("Gender", ["Female", "Male"])
    
    st.markdown("### Team Loyalty")
    has_fav_team = st.selectbox("Do you ride or die for a team?", ["Nope", "You know it!"])
    driver_game_excitement = st.selectbox("Does game day get your heart racing?", ["Not really", "Absolutely!"])
    driver_fantasy = st.selectbox("Are you a fantasy football manager?", ["No", "Yes, I live for draft day"])

with col2:
    st.markdown("### Viewership Data")
    content_frequency_weekly = st.select_slider(
        "How much football do you consume?",
        options=["Rarely", "Sometimes", "Weekly", "Most days", "Daily"],
        value="Weekly"
    )
    content_watch_likelihood = st.select_slider(
        "Will you catch the next game?",
        options=["Unlikely", "Maybe", "Probably", "Definitely"],
        value="Probably"
    )
    barrier_no_time = st.selectbox("When life gets busy, do you still watch?", ["I make time", "Yeah, too busy"])
    
    st.markdown("### League Sentiment")
    nfl_community_care = st.selectbox("Does the NFL do enough for the community?", ["Not convinced", "Yes, they do"])
    player_credibility_social = st.selectbox("Do you value players speaking out on social issues?", ["Not really", "I hear them out"])

# Logic Helpers
def yes_no(val):
    return 1 if val in ["You know it!", "Absolutely!", "Yes, I live for draft day", "Yes, they do", "I hear them out", "Yeah, too busy"] else 0

def frequency_to_int(val):
    return {"Rarely": 1, "Sometimes": 2, "Weekly": 3, "Most days": 4, "Daily": 5}[val]

def likelihood_to_int(val):
    return {"Unlikely": 1, "Maybe": 2, "Probably": 3, "Definitely": 4}[val]

st.divider()

# Action Button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    predict_btn = st.button("ANALYZE FAN STATUS", type="primary", use_container_width=True)

if predict_btn:
    payload = {
        "nfl_community_care": yes_no(nfl_community_care),
        "player_credibility_social": yes_no(player_credibility_social),
        "content_frequency_weekly": frequency_to_int(content_frequency_weekly),
        "content_watch_likelihood": likelihood_to_int(content_watch_likelihood),
        "has_fav_team": yes_no(has_fav_team),
        "driver_game_excitement": yes_no(driver_game_excitement),
        "driver_fantasy": yes_no(driver_fantasy),
        "barrier_no_time": yes_no(barrier_no_time),
        "age": age,
        "gender": 1 if gender == "Male" else 0
    }
    
    with st.spinner("Crunching Stats..."):
        time.sleep(1)
        
        try:
            response = requests.post(API_URL, json=payload)
            result = response.json()
            
            prediction = result['prediction']
            probs = result['probabilities']
            
            # Text Content
            high_desc = "Is your mood on Monday morning entirely dependent on the final score from Sunday night? Sunday isn't a day of rest for you because it is a full contact sport. You are up before the pregame shows start to check the final injury reports and tweak your fantasy lineup one last time. You don't just watch the quarterback throw the ball. You are watching the offensive line schemes and screaming about blown coverage before the announcers even notice it. Your friends text you when a trade happens because they know you have already analyzed the salary cap impact five minutes ago. You aren't just a spectator. You are a student of the game who demands total access. True expertise requires elite tools to stay sharp so check out the premium scouting resources we selected for you below to take your game to the next level."
            medium_desc = "Do you love the touchdowns but refuse to let a bad call ruin your entire week? You live for the electricity of the game but you aren't letting a Week 4 loss ruin your entire month. Football is the ultimate social currency for you. It is about the adrenaline of a fourth quarter comeback and the banter in your group chat and the roar of the bar when a big play happens. You want the big plays without the downtime and the highlights without the heartache. You have mastered the art of the Perfect Sunday where you get maximum action with minimum boredom. Your fandom is healthy and fun and fast paced. Keep that energy high by exploring the recommended feeds below that are designed to cut out the commercials and deliver straight dopamine from around the league."
            low_desc = "Did you mostly show up for the snacks and stay for the hits? Welcome to the greatest show on earth. You have felt the energy of the Super Bowl spectacle or seen the viral highlights on your feed and now you are ready to understand why millions hold their breath when the ball is in the air. Maybe you are here for the athleticism or the strategic drama or just to finally understand what everyone is yelling about at the party. Don't sweat the complex rules because every die hard fan started exactly where you are right now. The NFL is a massive unfolding story of heroes and villains and miracles. Your journey into the culture begins today. All you need to do is learn the language and find the colors you will represent for life so start your journey with the starter pack links below."
            
            # Descriptions & Class Styling
            if prediction == "High":
                tier_class = "tier-high"
                tier_title = "ALL-PRO FAN"
                tier_desc = high_desc
            elif prediction == "Medium":
                tier_class = "tier-medium"
                tier_title = "CASUAL FAN"
                tier_desc = medium_desc
            else:
                tier_class = "tier-low"
                tier_title = "ROOKIE FAN"
                tier_desc = low_desc

            # --- RENDER RESULT CARD (No indentation for HTML strings) ---
            st.markdown(f"""
<div class='player-card {tier_class}'>
<div class='card-header'>
<span class='card-rank'>Official Designation</span>
<h1 class='card-title'>{tier_title}</h1>
</div>
<div class='card-body'>
{tier_desc}
<hr style='border-color:rgba(255,255,255,0.1); margin: 1.5rem 0;'>
<div class='stat-row'>
<div class='stat-label'>ALL-PRO</div>
<div class='stat-track'><div class='stat-fill' style='width: {probs[0]*100}%'></div></div>
<div class='stat-val'>{probs[0]:.0%}</div>
</div>
<div class='stat-row'>
<div class='stat-label'>CASUAL</div>
<div class='stat-track'><div class='stat-fill' style='width: {probs[2]*100}%'></div></div>
<div class='stat-val'>{probs[2]:.0%}</div>
</div>
<div class='stat-row'>
<div class='stat-label'>ROOKIE</div>
<div class='stat-track'><div class='stat-fill' style='width: {probs[1]*100}%'></div></div>
<div class='stat-val'>{probs[1]:.0%}</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

            if prediction == "High":
                st.balloons()

            # --- RENDER RESOURCES ---
            high_res = """
<div class='resource-box'>
<div class='resource-title'>NFL+ Premium</div>
<div style='color:#888; font-size:0.8rem; margin-bottom:0.5rem'>All-22 coaches film & replays</div>
<a href='https://www.nfl.com/plus/' target='_blank' class='resource-link'>ACCESS FEED &rarr;</a>
</div>
<div class='resource-box'>
<div class='resource-title'>Sunday Ticket</div>
<div style='color:#888; font-size:0.8rem; margin-bottom:0.5rem'>Every out-of-market game live</div>
<a href='https://tv.youtube.com/learn/nflsundayticket/' target='_blank' class='resource-link'>SUBSCRIBE &rarr;</a>
</div>
"""
            med_res = """
<div class='resource-box'>
<div class='resource-title'>NFL RedZone</div>
<div style='color:#888; font-size:0.8rem; margin-bottom:0.5rem'>7 hours of commercial-free action</div>
<a href='https://www.nfl.com/redzone/' target='_blank' class='resource-link'>WATCH NOW &rarr;</a>
</div>
<div class='resource-box'>
<div class='resource-title'>Fantasy Football</div>
<div style='color:#888; font-size:0.8rem; margin-bottom:0.5rem'>Join a league today</div>
<a href='https://fantasy.nfl.com/' target='_blank' class='resource-link'>DRAFT TEAM &rarr;</a>
</div>
"""
            low_res = """
<div class='resource-box'>
<div class='resource-title'>Football 101</div>
<div style='color:#888; font-size:0.8rem; margin-bottom:0.5rem'>Learn the rules & positions</div>
<a href='https://operations.nfl.com/the-rules/nfl-rulebook/' target='_blank' class='resource-link'>START HERE &rarr;</a>
</div>
<div class='resource-box'>
<div class='resource-title'>Top 100 Plays</div>
<div style='color:#888; font-size:0.8rem; margin-bottom:0.5rem'>Best moments in history</div>
<a href='https://www.youtube.com/nfl' target='_blank' class='resource-link'>WATCH CLIPS &rarr;</a>
</div>
"""
            selected_res = high_res if prediction == "High" else med_res if prediction == "Medium" else low_res
            
            st.markdown(f"""
<div style='margin-top:2rem'>
<h3>OFFICIAL RECOMMENDATIONS</h3>
<div class='resource-container'>
{selected_res}
<div class='resource-box'>
<div class='resource-title'>Find Your Team</div>
<div style='color:#888; font-size:0.8rem; margin-bottom:0.5rem'>Browse all 32 franchises</div>
<a href='https://www.nfl.com/teams/' target='_blank' class='resource-link'>EXPLORE &rarr;</a>
</div>
<div class='resource-box'>
<div class='resource-title'>NFL Shop</div>
<div style='color:#888; font-size:0.8rem; margin-bottom:0.5rem'>Official Gear</div>
<a href='https://www.nflshop.com/' target='_blank' class='resource-link'>GEAR UP &rarr;</a>
</div>
</div>
</div>
""", unsafe_allow_html=True)
            
            # Download Logic
            st.divider()
            dl_col1, dl_col2, dl_col3 = st.columns([1,1,1])
            with dl_col2:
                 result_text = f"NFL FAN ENGAGEMENT REPORT\nLEVEL: {tier_title}\n\n{tier_desc}\n\nPROBABILITIES:\nAll-Pro: {probs[0]:.1%}\nCasual: {probs[2]:.1%}\nRookie: {probs[1]:.1%}"
                 st.download_button(
                    label="DOWNLOAD REPORT CARD",
                    data=result_text,
                    file_name="nfl_fan_report.txt",
                    mime="text/plain",
                    use_container_width=True
                )

        except Exception as e:
            st.error(f"Connection error: {e}")

# Footer
st.markdown("""
<div style='text-align:center; padding:3rem 0; color:#555; font-size:0.8rem;'>
NGUYEN MINH PHUC · FoAI9 PROJECT
</div>
""", unsafe_allow_html=True)