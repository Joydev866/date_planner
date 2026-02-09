"""
Executor Agent
Orchestrates API calls and collects data from external services
"""

from typing import Dict, List
from tools.places_api import PlacesAPI
from tools.weather_api import WeatherAPI

class ExecutorAgent:
    def __init__(self):
        self.places_api = PlacesAPI()
        self.weather_api = WeatherAPI()
    
    def execute(self, plan: Dict) -> Dict:
        """
        Execute the plan by calling necessary APIs
        
        Args:
            plan: Dictionary from Planner Agent with extracted parameters
        
        Returns:
            Dictionary with collected data from APIs
        """
        results = {
            "plan": plan,
            "restaurants": [],
            "weather": None,
            "errors": []
        }
        
        # Fetch restaurants if needed
        if plan.get("needs_restaurants", True):
            try:
                restaurants = self.places_api.search_restaurants(
                    city=plan["city"],
                    budget=plan["budget"],
                    date_type=plan["date_type"]
                )
                results["restaurants"] = restaurants
                
                if not restaurants:
                    results["errors"].append("No restaurants found matching criteria")
                    
            except Exception as e:
                results["errors"].append(f"Error fetching restaurants: {str(e)}")
        
        # Fetch weather if needed
        if plan.get("needs_weather", True):
            try:
                # Determine days ahead based on timing
                days_ahead = self._parse_timing(plan.get("timing", "today"))
                
                weather = self.weather_api.get_weather_forecast(
                    city=plan["city"],
                    days_ahead=days_ahead
                )
                results["weather"] = weather
                
                if not weather:
                    results["errors"].append("Weather data unavailable")
                    
            except Exception as e:
                results["errors"].append(f"Error fetching weather: {str(e)}")
        
        return results
    
    def _parse_timing(self, timing: str) -> int:
        """
        Convert timing string to days ahead
        
        Args:
            timing: String like "today", "tomorrow", "this weekend"
        
        Returns:
            Number of days ahead (0 for today, 1 for tomorrow, etc.)
        """
        timing_lower = timing.lower()
        
        if "today" in timing_lower or "tonight" in timing_lower:
            return 0
        elif "tomorrow" in timing_lower:
            return 1
        elif "weekend" in timing_lower:
            # Assume this weekend is 2-3 days away
            return 2
        else:
            # Default to today
            return 0
