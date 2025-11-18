import streamlit as st
import requests
import time

# -------------------------
# Custom CSS Styling
# -------------------------
st.markdown("""
    <style>
        /* Main Layout */
        .stApp, .main, .block-container {
            background: linear-gradient(135deg, #eef2fb, #ddeaf6);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        /* Sidebar */
        .sidebar .sidebar-content {
            background: linear-gradient(135deg, #f5f7fa, #f3f6fb);
            border-radius: 16px;
            padding: 20px 0 18px 0;
        }
        /* Navigation Highlight */
        [data-testid="stSidebarNav"] li[data-testid="stSidebarNavLink"]:has(svg) {
            font-weight: 600 !important;
            background: #c8e6e7 !important;
            border-radius: 7px;
            padding-left: 10px !important;
        }
        /* Main Title */
        .main-title {
            font-size: 44px;
            font-weight: 900;
            background: linear-gradient(90deg, #234c63 40%, #3282b8 60%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin: 45px 0 7px 0;
        }
        .subtitle {
            font-size: 20px;
            color: #415a77;
            text-align: center;
            margin-bottom: 26px;
        }
        /* Cards */
        .main-card, .result-box {
            border-radius: 20px;
            padding: 25px 36px;
            margin: 18px 0;
            text-align: center;
            box-shadow: 0px 8px 25px rgba(27, 38, 44, 0.12);
            background: #fff;
        }
        .main-card:hover {
            transform: translateY(-4px) scale(1.025);
            box-shadow: 0px 12px 30px rgba(50, 130, 184, 0.11);
        }
        /* Sentiment Result */
        .result-box {
            font-size: 30px;
            font-weight: 700;
            animation: bounce-in .7s;
        }
        .positive { background: linear-gradient(100deg, #ebfbee, #baf2c1); color: #20752c; }
        .negative { background: linear-gradient(100deg, #fff1f3, #f8d7da); color: #b7322b; }
        .neutral { background: linear-gradient(100deg, #f6f9fc, #fffbe7); color: #897108; }
        @keyframes bounce-in {
            0% { transform: scale(0.92); opacity: 0; }
            60% { transform: scale(1.05); }
            80% { transform: scale(0.99); }
            100% { transform: scale(1); opacity: 1; }
        }
        /* Input box focus */
        textarea:focus {
            border: 2px solid #3282b8 !important;
            box-shadow: 0 0 8px #71c0e8;
            background: #f1f9ff !important;
        }
        /* Character counter */
        .char-counter { font-size: 14px; color: #495057; text-align: right; margin-top: -14px; }
        .char-counter.warning { color: #d6336c; font-weight: bold; }
        /* Toast/alert box */
        .toast-alert {
            font-size: 17px;
            background: #fff3cd;
            color: #8a6d3b;
            border-radius: 14px;
            border: 1px solid #ffeeba;
            padding: 12px;
            margin-bottom: 14px;
        }
        /* Footer */
        .footer {
            font-size: 14px;
            color: #8da9c4;
            text-align: center;
            position: fixed;
            left: 0; right: 0; bottom: 0;
            background: #f6f9fc;
            padding: 16px 0 10px 0;
            z-index: 9999;
        }
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
    st.markdown("<div class='main-title'>Tweet Sentiment Analysis 🌙</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Fast • Beautiful • Accurate</div>", unsafe_allow_html=True)

    st.markdown("""
        <div class='main-card'>
            <h3>Welcome!</h3>
            <p>Analyze tweet sentiment instantly. Our AI understands slang, emojis, and informal language.</p>
        </div>
        <div class='main-card'>
            <h3>How to Use</h3>
            <ol style='text-align:left; display:inline-block;'>
                <li>Go to "Prediction"</li>
                <li>Type or paste your tweet</li>
                <li>Click <b>Analyze Sentiment</b></li>
                <li>See the result instantly</li>
            </ol>
        </div>
    """, unsafe_allow_html=True)

# -------------------------
# ABOUT PAGE
# -------------------------
elif page == "About":
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.markdown("<div class='main-title'>About This Project</div>", unsafe_allow_html=True)
    st.write("""
        This interactive app predicts tweet sentiment using a trained NLP machine learning model.
        
        ### How It Works
        - Type a tweet  
        - The app calls a hosted API  
        - The API applies an ML pipeline  
        - Sentiment label is returned
        
        Sentiment Labels:
        - **0 = Neutral 😐**
        - **1 = Negative 😠**
        - **2 = Positive 😊**
        
        Handles slang, emojis, abbreviations, and informal language.
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# PREDICTION PAGE
# -------------------------
elif page == "Prediction":
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.markdown("<div class='main-title'>Predict Tweet Sentiment</div>", unsafe_allow_html=True)
    
    tweet = st.text_area("Enter your tweet:", height=140)
    
    # Character counter
    char_class = "warning" if len(tweet) > 280 else ""
    st.markdown(f"<div class='char-counter {char_class}'>{len(tweet)} characters</div>", unsafe_allow_html=True)

    predict_btn = st.button("Analyze Sentiment")
    if predict_btn:
        if not tweet.strip():
            st.markdown("<div class='toast-alert'>⚠️ Please enter a tweet before submitting.</div>", unsafe_allow_html=True)
            st.stop()

        with st.spinner("Analyzing sentiment..."):
            try:
                max_retries = 3
                response = None
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

                if response is None or response.status_code == 429:
                    st.markdown("<div class='toast-alert'>❌ Too many requests. Please wait a few seconds and try again.</div>", unsafe_allow_html=True)
                    st.stop()
                elif response.status_code != 200:
                    st.markdown(f"<div class='toast-alert'>❌ API error ({response.status_code})</div>", unsafe_allow_html=True)
                    st.json({"response_text": response.text})
                    st.stop()

                data = response.json()
                prediction = data.get("prediction", [None])[0]
                if prediction is None:
                    st.markdown("<div class='toast-alert'>❌ API response missing 'prediction'.</div>", unsafe_allow_html=True)
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
                st.markdown("<div class='toast-alert'>⏳ API took too long to respond.</div>", unsafe_allow_html=True)
            except requests.exceptions.ConnectionError:
                st.markdown("<div class='toast-alert'>🔌 Could not connect to API. It may be offline.</div>", unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"<div class='toast-alert'>Unexpected error: {e}</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# Footer
# -------------------------
st.markdown("<div class='footer'>Developed by Ian Kiptoo © 2025 | <a href='#' style='color:#3282b8;text-decoration:none;'>Contact</a></div>", unsafe_allow_html=True)
