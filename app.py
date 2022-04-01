import streamlit as st
import requests
import datetime
import pandas as pd


url = 'https://taxifaire-container-pcccysnixq-uc.a.run.app/predict'

#1. Gathering information from client (form)

pickup_address = st.text_input('Departure address', value="5th avenue, NYC")
dropoff_address = st.text_input('Arrival address', value="JFK airport, NYC")
pickup_day = st.date_input('Pickup day')
pickup_time = st.time_input('Pickup time')
passenger_count = st.number_input('# of passengers', 1, 8)

# 1.1 Transforming addresses to lat-lon
url_geocoding = "https://nominatim.openstreetmap.org/search?"
params_pickup = {
    'q' : pickup_address,
    'format': 'json'
}
params_dropoff = {
    'q' : dropoff_address,
    'format': 'json'
}
response_pickup = requests.get(url_geocoding, params=params_pickup).json()
response_dropoff = requests.get(url_geocoding, params=params_dropoff).json()

pickup_longitude = response_pickup[0]['lon']
pickup_latitude = response_pickup[0]['lat']
dropoff_longitude = response_dropoff[0]['lon']
dropoff_latitude = response_dropoff[0]['lat']

# 1.2 Transforming day and time to datetime

formatted_pickup_datetime = datetime.datetime.combine(pickup_day, pickup_time)

#2. Let's build a dictionary containing the parameters for our API...

params = {'pickup_datetime': [formatted_pickup_datetime],
        'pickup_longitude': [float(pickup_longitude)],
        'pickup_latitude': [float(pickup_latitude)],
        'dropoff_longitude': [float(dropoff_longitude)],
        'dropoff_latitude': [float(dropoff_latitude)],
        'passenger_count': [int(passenger_count)]
}

#3. Let's call our API using the `requests` package...

response = requests.get(url, params=params)

#4. Let's retrieve the prediction from the **JSON** returned by the API...

json_resp = response.json()

## Finally, we can display the prediction to the user

df= pd.DataFrame([
    [float(pickup_latitude), float(pickup_longitude)],
    [float(dropoff_latitude), float(dropoff_longitude)]],
    columns=['lat', 'lon']
)

st.map(df)

st.metric('Predicted price', json_resp['predicted_fare'])
