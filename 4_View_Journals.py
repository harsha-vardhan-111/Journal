import psycopg2
import streamlit as st
from datetime import datetime

# Function to fetch journal entries for a specific date
def fetch_journal_entries(date):
    try:
        connection = psycopg2.connect(
            dbname="hackathon",
            user="postgres",
            password="pass",  # Replace with your password
            host="localhost",
            port="5432"
        )
        cur = connection.cursor()
        
        # Convert selected date to match the format of entry_date (ignoring time)
        date_str = date.strftime('%Y-%m-%d')
        
        cur.execute("""
            SELECT entry_date, journal 
            FROM journalentries 
            WHERE DATE(entry_date) = %s AND userid = 1 AND name = 'Deepak'
            ORDER BY entry_date;
            """, (date_str,))
        
        data = cur.fetchall()
        cur.close()
        connection.close()
        return data
    except (Exception, psycopg2.Error) as error:
        st.error("Error fetching data from PostgreSQL: " + str(error))
        return []

# Streamlit UI for viewing journal entries
def view_journals_page():
    st.header("View Journal Entries")
    st.write("Select a date to view your journal entries.")

    # Custom CSS for the journal entry box
    st.markdown("""
        <style>
            .journal-box {
                background-color: #E0FFFF;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 15px;
                box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            }
            .journal-box h3 {
                color: #333;
                font-weight: bold;
            }
            .journal-box p {
                color: #555;
                font-size: 1.1em;
            }
        </style>
    """, unsafe_allow_html=True)

    # Date Picker
    date = st.date_input("Select a date to view entries", datetime.now(), key="view_journal_date")

    # Fetch journal entries for the selected date
    entries = fetch_journal_entries(date)

    # Display journal entries
    if entries:
        st.write(f"Journal entries for {date.strftime('%Y-%m-%d')}:")
        for entry_date, journal in entries:
            # Use markdown with custom CSS to display each journal entry in a styled box
            st.markdown(f"""
                <div class="journal-box">
                    <h3>Entry Time: {entry_date.strftime('%Y-%m-%d %H:%M:%S')}</h3>
                    <p>{journal}</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.write("No entries found for this date.")
    
view_journals_page()
