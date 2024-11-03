import psycopg2
import streamlit as st
import pandas as pd

# Function to fetch emotions count from the database
def fetch_emotion_counts():
    try:
        connection = psycopg2.connect(
            dbname="hackathon",
            user="postgres",
            password="pass",  # Replace with your password
            host="localhost",
            port="5432"
        )
        cur = connection.cursor()
        cur.execute("""
            SELECT LOWER(TRIM(emotion_split.Emotion)) AS Emotion,
                   COUNT(*) AS EmotionCount
            FROM journalentries j
            JOIN LATERAL regexp_split_to_table(j.emotions, ',') AS emotion_split(Emotion) ON TRUE
            WHERE j.userid = 1
              AND j.entry_date >= NOW() - INTERVAL '10 days'
              AND j.name = 'Deepak'
            GROUP BY LOWER(TRIM(emotion_split.Emotion))
            ORDER BY EmotionCount DESC;
            """
        )
        
        data = cur.fetchall()
        cur.close()
        connection.close()
        return data
    except (Exception, psycopg2.Error) as error:
        st.error("Error fetching data from PostgreSQL: " + str(error))
        return []

# Streamlit UI setup
st.title("🌟 Top Emotions felt by Deepak in the past 10 Days 🌟")

# Custom CSS for styling
st.markdown("""
    <style>
        .emotion-card {
            font-size: 1.2em;
            font-weight: bold;
            padding: 10px;
            margin: 10px 0;
            border-radius: 10px;
            color: #fff;
            text-align: center;
        }
        .emotion-1 { background-color: #ff6b6b; }
        .emotion-2 { background-color: #ffa36c; }
        .emotion-3 { background-color: #6bcff6; }
    </style>
""", unsafe_allow_html=True)

# Fetch the top emotions and display them immediately
results = fetch_emotion_counts()
if results:
    # Get the top 3 emotions
    top_emotions = [emotion[0] for emotion in results[:3]]
    
    # Display each emotion with custom colors and styling
    st.subheader("Top 3 Emotions")

    # Create custom divs for each emotion with colors
    for i, emotion in enumerate(top_emotions, 1):
        st.markdown(f'<div class="emotion-card emotion-{i}"> {emotion.capitalize()}</div>', unsafe_allow_html=True)
else:
    st.write("No data found for the past 10 days.")
