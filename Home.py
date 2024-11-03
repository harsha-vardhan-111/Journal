import streamlit as st 

def home_page():
    # Custom CSS for the overall aesthetic
    st.markdown("""
        <style>
            body {
                background-image: url('https://www.example.com/path/to/your/image.jpg');
                background-size: cover;
                font-family: 'Poppins', sans-serif;
            }
            .main {
                background-color: rgba(255, 255, 255, 0.8);
                padding: 20px;
                border-radius: 10px;
            }
            @keyframes fadeIn {
                0% { opacity: 0; transform: translateY(-20px); }
                100% { opacity: 1; transform: translateY(0); }
            }
            
            .animated-title {
                font-family: 'Poppins', sans-serif;
                font-size: 64px;
                font-weight: bold;
                color: #333;
                text-align: center;
                margin-top: 40px;
                animation: fadeIn 2s ease-in-out;
            }

            .message-box {
                font-family: 'Georgia', serif;
                font-size: 24px;
                color: #333;
                background-color: #f0d6d2;
                padding: 20px;
                border-radius: 12px;
                text-align: center;
                margin-top: 20px;
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
                max-width: 800px;
                margin-left: auto;
                margin-right: auto;
            }

            .question {
                font-family: 'Poppins', sans-serif;
                font-size: 28px;
                color: #333;
                text-align: center;
                margin-top: 30px;
            }

            .stButton > button {
                background-color: #5a5a5a;
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 30px;
                font-size: 18px;
                margin: 10px;
                cursor: pointer;
                transition: background-color 0.3s;
            }

            .stButton > button:hover {
                background-color: #777;
                color: #f5f5f5;
            }

            .stButton > div {
                display: flex;
                justify-content: center;
            }

            .stButton > div:nth-child(2) {
                justify-content: flex-end;
            }

            .stAlert {
                font-family: 'Georgia', serif;
                font-size: 28px;
                color: #333;
                background-color: #d4edda;
                padding: 40px;
                border-radius: 12px;
                text-align: center;
                margin-top: 20px;
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
                max-width: 800px;
                margin-left: auto;
                margin-right: auto;
            }
        </style>
    """, unsafe_allow_html=True)

    # Display the animated title
    st.markdown("""
    <div class="animated-title">
        SoulScribe
    </div>
    """, unsafe_allow_html=True)

    # Display the aesthetic message box
    st.markdown("""
    <div class="message-box">
        Take a deep breath and think about today’s journey. Each moment contributed to who you are. Unwind with peace and gratitude.
    </div>
    """, unsafe_allow_html=True)

    # Display the question asking about the user's day
    st.markdown("""
    <div class="question">
        How's your day going?
    </div>
    """, unsafe_allow_html=True)

    # Display the buttons and responses
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Feeling Great!"):
            st.snow()  # Display confetti-like snow effect
            st.markdown("""
            <div class="stAlert">
                That's wonderful! Keep spreading your joy and positivity!
            </div>
            """, unsafe_allow_html=True)

    with col2:
        if st.button("Could be Better"):
            st.balloons()  # Celebrate with balloons
            st.markdown("""
            <div class="stAlert">
                It's okay. Take this moment to rest and remind yourself that tomorrow is a new day. You’re doing great.
            </div>
            """, unsafe_allow_html=True)

home_page()
