import streamlit as st
import joblib
import pandas as pd

st.set_page_config(
    page_title="Airline Price Prediction",
    page_icon="✈️",
    layout="wide"
)

# Custom design
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #eef5ff 0%, #f8faff 55%, #e8f2ff 100%);
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1150px;
}
.hero {
    background: linear-gradient(120deg, #102a56, #1769aa);
    padding: 32px;
    border-radius: 22px;
    color: white;
    margin-bottom: 25px;
    box-shadow: 0 8px 25px rgba(16, 42, 86, 0.18);
}
.hero h1 {
    color: white;
    font-size: 36px;
    margin-bottom: 8px;
}
.hero p {
    color: #e1edff;
    font-size: 16px;
}
.section {
    background: white;
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #dce8f8;
    margin-bottom: 18px;
}
.price-card {
    background: linear-gradient(120deg, #0d326b, #1683c7);
    color: white;
    padding: 28px;
    border-radius: 20px;
    text-align: center;
    margin-top: 20px;
    box-shadow: 0 8px 24px rgba(22, 105, 170, 0.2);
}
.price-label {
    font-size: 16px;
    color: #d9edff;
}
.price-value {
    font-size: 38px;
    font-weight: 800;
    margin-top: 8px;
}
div.stButton > button {
    background: linear-gradient(90deg, #1769aa, #1683c7);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 24px;
    font-weight: 700;
    width: 100%;
}
div.stButton > button:hover {
    color: white;
    border: 1px solid #1769aa;
}
</style>
""", unsafe_allow_html=True)

# Load saved files
model = joblib.load("flight_price_model.joblib")
options = joblib.load("flight_options.joblib")
duration_lookup = pd.read_csv("flight_duration_lookup.csv")

# Header
st.markdown("""
<div class="hero">
    <h1>✈️ Airline Price Prediction</h1>

    <p>Smart Flight Fare Estimator | Machine Learning Project</p>
    <p>Choose your journey details to estimate your ticket price.</p>
</div>
""", unsafe_allow_html=True)
# Project Introduction
st.markdown("""
<div class="section">
    <h2>Welcome to Your Smart Flight Fare Estimator</h2>
    <p>
        Planning a trip? This application uses Machine Learning
        to estimate airline ticket prices based on your selected
        flight details.
    </p>
    <p>
        Choose your airline, route, travel class, departure time,
        flight duration, and days remaining before departure to
        generate an estimated fare.
    </p>
</div>
""", unsafe_allow_html=True)
# Flight details
st.markdown("### 🧳 Plan Your Journey")
st.markdown('<div class="section">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    airline = st.selectbox("✈️ Airline", options["airline"])
    source_city = st.selectbox("📍 Source City", options["source_city"])
    destination_city = st.selectbox(
        "🏁 Destination City", options["destination_city"]
    )
    flight_class = st.selectbox("💺 Class", options["class"])
    stops = st.selectbox("🔄 Stops", options["stops"])

with col2:
    departure_time = st.selectbox(
        "🌅 Departure Time", options["departure_time"]
    )
    arrival_time = st.selectbox(
        "🌇 Arrival Time", options["arrival_time"]
    )
    
    days_left = st.number_input(
        "📅 Days Left Before Departure",
        min_value=1, value=15, step=1
    )
    # Automatically estimate flight duration
matching_flights = duration_lookup[
    (duration_lookup["airline"] == airline)
    & (duration_lookup["source_city"] == source_city)
    & (duration_lookup["destination_city"] == destination_city)
]

if not matching_flights.empty:
    duration = round(float(matching_flights["duration"].iloc[0]),2)
    st.info(f"⏱️ Estimated Flight Duration: {duration:.2f} hours")
else:
    duration = None
    st.warning("No duration data available for this flight route.")

st.markdown('</div>', unsafe_allow_html=True)

# Prediction
st.markdown("### 💰 Estimate Your Fare")

if st.button("✨ Predict Ticket Price") and duration is not None :
    input_data = pd.DataFrame([{
        "airline": airline,
        "source_city": source_city,
        "departure_time": departure_time,
        "stops": stops,
        "arrival_time": arrival_time,
        "destination_city": destination_city,
        "class": flight_class,
        "duration": duration,
        "days_left": days_left
    }])

    prediction = model.predict(input_data)[0]

    st.markdown(f"""
    <div class="price-card">
        <div class="price-label">Estimated Ticket Price</div>
        <div class="price-value">₹{prediction:,.2f}</div>
        <p>✈️ Your estimated fare is ready!</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🧳 Your Flight Summary")

    st.markdown(f"""
    <div class="section">
        <h3>✈️ {airline}</h3>
        <h2>{source_city} → {destination_city}</h2>
        <hr>
        <p><b>💺 Travel Class:</b> {flight_class}</p>
        <p><b>🔄 Stops:</b> {stops}</p>
        <p><b>🌅 Departure:</b> {departure_time}</p>
        <p><b>🌇 Arrival:</b> {arrival_time}</p>
        <p><b>⏱️ Duration:</b> {duration} hours</p>
        <p><b>📅 Days before departure:</b> {days_left}</p>
    </div>
    """, unsafe_allow_html=True)

    st.caption(
        "Note: This is a machine-learning estimate, not a guaranteed market fare."
    )

    st.caption(
        "Note: This is a machine-learning estimate, not a guaranteed market fare."
    )
    st.markdown("---")
st.markdown("## 📘 About This Project")

st.write("""
This Airline Price Prediction application uses Machine Learning
to estimate flight ticket prices based on selected flight details.

*Key Features:*
- Select airline and travel cities.
- Choose travel class, stops, and timings.
- Estimate flight duration automatically.
- Predict the approximate ticket price using a trained Machine Learning model.

*Technology Used:* Python, Pandas, Scikit-learn, and Streamlit.
""")

st.caption("Note: Predicted prices are estimates and may differ from actual ticket prices.")
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Developed by Tripti Kedia | Machine Learning Project ✈️"
    "</div>",
    unsafe_allow_html=True
)