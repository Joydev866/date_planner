"""
OpenWeather API Integration Tool
Fetches weather forecasts for date planning
"""

import os
import requests
from datetime import datetime, timedelta
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()

class WeatherAPI:
    def __init__(self):
        self.api_key = os.getenv("OPEN_WEATHER_API")
        if not self.api_key:
            raise ValueError("OPEN_WEATHER_API key not found in environment variables")
        
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    def get_weather_forecast(self, city: str, days_ahead: int = 0) -> Optional[Dict]:
        """
        Get weather forecast for a city
        
        Args:
            city: City name (e.g., "Bangalore", "Mumbai")
            days_ahead: Number of days ahead (0 for today, 1 for tomorrow, etc.)
        
        Returns:
            Dictionary with weather information
        """
        try:
            # Get current weather and forecast
            forecast_url = f"{self.base_url}/forecast"
            params = {
                "q": f"{city},IN",  # IN for India
                "appid": self.api_key,
                "units": "metric"  # Celsius
            }
            
            response = requests.get(forecast_url, params=params)
            data = response.json()
            
            if data.get("cod") != "200":
                return None
            
            # Calculate target date
            target_date = datetime.now() + timedelta(days=days_ahead)
            target_date_str = target_date.strftime("%Y-%m-%d")
            
            # Find forecast for the target date (evening time ~18:00)
            forecasts = data.get("list", [])
            evening_forecast = None
            
            for forecast in forecasts:
                forecast_time = datetime.fromtimestamp(forecast["dt"])
                if forecast_time.strftime("%Y-%m-%d") == target_date_str:
                    hour = forecast_time.hour
                    # Look for evening forecast (18:00 - 21:00)
                    if 18 <= hour <= 21:
                        evening_forecast = forecast
                        break
            
            # If no evening forecast found, use the first forecast for that day
            if not evening_forecast:
                for forecast in forecasts:
                    forecast_time = datetime.fromtimestamp(forecast["dt"])
                    if forecast_time.strftime("%Y-%m-%d") == target_date_str:
                        evening_forecast = forecast
                        break
            
            if not evening_forecast:
                # Fallback to current weather
                current_url = f"{self.base_url}/weather"
                current_response = requests.get(current_url, params=params)
                current_data = current_response.json()
                
                if current_data.get("cod") != 200:
                    return None
                
                return self._parse_current_weather(current_data)
            
            return self._parse_forecast(evening_forecast)
            
        except Exception as e:
            print(f"Error fetching weather: {e}")
            return None
    
    def _parse_forecast(self, forecast: Dict) -> Dict:
        """Parse forecast data into a clean format"""
        weather_main = forecast["weather"][0]["main"]
        weather_desc = forecast["weather"][0]["description"]
        temp = forecast["main"]["temp"]
        feels_like = forecast["main"]["feels_like"]
        humidity = forecast["main"]["humidity"]
        
        # Check for rain
        rain_prob = forecast.get("pop", 0) * 100  # Probability of precipitation
        will_rain = rain_prob > 50 or weather_main.lower() in ["rain", "drizzle", "thunderstorm"]
        
        return {
            "temperature": round(temp, 1),
            "feels_like": round(feels_like, 1),
            "condition": weather_main,
            "description": weather_desc.capitalize(),
            "humidity": humidity,
            "rain_probability": round(rain_prob, 1),
            "will_rain": will_rain,
            "suitable_for_outdoor": not will_rain and 15 <= temp <= 35
        }
    
    def _parse_current_weather(self, data: Dict) -> Dict:
        """Parse current weather data into a clean format"""
        weather_main = data["weather"][0]["main"]
        weather_desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        
        # Check for rain
        will_rain = weather_main.lower() in ["rain", "drizzle", "thunderstorm"]
        
        return {
            "temperature": round(temp, 1),
            "feels_like": round(feels_like, 1),
            "condition": weather_main,
            "description": weather_desc.capitalize(),
            "humidity": humidity,
            "rain_probability": 100 if will_rain else 0,
            "will_rain": will_rain,
            "suitable_for_outdoor": not will_rain and 15 <= temp <= 35
        }
    
    def is_good_weather_for_date(self, weather: Dict) -> tuple[bool, str]:
        """
        Determine if weather is suitable for a date
        
        Returns:
            Tuple of (is_suitable, reason)
        """
        if not weather:
            return True, "Weather data unavailable, plan accordingly"
        
        if weather["will_rain"]:
            return False, f"Rain expected ({weather['rain_probability']}% chance). Consider indoor venues."
        
        temp = weather["temperature"]
        if temp < 15:
            return False, f"Cold weather ({temp}°C). Suggest cozy indoor venues."
        elif temp > 35:
            return False, f"Very hot ({temp}°C). Recommend air-conditioned venues."
        
        return True, f"Pleasant weather ({temp}°C, {weather['description']}). Great for outdoor or indoor dates!"
