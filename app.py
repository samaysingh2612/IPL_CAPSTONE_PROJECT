# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="IPL Analytics Dashboard",
    page_icon="🏏",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
df = pd.read_csv("IPL.csv")

# ---------------- SIDEBAR ----------------
st.sidebar.title("🏏 IPL Dashboard")

page = st.sidebar.radio(
    "Navigate",
    ["Home", "Team Analysis", "Player Analysis", "Match Insights"]
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main {
    background-color: #0f172a;
    color: white;
}

.stApp {
    background: linear-gradient(to right, #0f172a, #1e293b);
}

h1, h2, h3 {
    color: #facc15;
}

[data-testid="stSidebar"] {
    background-color: #111827;
}

.css-1d391kg {
    background-color: #111827;
}

.metric-card {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HOME PAGE ----------------
if page == "Home":

    st.title("🏏 IPL Analytics Dashboard")

    st.image("ipl_logo.png", width=250)

    st.markdown("""
    ## Welcome to IPL Analytics Dashboard
    
    Explore:
    - Team Performance
    - Player Statistics
    - Match Insights
    - Toss Analysis
    - Winning Trends
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Matches", len(df))

    with col2:
        st.metric("Total Teams", df['team1'].nunique())

    with col3:
        st.metric("Total Venues", df['venue'].nunique())

# ---------------- TEAM ANALYSIS ----------------
elif page == "Team Analysis":

    st.title("📊 Team Analysis")

    teams = sorted(df['winner'].dropna().unique())

    selected_team = st.selectbox("Select Team", teams)

    team_wins = df[df['winner'] == selected_team]

    st.subheader(f"{selected_team} Total Wins")
    st.metric("Wins", len(team_wins))

    venue_wins = team_wins['venue'].value_counts().reset_index()
    venue_wins.columns = ['Venue', 'Wins']

    fig = px.bar(
        venue_wins,
        x='Venue',
        y='Wins',
        color='Wins',
        title=f'{selected_team} Wins by Venue'
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------- PLAYER ANALYSIS ----------------
elif page == "Player Analysis":

    st.title("🏏 Player Analysis")

    if 'player_of_match' in df.columns:

        top_players = df['player_of_match'].value_counts().head(10)

        fig = px.bar(
            x=top_players.index,
            y=top_players.values,
            color=top_players.values,
            labels={'x': 'Player', 'y': 'Awards'},
            title='Top Player of the Match Winners'
        )

        st.plotly_chart(fig, use_container_width=True)

# ---------------- MATCH INSIGHTS ----------------
elif page == "Match Insights":

    st.title("📈 Match Insights")

    toss_winner = df['toss_winner'].value_counts().head(10)

    fig = px.pie(
        names=toss_winner.index,
        values=toss_winner.values,
        title='Toss Winners Distribution'
    )

    st.plotly_chart(fig, use_container_width=True)

    win_by_runs = df['win_by_runs']

    fig2 = px.histogram(
        win_by_runs,
        nbins=30,
        title='Win By Runs Distribution'
    )

    st.plotly_chart(fig2, use_container_width=True)
