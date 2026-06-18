import streamlit as st
import pandas as pd
import joblib

# Load the trained model
model = joblib.load("rainfall_model.pkl")

# Page settings
st.set_page_config(
    page_title="Rainfall Prediction",
    page_icon="🌧️",
    layout="centered"
)

st.title("🌧️ Rainfall Prediction System")
st.write("Enter the weather details below to predict the chance of rain.")

# Dropdown options
locations = [
    "Albury", "BadgerysCreek", "Cobar", "CoffsHarbour", "Moree",
    "Newcastle", "NorahHead", "NorfolkIsland", "Penrith", "Richmond",
    "Sydney", "SydneyAirport", "WaggaWagga", "Williamtown", "Wollongong",
    "Canberra", "Tuggeranong", "MountGinini", "Ballarat", "Bendigo",
    "Sale", "MelbourneAirport", "Melbourne", "Mildura", "Nhil",
    "Portland", "Watsonia", "Dartmoor", "Brisbane", "Cairns",
    "GoldCoast", "Townsville", "Adelaide", "MountGambier",
    "Nuriootpa", "Woomera", "Albany", "Witchcliffe", "PearceRAAF",
    "PerthAirport", "Perth", "SalmonGums", "Walpole", "Hobart",
    "Launceston", "AliceSprings", "Darwin", "Katherine", "Uluru"
]

wind_directions = [
    "N", "NNE", "NE", "ENE",
    "E", "ESE", "SE", "SSE",
    "S", "SSW", "SW", "WSW",
    "W", "WNW", "NW", "NNW"
]

# Input fields
location = st.selectbox("Location", locations)

col1, col2 = st.columns(2)

with col1:
    min_temp = st.number_input("Min Temperature (°C)", value=20.0)
    max_temp = st.number_input("Max Temperature (°C)", value=30.0)
    rainfall = st.number_input("Rainfall Today (mm)", value=0.0)
    wind_gust = st.number_input("Wind Gust Speed (km/h)", value=30)
    wind_speed_9am = st.number_input("Wind Speed at 9 AM (km/h)", value=15)
    wind_speed_3pm = st.number_input("Wind Speed at 3 PM (km/h)", value=20)
    humidity_9am = st.slider("Humidity at 9 AM (%)", 0, 100, 60)

with col2:
    humidity_3pm = st.slider("Humidity at 3 PM (%)", 0, 100, 65)
    pressure_9am = st.number_input("Pressure at 9 AM (hPa)", value=1015.0)
    pressure_3pm = st.number_input("Pressure at 3 PM (hPa)", value=1012.0)
    cloud_9am = st.slider("Cloud Cover at 9 AM", 0, 8, 4)
    cloud_3pm = st.slider("Cloud Cover at 3 PM", 0, 8, 5)
    temp_9am = st.number_input("Temperature at 9 AM (°C)", value=22.0)
    temp_3pm = st.number_input("Temperature at 3 PM (°C)", value=28.0)

wind_dir_9am = st.selectbox("Wind Direction at 9 AM", wind_directions)
wind_dir_3pm = st.selectbox("Wind Direction at 3 PM", wind_directions)

rain_today = st.radio("Did it rain today?", ["No", "Yes"])

# Predict button
if st.button("Predict Rainfall"):

    user_data = pd.DataFrame({
        "Location": [location],
        "MinTemp": [min_temp],
        "MaxTemp": [max_temp],
        "Rainfall": [rainfall],
        "WindGustSpeed": [wind_gust],
        "WindDir9am": [wind_dir_9am],
        "WindDir3pm": [wind_dir_3pm],
        "WindSpeed9am": [wind_speed_9am],
        "WindSpeed3pm": [wind_speed_3pm],
        "Humidity9am": [humidity_9am],
        "Humidity3pm": [humidity_3pm],
        "Pressure9am": [pressure_9am],
        "Pressure3pm": [pressure_3pm],
        "Cloud9am": [cloud_9am],
        "Cloud3pm": [cloud_3pm],
        "Temp9am": [temp_9am],
        "Temp3pm": [temp_3pm],
        "RainToday": [rain_today]
    })

    rain_probability = model.predict_proba(user_data)[0][1]
    rain_percentage = rain_probability * 100

    st.subheader("Prediction Result")

    st.metric(
        label="Chance of Rain",
        value=f"{rain_percentage:.2f}%"
    )

    if rain_percentage >= 70:
        st.error("🌧️ High chance of rain")

    elif rain_percentage >= 40:
        st.warning("⛅ Moderate chance of rain")

    else:
        st.success("☀️ Low chance of rain")