"""
Planner Agent
Extracts structured information from user prompts using OpenAI
"""

import os
import json
from typing import Dict
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class PlannerAgent:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        self.model = "stepfun/step-3.5-flash:free"  # Using cost-effective model
    
    def extract_intent(self, user_prompt: str) -> Dict:
        """
        Extract structured information from user's date planning request
        
        Args:
            user_prompt: Natural language request from user
        
        Returns:
            Dictionary with extracted parameters:
            - city: str
            - budget: int (in INR)
            - date_type: str (romantic, casual, cozy, etc.)
            - timing: str (today, tomorrow, this weekend, etc.)
            - needs_weather: bool
            - needs_restaurants: bool
            - special_requirements: str (indoor, outdoor, etc.)
        """
        
        system_prompt = """You are a date planning assistant. Extract structured information from user requests.

Your task is to analyze the user's date planning request and extract:
1. City name (default to "Bangalore" if not specified)
2. Budget in INR (default to 2000 if not specified)
3. Date type (romantic, casual, cozy, budget-friendly, etc.)
4. Timing (today, tomorrow, this weekend, specific date)
5. Whether weather information is needed (true if outdoor activities or timing mentioned)
6. Whether restaurant recommendations are needed (almost always true)
7. Any special requirements (indoor only, outdoor preferred, etc.)

Return ONLY a valid JSON object with these exact keys:
{
  "city": "string",
  "budget": number,
  "date_type": "string",
  "timing": "string",
  "needs_weather": boolean,
  "needs_restaurants": boolean,
  "special_requirements": "string"
}

Examples:
User: "Plan a romantic dinner date in Mumbai under ₹2500"
Response: {"city": "Mumbai", "budget": 2500, "date_type": "romantic", "timing": "today", "needs_weather": true, "needs_restaurants": true, "special_requirements": "none"}

User: "Suggest a cozy café date in Delhi this weekend"
Response: {"city": "Delhi", "budget": 2000, "date_type": "cozy", "timing": "this weekend", "needs_weather": true, "needs_restaurants": true, "special_requirements": "cafe preferred"}

User: "Plan an indoor date in Bangalore if it rains"
Response: {"city": "Bangalore", "budget": 2000, "date_type": "casual", "timing": "today", "needs_weather": true, "needs_restaurants": true, "special_requirements": "indoor only"}
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3
            )
            
            # Extract JSON from response (handle cases where model adds extra text)
            response_text = response.choices[0].message.content.strip()
            
            # Try to find JSON object in the response
            try:
                # First, try to parse the entire response as JSON
                extracted_data = json.loads(response_text)
            except json.JSONDecodeError:
                # If that fails, try to extract JSON from the text
                import re
                json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response_text)
                if json_match:
                    extracted_data = json.loads(json_match.group())
                else:
                    raise ValueError("No valid JSON found in response")
            
            # Validate and set defaults
            result = {
                "city": extracted_data.get("city", "Bangalore"),
                "budget": int(extracted_data.get("budget", 2000)),
                "date_type": extracted_data.get("date_type", "casual"),
                "timing": extracted_data.get("timing", "today"),
                "needs_weather": extracted_data.get("needs_weather", True),
                "needs_restaurants": extracted_data.get("needs_restaurants", True),
                "special_requirements": extracted_data.get("special_requirements", "none")
            }
            
            return result
            
        except Exception as e:
            print(f"Error in Planner Agent: {e}")
            # Return default values on error
            return {
                "city": "Bangalore",
                "budget": 2000,
                "date_type": "casual",
                "timing": "today",
                "needs_weather": True,
                "needs_restaurants": True,
                "special_requirements": "none"
            }
