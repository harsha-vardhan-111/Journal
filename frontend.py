import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="Mood Journal", layout="centered")

# Define the main page
def main():
    st.title("Daily Mood Journal")
    st.write("Welcome to your daily mood journal. How was your day?")

    # Date Picker
    date = st.date_input("Select a date", datetime.now())

    # Journal Entry Box
    journal_entry = st.text_area("How was your day?", height=200)

    # Submit Button
    if st.button("Submit"):
        st.success("Entry submitted!")
        # Here you would add code to save the entry and analyze sentiment
        # For now, we'll just display a placeholder sentiment feedback
        st.write("Sentiment: 😊 (Happy)")

    # Weekly Emotion Report Section
    st.header("Weekly Emotion Report")
    st.write("Review your emotions over the past week.")

    # Placeholder data for mood trend visualization
    dates = [datetime.now().date() for _ in range(7)]
    sentiments = [1, 2, 3, 2, 1, 3, 2]  # 1: Happy, 2: Neutral, 3: Sad

    # Mood Trend Visualization
    fig, ax = plt.subplots()
    ax.plot(dates, sentiments, marker='o')
    ax.set_title("Mood Trend Over the Past Week")
    ax.set_xlabel("Date")
    ax.set_ylabel("Sentiment")
    st.pyplot(fig)

    # Emotion Insights
    st.write("Your week was mostly positive with some mid-week lows.")

# Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Weekly Report"])

if page == "Home":
    main()
elif page == "Weekly Report":
    st.header("Weekly Emotion Report")
    st.write("Review your emotions over the past week.")
    # Reuse the weekly report section from the main function
    dates = [datetime.now().date() for _ in range(7)]
    sentiments = [1, 2, 3, 2, 1, 3, 2]  # 1: Happy, 2: Neutral, 3: Sad
    fig, ax = plt.subplots()
    ax.plot(dates, sentiments, marker='o')
    ax.set_title("Mood Trend Over the Past Week")
    ax.set_xlabel("Date")
    ax.set_ylabel("Sentiment")
    st.pyplot(fig)
    st.write("Your week was mostly positive with some mid-week lows.")

# Run the app
if __name__ == "__main__":
    main()