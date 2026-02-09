"""
Google Places API (New) Integration Tool
Uses the new Places API v1 with searchText endpoint
"""

import os
import requests
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

class PlacesAPI:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_PLACES_API")
        if not self.api_key:
            raise ValueError("GOOGLE_PLACES_API key not found in environment variables")
        
        self.base_url = "https://places.googleapis.com/v1/places:searchText"
    
    def search_restaurants(
        self, 
        city: str, 
        budget: int, 
        date_type: str = "romantic",
        max_results: int = 10
    ) -> List[Dict]:
        """
        Search for restaurants in a city based on budget and date type
        Uses the new Google Places API (New) with searchText endpoint
        
        Args:
            city: City name (e.g., "Bangalore", "Mumbai")
            budget: Maximum budget in INR
            date_type: Type of date (romantic, casual, cozy, etc.)
            max_results: Maximum number of results to return
        
        Returns:
            List of restaurant dictionaries with details
        """
        try:
            # Determine price level based on budget
            # Price levels: PRICE_LEVEL_INEXPENSIVE, PRICE_LEVEL_MODERATE, 
            #               PRICE_LEVEL_EXPENSIVE, PRICE_LEVEL_VERY_EXPENSIVE
            if budget < 1000:
                price_levels = ["PRICE_LEVEL_INEXPENSIVE"]
            elif budget < 2000:
                price_levels = ["PRICE_LEVEL_INEXPENSIVE", "PRICE_LEVEL_MODERATE"]
            elif budget < 4000:
                price_levels = ["PRICE_LEVEL_INEXPENSIVE", "PRICE_LEVEL_MODERATE", "PRICE_LEVEL_EXPENSIVE"]
            else:
                price_levels = ["PRICE_LEVEL_INEXPENSIVE", "PRICE_LEVEL_MODERATE", "PRICE_LEVEL_EXPENSIVE", "PRICE_LEVEL_VERY_EXPENSIVE"]
            
            # Build search query based on date type
            keywords = {
                "romantic": "romantic fine dining restaurant",
                "casual": "casual restaurant cafe",
                "cozy": "cozy cafe restaurant",
                "budget": "budget friendly restaurant",
                "budget-friendly": "budget friendly restaurant"
            }
            search_keyword = keywords.get(date_type.lower(), "restaurant")
            
            # Construct the text query
            text_query = f"{search_keyword} in {city}"
            
            # Prepare the request body for searchText
            request_body = {
                "textQuery": text_query,
                "maxResultCount": max_results,
                "locationBias": {
                    "circle": {
                        "center": {
                            "latitude": self._get_city_lat(city),
                            "longitude": self._get_city_lng(city)
                        },
                        "radius": 5000.0  # 5km radius
                    }
                }
            }
            
            # Set headers for the new API
            headers = {
                "Content-Type": "application/json",
                "X-Goog-Api-Key": self.api_key,
                "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.rating,places.userRatingCount,places.priceLevel,places.currentOpeningHours"
            }
            
            # Make the API request
            response = requests.post(
                self.base_url,
                json=request_body,
                headers=headers
            )
            
            if response.status_code != 200:
                print(f"API Error: {response.status_code} - {response.text}")
                return []
            
            data = response.json()
            
            # Parse and filter results
            restaurants = []
            for place in data.get("places", []):
                place_price_level = place.get("priceLevel", "PRICE_LEVEL_MODERATE")
                
                # Filter by price level
                if place_price_level in price_levels or place_price_level == "PRICE_LEVEL_UNSPECIFIED":
                    restaurant = {
                        "name": place.get("displayName", {}).get("text", "Unknown"),
                        "rating": place.get("rating", "N/A"),
                        "price_level": self._format_price_level(place_price_level),
                        "address": place.get("formattedAddress", "Address not available"),
                        "is_open": place.get("currentOpeningHours", {}).get("openNow", None),
                        "total_ratings": place.get("userRatingCount", 0)
                    }
                    restaurants.append(restaurant)
            
            # Sort by rating and number of reviews
            restaurants.sort(
                key=lambda x: (x["rating"] if isinstance(x["rating"], (int, float)) else 0, x["total_ratings"]), 
                reverse=True
            )
            
            return restaurants[:5]  # Return top 5
            
        except Exception as e:
            print(f"Error searching restaurants: {e}")
            return []
    
    def _get_city_lat(self, city: str) -> float:
        """Get approximate latitude for major Indian cities"""
        city_coords = {
            "mumbai": 19.0760,
            "delhi": 28.7041,
            "bangalore": 12.9716,
            "bengaluru": 12.9716,
            "hyderabad": 17.3850,
            "chennai": 13.0827,
            "kolkata": 22.5726,
            "pune": 18.5204,
            "ahmedabad": 23.0225,
            "jaipur": 26.9124,
            "surat": 21.1702,
            "lucknow": 26.8467,
            "kanpur": 26.4499,
            "nagpur": 21.1458,
            "indore": 22.7196,
            "thane": 19.2183,
            "bhopal": 23.2599,
            "visakhapatnam": 17.6868,
            "pimpri-chinchwad": 18.6298,
            "patna": 25.5941
        }
        return city_coords.get(city.lower(), 12.9716)  # Default to Bangalore
    
    def _get_city_lng(self, city: str) -> float:
        """Get approximate longitude for major Indian cities"""
        city_coords = {
            "mumbai": 72.8777,
            "delhi": 77.1025,
            "bangalore": 77.5946,
            "bengaluru": 77.5946,
            "hyderabad": 78.4867,
            "chennai": 80.2707,
            "kolkata": 88.3639,
            "pune": 73.8567,
            "ahmedabad": 72.5714,
            "jaipur": 75.7873,
            "surat": 72.8311,
            "lucknow": 80.9462,
            "kanpur": 80.3319,
            "nagpur": 79.0882,
            "indore": 75.8577,
            "thane": 72.9781,
            "bhopal": 77.4126,
            "visakhapatnam": 83.2185,
            "pimpri-chinchwad": 73.7997,
            "patna": 85.1376
        }
        return city_coords.get(city.lower(), 77.5946)  # Default to Bangalore
    
    def _format_price_level(self, price_level: str) -> str:
        """Convert API price level to user-friendly format"""
        price_mapping = {
            "PRICE_LEVEL_INEXPENSIVE": "₹",
            "PRICE_LEVEL_MODERATE": "₹₹",
            "PRICE_LEVEL_EXPENSIVE": "₹₹₹",
            "PRICE_LEVEL_VERY_EXPENSIVE": "₹₹₹₹",
            "PRICE_LEVEL_UNSPECIFIED": "Budget"
        }
        return price_mapping.get(price_level, "₹₹")
