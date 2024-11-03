import requests
import nltk
import streamlit as st
from collections import defaultdict
import psycopg2
from datetime import datetime

nltk.download('punkt')

# Set API URL and load the API key securely
API_URL = "https://api-inference.huggingface.co/models/j-hartmann/emotion-english-distilroberta-base"
headers = {"Authorization": "Bearer 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"}  # replace with st.secrets['HUGGINGFACE_API_KEY'] in production

# Function to query the API for each sentence
def query(text):
    response = requests.post(API_URL, headers=headers, json={"inputs": text})
    if response.status_code == 200:
        data = response.json()
        return data[0] if isinstance(data, list) and len(data) > 0 else []
    else:
        return {"error": response.json().get("error", "Unknown error")}

# Function to analyze the entire text by aggregating scores for each sentence
def analyze_text(text):
    sentences = nltk.sent_tokenize(text)
    emotion_scores = defaultdict(float)
    total_chunks = 0

    for sentence in sentences:
        emotions = query(sentence)
        if isinstance(emotions, list):
            # Aggregate scores for each emotion
            for emotion in emotions:
                emotion_scores[emotion['label']] += emotion['score']
            total_chunks += 1
        else:
            st.error("API error for sentence: " + sentence)

    # Average the scores across all chunks
    averaged_emotions = [{"label": label, "score": score / total_chunks} for label, score in emotion_scores.items()]
    return sorted(averaged_emotions, key=lambda x: x['score'], reverse=True)

# Function to connect to the database
def connect_to_db():
    try:
        connection = psycopg2.connect(
            dbname="hackathon",
            user="postgres",
            password="pass",  # Replace with your password
            host="localhost",
            port="5432"
        )
        print("Connected to the database.")
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return None

# Function to insert a journal entry into the database
def save_journal_entry(connection, name, emotions, entry_date, journal, userid=1):
    try:
        cur = connection.cursor()
        
        # Filter emotions to only keep significant ones (e.g., scores > 0.1)
        significant_emotions = [emotion['label'] for emotion in emotions if emotion['score'] > 0.1]
        
        # Convert filtered emotions to a comma-separated string
        emotions_str = ", ".join(significant_emotions)
        
        # Debugging print statement with filtered data
        print(f"Emotions: {emotions_str} | Journal Length: {len(journal)} | Date: {entry_date} | UserID: {userid}")
        
        insert_query = """
        INSERT INTO JournalEntries (name, emotions, entry_date, journal, userid)
        VALUES (%s, %s, %s, %s, %s)
        """
        cur.execute(insert_query, (name, emotions_str, entry_date, journal, userid))
        connection.commit()
        cur.close()
        print("Journal entry saved to the database.")
    except (Exception, psycopg2.Error) as error:
        print("Error while inserting into PostgreSQL", error)

# Streamlit UI setup
st.markdown("<h1 style= color: #4CAF50;'>Cumulative Emotion Analysis App</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: grey;'>Analyze and store emotions from your daily reflections</h4>", unsafe_allow_html=True)

# Custom CSS for better styling
st.markdown("""
    <style>
        .emotion-box {
            background-color: #f0f8ff;
            border: 1px solid #b3cde0;
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
            font-size: 1.2em;
            color: #333;
        }
        .emotion-primary {
            font-size: 1.4em;
            font-weight: bold;
            color: #ff6f61;
        }
    </style>
""", unsafe_allow_html=True)

# Text area for user input
text = st.text_area("Enter your journal text for analysis:", placeholder="Type here...", height=200)

# Analyze button
if st.button("Analyze and Save"):
    if text:
        # Perform emotion analysis
        with st.spinner("Analyzing emotions..."):
            averaged_emotions = analyze_text(text)

            # Display results in styled boxes
            if averaged_emotions:
                top_emotion = averaged_emotions[0]
                second_emotion = averaged_emotions[1] if len(averaged_emotions) > 1 else None

                st.markdown("<h3>Detected Emotions:</h3>", unsafe_allow_html=True)
                if second_emotion and abs(top_emotion['score'] - second_emotion['score']) < 0.1:
                    st.markdown(f"<div class='emotion-box'><span class='emotion-primary'>Top Emotions:</span><br>1. {top_emotion['label'].capitalize()}<br>2. {second_emotion['label'].capitalize()}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='emotion-box'><span class='emotion-primary'>Primary Emotion:</span> {top_emotion['label'].capitalize()}</div>", unsafe_allow_html=True)

                # Connect to the database and save the result
                connection = connect_to_db()
                if connection:
                    name = "Deepak"
                    entry_date = datetime.now()
                    save_journal_entry(connection, name, averaged_emotions, entry_date, text)
                    connection.close()
                    st.success("Journal entry successfully saved!")
            else:
                st.error("No emotions detected. Please try with a different text.")
    else:
        st.warning("Please enter some text.")

