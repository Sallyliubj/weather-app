from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv


app = Flask(__name__)

load_dotenv()
API_KEY = os.getenv('OPENWEATHER_API_KEY')
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
FORECAST_URL = 'https://api.openweathermap.org/data/2.5/forecast'


@app.route('/')
def home():
    return render_template('index.html')

# Route to handle current weather requests
@app.route('/get_weather', methods=['POST'])
def get_weather():
    city = request.form.get('city')
    if not city:
        return jsonify({'error': 'City name is required'}), 400

    # Call the OpenWeatherMap API for current weather
    response = requests.get(BASE_URL, params={
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    })

    if response.status_code != 200:
        return jsonify({'error': 'Unable to get weather data'}), response.status_code

    data = response.json()

    # Extract useful information from API response
    weather = {
        'city': data['name'],
        'temperature': data['main']['temp'],
        'feels_like': data['main']['feels_like'],
        'humidity': data['main']['humidity'],
        'description': data['weather'][0]['description'],
        'icon': data['weather'][0]['icon'],
    }

    # Call the OpenWeatherMap API for a 5-day forecast
    forecast_response = requests.get(FORECAST_URL, params={
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    })

    if forecast_response.status_code != 200:
        return jsonify({'error': 'Unable to get forecast data'}), forecast_response.status_code

    forecast_data = forecast_response.json()
    forecasts = []
    unique_dates = set()

    # Extract useful forecast information
    for item in forecast_data['list']:
        forecast_date = item['dt_txt'].split(' ')[0]
        forecast_time = item['dt_txt'].split(' ')[1]
        # Only include forecasts around midday (e.g., 12:00:00) to represent daytime
        if forecast_time == '12:00:00' and forecast_date not in unique_dates:
            unique_dates.add(forecast_date)
            forecast = {
                'datetime': item['dt_txt'],
                'temperature': item['main']['temp'],
                'description': item['weather'][0]['description'],
                'icon': item['weather'][0]['icon'],
            }
            forecasts.append(forecast)

    return render_template('weather.html', weather=weather, forecasts=forecasts)



# Route to get weather based on user's location
@app.route('/get_weather_by_location', methods=['POST'])
def get_weather_by_location():
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    if not latitude or not longitude:
        return jsonify({'error': 'Latitude and Longitude are required'}), 400

    # Call the OpenWeatherMap API for current weather by geographic coordinates
    response = requests.get(BASE_URL, params={
        'lat': latitude,
        'lon': longitude,
        'appid': API_KEY,
        'units': 'metric'
    })

    if response.status_code != 200:
        return jsonify({'error': 'Unable to get weather data'}), response.status_code

    data = response.json()

    # Extract useful information from API response
    weather = {
        'city': data['name'],
        'temperature': data['main']['temp'],
        'feels_like': data['main']['feels_like'],
        'humidity': data['main']['humidity'],
        'description': data['weather'][0]['description'],
        'icon': data['weather'][0]['icon'],
    }

    # Call the OpenWeatherMap API for a 5-day forecast
    forecast_response = requests.get(FORECAST_URL, params={
        'lat': latitude,
        'lon': longitude,
        'appid': API_KEY,
        'units': 'metric'
    })

    if forecast_response.status_code != 200:
        return jsonify({'error': 'Unable to get forecast data'}), forecast_response.status_code

    forecast_data = forecast_response.json()
    forecasts = []
    unique_dates = set()

    # Extract useful forecast information
    for item in forecast_data['list']:
        forecast_date = item['dt_txt'].split(' ')[0]
        forecast_time = item['dt_txt'].split(' ')[1]
        # Only include forecasts around midday (e.g., 12:00:00) to represent daytime
        if forecast_time == '12:00:00' and forecast_date not in unique_dates:
            unique_dates.add(forecast_date)
            forecast = {
                'datetime': item['dt_txt'],
                'temperature': item['main']['temp'],
                'description': item['weather'][0]['description'],
                'icon': item['weather'][0]['icon'],
            }
            forecasts.append(forecast)

    return render_template('weather.html', weather=weather, forecasts=forecasts)



if __name__ == '__main__':
    app.run(debug=True)