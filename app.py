import streamlit as st
import requests
import time

# -------------------------
# Custom CSS Styling
# -------------------------
st.markdown("""
    <style>
        /* Full app gradient */
        .stApp, .main, .block-container {
            background: linear-gradient(135deg, #f0f4f8, #d9e2ec);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        /* Sidebar styling */
        .sidebar .sidebar-content {
            background: linear-gradient(135deg, #e9ecef, #f1f3f6);
            border-radius: 12px;
            padding: 20px;
        }

        /* Titles */
        .title {
            font-size: 44px;
            font-weight: 900;
            color: #1b262c;
            text-align: center;
            margin-bottom: 5px;
        }

        .subtitle {
            font-size: 20px;
            color: #415a77;
            text-align: center;
            margin-bottom: 30px;
        }

        /* Cards */
        .home-card, .result-box {
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 20px;
            text-align: center;
            box-shadow: 0px 8px 25px rgba(0,0,0,0.15);
            transition: transform 0.2s ease-in-out;
        }
        .home-card:hover {
            transform: translateY(-5px);
        }

        /* Result boxes */
        .result-box {
            font-size: 28px;
            font-weight: 700;
            animation: fadeIn 0.7s ease-in-out;
        }
        .positive { background-color: #d4edda; color: #155724; }
        .negative { background-color: #f8d7da; color: #721c24; }
        .neutral { background-color: #fff3cd; color: #856404; }

        @keyframes fadeIn {
            from {opacity: 0; transform: translateY(-10px);}
            to {opacity: 1; transform: translateY(0);}
        }

        /* Character counter */
        .char-counter { font-size: 14px; color: #495057; text-align: right; margin-top: -10px; }
        .char-counter.warning { color: #d6336c; font-weight: bold; }

        /* Footer */
        .footer { font-size: 14px; color: #495057; text-align: center; margin-top: 50px; padding-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# -------------------------
# API Endpoint
# -------------------------
API_URL = "https://nlp-tweet-sentiment-project.onrender.com/predict"

# -------------------------
# Sidebar Navigation
# -------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Home", "About", "Prediction"])

# -------------------------
# HOME PAGE
# -------------------------
if page == "Home":
    st.markdown("<div class='title'>Tweet Sentiment Analysis 🌙</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Fast • Beautiful • Accurate</div>", unsafe_allow_html=True)

    st.markdown("""
        <div class='home-card'>
            <h3>Welcome!</h3>
            <p>Analyze the sentiment of your tweets instantly. Our AI model understands slang, emojis, and informal language.</p>
        </div>
        <div class='home-card'>
            <h3>How to Use</h3>
            <ol style='text-align:left; display:inline-block;'>
                <li>Navigate to the "Prediction" page</li>
                <li>Type or paste your tweet</li>
                <li>Click "Analyze Sentiment"</li>
                <li>View the result instantly</li>
            </ol>
        </div>
    """, unsafe_allow_html=True)

# -------------------------
# ABOUT PAGE
# -------------------------
elif page == "About":
    st.markdown("<div class='home-card'>", unsafe_allow_html=True)
    st.title("About This Project")
    st.write("""
        This interactive web app analyzes the sentiment of tweets using a trained NLP machine learning model.

        ### How It Works
        - Type a tweet  
        - The app sends it to our hosted API  
        - The API processes the text using the ML pipeline  
        - A sentiment label is returned instantly  

        ### Sentiment Labels
        - **0 = Neutral 😐**  
        - **1 = Negative 😠**  
        - **2 = Positive 😊**  

        The model handles slang, emojis, abbreviations, and informal language.
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# PREDICTION PAGE
# -------------------------
elif page == "Prediction":
    st.markdown("<div class='home-card'>", unsafe_allow_html=True)
    st.title("Predict Tweet Sentiment")
    
    tweet = st.text_area("Enter your tweet:", height=140)
    
    # Character counter
    char_class = "warning" if len(tweet) > 280 else ""
    st.markdown(f"<div class='char-counter {char_class}'>{len(tweet)} characters</div>",
                unsafe_allow_html=True)

    if st.button("Analyze Sentiment"):
        if not tweet.strip():
            st.warning("⚠️ Please enter a tweet before submitting.")
            st.stop()

        with st.spinner("Analyzing sentiment..."):
            try:
                max_retries = 3
                for attempt in range(max_retries):
                    start_time = time.time()
                    response = requests.post(
                        API_URL,
                        json={"input": [tweet]},
                        headers={"Content-Type": "application/json"},
                        timeout=10
                    )
                    api_time = time.time() - start_time

                    if response.status_code == 429:
                        time.sleep(2 + attempt*2)  # exponential backoff
                    else:
                        break

                if response.status_code == 429:
                    st.error("❌ Too many requests. Please wait a few seconds and try again.")
                    st.stop()
                elif response.status_code != 200:
                    st.error(f"❌ API returned an error (status {response.status_code})")
                    st.json({"response_text": response.text})
                    st.stop()

                data = response.json()
                prediction = data.get("prediction", [None])[0]
                if prediction is None:
                    st.error("❌ API response missing 'prediction'.")
                    st.stop()

                sentiments = {
                    2: ("Positive 😊", "positive"),
                    1: ("Negative 😠", "negative"),
                    0: ("Neutral 😐", "neutral"),
                }
                label, css_class = sentiments.get(prediction, ("Unknown 🤔", "neutral"))

                st.markdown(f"<div class='result-box {css_class}'>{label}</div>", unsafe_allow_html=True)
                st.info(f"⏱ API Response Time: {api_time:.2f} seconds")

            except requests.exceptions.Timeout:
                st.error("⏳ The API took too long to respond.")
            except requests.exceptions.ConnectionError:
                st.error("🔌 Could not connect to the API. The API may be offline.")
            except Exception as e:
                st.error(f"Unexpected error: {e}")

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# Footer
# -------------------------
st.markdown("<div class='footer'>Developed by Ian Kiptoo © 2025</div>", unsafe_allow_html=True)
