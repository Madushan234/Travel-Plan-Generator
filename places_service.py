from config.config import get_google_api_key
import requests
import os
import pandas as pd
import joblib
from datetime import datetime


API_KEY = get_google_api_key()

def determine_season(latitude, month):
    northern_hemisphere_seasons = {
        (12, 1, 2): "Winter",
        (3, 4, 5): "Spring",
        (6, 7, 8): "Summer",
        (9, 10, 11): "Autumn"
    }
    southern_hemisphere_seasons = {
        (12, 1, 2): "Summer",
        (3, 4, 5): "Autumn",
        (6, 7, 8): "Winter",
        (9, 10, 11): "Spring"
    }
    
    if latitude >= 0:  # Northern Hemisphere
        for months, season in northern_hemisphere_seasons.items():
            if month in months:
                return season
    else:  # Southern Hemisphere
        for months, season in southern_hemisphere_seasons.items():
            if month in months:
                return season
    return "Unknown"


def get_lat_lng(location_name):
    """Get latitude and longitude for a location using Google Geocoding API."""
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location_name}&key={API_KEY}"
    response = requests.get(geocode_url)
    if response.status_code != 200:
        return None, None
    data = response.json()
    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng'], data['results'][0]['place_id']
    else:
        return None, None


def nearby_search(lat, lng, radius=1000):
    """Search for nearby tourist attractions, parks, hotels, etc."""
    places_url = (
        f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
        f"location={lat},{lng}&radius={radius}&type=tourist_attraction|zoo|park|museum|hotel|airport|bus_station|train_station"
        f"&key={API_KEY}"
    )
    response = requests.get(places_url)
    if response.status_code != 200:
        return []
    data = response.json()
    if data['status'] == 'OK':
        return data['results']
    else:
        return []


def get_place_details(place_id):
    """Fetch details like phone number, website, and opening hours for a place."""
    details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,rating,user_ratings_total,formatted_address,international_phone_number,opening_hours,website&key={API_KEY}"
    response = requests.get(details_url)
    if response.status_code != 200:
        return {}
    data = response.json()
    if data['status'] == 'OK':
        return data['result']
    else:
        return {}


def fetch_weather_data(lat, lon, search_place_details):
    """Fetch weather data for the given latitude and longitude."""
    api_url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
        f"&daily=weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset,"
        f"daylight_duration,sunshine_duration,precipitation_sum,rain_sum,showers_sum,"
        f"snowfall_sum,wind_speed_10m_max&timezone=GMT&forecast_days=7"
    )

    response = requests.get(api_url)
    if response.status_code == 200:
        weather_data = response.json()

        travel_suitability_score_model = joblib.load('travel_suitability_score_model.pkl')
        best_travel_time_model = joblib.load('best_travel_time_model.pkl')


        weather_list = []
        for i in range(len(weather_data['daily']['time'])):

            date_str = weather_data['daily']['time'][i]
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            month = date_obj.month
            season = determine_season(lat, month)

            new_data = pd.DataFrame({
                'Maximum temperature (Â°C)': [weather_data['daily']['temperature_2m_max'][i]],
                'Minimum temperature (Â°C)': [weather_data['daily']['temperature_2m_min'][i]],
                'Precipitation Sum (mm)': [weather_data['daily']['precipitation_sum'][i]],
                'Wind Speed Max (km/h)': [weather_data['daily']['wind_speed_10m_max'][i]],
                'Sunshine Duration (Seconds)': [weather_data['daily']['sunshine_duration'][i]],
                'Daylight Duration (Seconds)': [weather_data['daily']['daylight_duration'][i]],
                'Weather condition code (WMO code)': [weather_data['daily']['weather_code'][i]],
            })
            predicted_score = travel_suitability_score_model.predict(new_data)

            season_encoded = {
                "Winter": 0,
                "Spring": 1,
                "Summer": 2,
                "Autumn": 3,
                "Unknown": -1
            }[season]
            rating = search_place_details.get('rating', '4.0')
            try:
                rating = float(rating) if rating != 'N/A' else 4.0
            except ValueError:
                rating = 4.0
            best_travel_time_model_data = pd.DataFrame({
                'Rating': [rating],
                'Precipitation Sum (mm)': [weather_data['daily']['precipitation_sum'][i]],
                'Maximum temperature (°C)': [weather_data['daily']['temperature_2m_max'][i]],
                'Minimum temperature (°C)': [weather_data['daily']['temperature_2m_min'][i]],
                'Wind Speed Max (km/h)': [weather_data['daily']['wind_speed_10m_max'][i]],
                'Season_Encoded': [season_encoded],
                'Place Type_park': [1 if 'park' in search_place_details.get('types', []) else 0],
                'Place Type_tourist_attraction': [1 if 'tourist_attraction' in search_place_details.get('types', []) else 0],
                'Place Type_zoo': [1 if 'zoo' in search_place_details.get('types', []) else 0]
            })
            best_travel_time_model_score = best_travel_time_model.predict(best_travel_time_model_data)
            season_mapping = {0: 'Winter', 1: 'Spring', 2: 'Summer', 3: 'Autumn'}
            weather_code = weather_data['daily']['weather_code'][i]
            weather_description = get_weather_code_description(weather_code)
            weather_list.append({
                "Date": weather_data['daily']['time'][i],
                "Season": season,
                "Best Travel Time (season)": season_mapping[best_travel_time_model_score[0]],
                "Weather": weather_description,
                "Max Temperature (°C)": weather_data['daily']['temperature_2m_max'][i],
                "Min Temperature (°C)": weather_data['daily']['temperature_2m_min'][i],
                "Sunrise": weather_data['daily']['sunrise'][i],
                "Sunset": weather_data['daily']['sunset'][i],
                "Daylight Duration (s)": weather_data['daily']['daylight_duration'][i],
                "Sunshine Duration (s)": weather_data['daily']['sunshine_duration'][i],
                "Precipitation (mm)": weather_data['daily']['precipitation_sum'][i],
                "Rain Sum (mm)": weather_data['daily']['rain_sum'][i],
                "Showers Sum (mm)": weather_data['daily']['showers_sum'][i],
                "Snowfall Sum (cm)": weather_data['daily']['snowfall_sum'][i],
                "Wind Speed Max (km/h)": weather_data['daily']['wind_speed_10m_max'][i],
                "predicted_travel_suitability_score": round(predicted_score[0], 2)
            })

        return weather_list
    else:
        return []


wmo_weather_codes = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Drizzle: Light intensity",
    53: "Drizzle: Moderate intensity",
    55: "Drizzle: Dense intensity",
    56: "Freezing Drizzle: Light intensity",
    57: "Freezing Drizzle: Dense intensity",
    61: "Rain: Slight intensity",
    63: "Rain: Moderate intensity",
    65: "Rain: Heavy intensity",
    66: "Freezing Rain: Light intensity",
    67: "Freezing Rain: Heavy intensity",
    71: "Snow fall: Slight intensity",
    73: "Snow fall: Moderate intensity",
    75: "Snow fall: Heavy intensity",
    77: "Snow grains",
    80: "Rain showers: Slight intensity",
    81: "Rain showers: Moderate intensity",
    82: "Rain showers: Violent intensity",
    85: "Snow showers: Slight intensity",
    86: "Snow showers: Heavy intensity",
    95: "Thunderstorm: Slight or moderate",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail"
}

def get_weather_code_description(weather_code):
    """Return the description for a given WMO weather code."""
    return wmo_weather_codes.get(weather_code, "Unknown weather condition")
