import streamlit as st
import requests
import time

# -------------------------
# Custom CSS Styling
# -------------------------
st.markdown("""
    <style>

        /* Global background */
        body {
            background-color: #f4f6f9;
        }

        /* Title */
        .title {
            font-size: 42px;
            font-weight: 900;
            color: #2d3436;
            text-align: center;
            padding-bottom: 5px;
        }

        /* Subtitle */
        .subtitle {
            font-size: 20px;
            color: #636e72;
            text-align: center;
            margin-bottom: 30px;
        }

        /* Result styling */
        .result-box {
            padding: 25px;
            border-radius: 12px;
            margin-top: 20px;
            font-size: 26px;
            text-align: center;
            font-weight: 700;
            animation: fadeIn 0.6s ease-in-out;
        }
        .positive {
            background-color: #d4edda;
            color: #155724;
        }
        .negative {
            background-color: #f8d7da;
            color: #721c24;
        }
        .neutral {
            background-color: #fff3cd;
            color: #856404;
        }

        /* Fade-in animation */
        @keyframes fadeIn {
            from {opacity: 0;}
            to {opacity: 1;}
        }

        /* Character counter */
        .char-counter {
            font-size: 14px;
            color: #636e72;
            text-align: right;
            margin-top: -10px;
        }

    </style>
""", unsafe_allow_html=True)

# -------------------------
# API Endpoint
# -------------------------
API_URL = "https://nlp-tweet-sentiment-project.onrender.com/predict"

# -------------------------
# Navigation
# -------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Home", "About", "Prediction"])


# -------------------------
# HOME PAGE
# -------------------------
if page == "Home":
    st.markdown("<div class='title'>Tweet Sentiment Analysis 🌙</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Fast • Beautiful • Accurate</div>", unsafe_allow_html=True)
    st.write("Use the sidebar to explore the app.")


# -------------------------
# ABOUT PAGE
# -------------------------
elif page == "About":
    st.title("About This Project")
    st.write("""
        This interactive web app analyzes the sentiment of tweets using a trained NLP machine learning model.

        ### How It Works
        - You type a tweet  
        - The app sends it to our hosted Flask API  
        - The API processes the text using the machine-learning pipeline  
        - A sentiment label is returned instantly  

        ### Sentiment Labels
        - **0 = Neutral 😐**  
        - **1 = Negative 😠**  
        - **2 = Positive 😊**  
        
        The model is trained specifically for tweets and handles slang, emojis, abbreviations, and informal language.
    """)


# -------------------------
# PREDICTION PAGE
# -------------------------
elif page == "Prediction":

    st.title("Predict Tweet Sentiment")
    
    tweet = st.text_area("Enter your tweet:", height=140)

    # Character counter
    st.markdown(
        f"<div class='char-counter'>{len(tweet)} characters</div>", 
        unsafe_allow_html=True
    )

    if st.button("Analyze Sentiment"):

        if not tweet.strip():
            st.warning("⚠️ Please enter a tweet before submitting.")
            st.toast("Tweet cannot be empty!", icon="⚠️")
            st.stop()

        # Spinner animation
        with st.spinner("Analyzing sentiment..."):
            try:
                start_time = time.time()

                response = requests.post(
                    API_URL,
                    json={"input": [tweet]},
                    headers={"Content-Type": "application/json"},
                    timeout=10
                )

                api_time = time.time() - start_time

                if response.status_code != 200:
                    st.error("❌ API returned an error.")
                    st.json(response.json())
                    st.toast("The API returned an error.", icon="⚠️")
                    st.stop()

                data = response.json()
                prediction = data["prediction"][0]

                # Sentiment mapping
                sentiments = {
                    2: ("Positive 😊", "positive"),
                    1: ("Negative 😠", "negative"),
                    0: ("Neutral 😐", "neutral"),
                }

                label, css_class = sentiments.get(prediction, ("Unknown 🤔", "neutral"))

                # Display result
                st.markdown(
                    f"<div class='result-box {css_class}'>{label}</div>",
                    unsafe_allow_html=True
                )

                # API latency
                st.info(f"⏱ API Response Time: {api_time:.2f} seconds")

                st.toast("Prediction successful!", icon="🎉")

            except requests.exceptions.Timeout:
                st.error("⏳ The API took too long to respond.")
                st.toast("Request timed out!", icon="⚠️")

            except requests.exceptions.ConnectionError:
                st.error("🔌 Could not connect to the API. It may be offline.")
                st.toast("API connection failed!", icon="❌")

            except Exception as e:
                st.error(f"Unexpected error: {e}")
                st.toast("Something went wrong!", icon="🔥")
