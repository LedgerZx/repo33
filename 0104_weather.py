import requests
import json
from datetime import datetime
import sys
import time

def get_weather_data(api_key, city):
    """Fetch weather data from OpenWeatherMap API"""
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'  # Use 'imperial' for Fahrenheit
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def display_weather(weather_data):
    """Display weather data with ASCII art"""
    if not weather_data:
        return
    
    city = weather_data['name']
    country = weather_data['sys']['country']
    temp = weather_data['main']['temp']
    feels_like = weather_data['main']['feels_like']
    humidity = weather_data['main']['humidity']
    pressure = weather_data['main']['pressure']
    wind_speed = weather_data['wind']['speed']
    wind_deg = weather_data['wind']['deg']
    weather_main = weather_data['weather'][0]['main']
    weather_desc = weather_data['weather'][0]['description']
    sunrise = datetime.fromtimestamp(weather_data['sys']['sunrise']).strftime('%H:%M')
    sunset = datetime.fromtimestamp(weather_data['sys']['sunset']).strftime('%H:%M')
    
    # ASCII art for weather conditions
    weather_icons = {
        'Clear': '☀️',
        'Clouds': '☁️',
        'Rain': '🌧️',
        'Drizzle': '🌦️',
        'Thunderstorm': '⛈️',
        'Snow': '❄️',
        'Mist': '🌫️',
        'Fog': '🌫️'
    }
    
    icon = weather_icons.get(weather_main, '🌡️')
    
    # Wind direction
    directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                  'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    wind_dir = directions[int((wind_deg + 11.25) / 22.5) % 16]
    
    # Display
    print("\n" + "="*50)
    print(f"{icon}  Weather in {city}, {country}")
    print("="*50)
    print(f"🌡️  Temperature: {temp}°C (feels like {feels_like}°C)")
    print(f"☁️  Condition: {weather_desc.title()}")
    print(f"💧  Humidity: {humidity}%")
    print(f"🌪️  Wind: {wind_speed} m/s {wind_dir}")
    print(f"📊  Pressure: {pressure} hPa")
    print(f"🌅  Sunrise: {sunrise}")
    print(f"🌇  Sunset: {sunset}")
    print("="*50)
    print(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)

def main():
    # You need to get a free API key from https://openweathermap.org/api
    API_KEY = "YOUR_API_KEY_HERE"  # Replace with your actual API key
    
    if API_KEY == "YOUR_API_KEY_HERE":
        print("Please get a free API key from https://openweathermap.org/api")
        print("and replace 'YOUR_API_KEY_HERE' in the script")
        sys.exit(1)
    
    while True:
        city = input("\nEnter city name (or 'quit' to exit): ").strip()
        
        if city.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if not city:
            continue
        
        print(f"Fetching weather for {city}...")
        weather_data = get_weather_data(API_KEY, city)
        display_weather(weather_data)
        
        if weather_data:
            # Ask if user wants to continue
            choice = input("\nCheck another city? (y/n): ").strip().lower()
            if choice not in ['y', 'yes']:
                break

if __name__ == "__main__":
    main()
