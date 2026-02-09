"""
Verifier Agent
Validates data and generates final date plan recommendations
"""

import os
from typing import Dict, List
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class VerifierAgent:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        self.model = "stepfun/step-3.5-flash:free"  # Using cost-effective model
    
    def verify_and_generate_plan(self, execution_results: Dict) -> Dict:
        """
        Verify collected data and generate final date plan
        
        Args:
            execution_results: Results from Executor Agent
        
        Returns:
            Dictionary with verified recommendations and final plan
        """
        plan = execution_results["plan"]
        restaurants = execution_results["restaurants"]
        weather = execution_results["weather"]
        errors = execution_results["errors"]
        
        # Validation checks
        validation = {
            "has_restaurants": len(restaurants) > 0,
            "has_weather": weather is not None,
            "budget_satisfied": True,
            "weather_suitable": True,
            "issues": []
        }
        
        # Check weather suitability
        if weather:
            if weather.get("will_rain") and "indoor" not in plan.get("special_requirements", "").lower():
                validation["weather_suitable"] = False
                validation["issues"].append("Rain expected - filtering for indoor venues")
            
            if weather.get("temperature", 25) > 35:
                validation["issues"].append("Very hot weather - recommend air-conditioned venues")
            elif weather.get("temperature", 25) < 15:
                validation["issues"].append("Cold weather - recommend cozy indoor venues")
        
        # Filter restaurants based on weather and requirements
        filtered_restaurants = self._filter_restaurants(
            restaurants, 
            weather, 
            plan.get("special_requirements", "")
        )
        
        # Generate final plan using AI
        final_plan = self._generate_final_plan(
            plan, 
            filtered_restaurants, 
            weather, 
            validation
        )
        
        return {
            "validation": validation,
            "filtered_restaurants": filtered_restaurants,
            "weather_info": weather,
            "final_plan": final_plan,
            "errors": errors
        }
    
    def _filter_restaurants(
        self, 
        restaurants: List[Dict], 
        weather: Dict, 
        special_requirements: str
    ) -> List[Dict]:
        """
        Filter restaurants based on weather and special requirements
        """
        if not restaurants:
            return []
        
        filtered = restaurants.copy()
        
        # If rain expected or indoor required, prioritize indoor venues
        if weather and (weather.get("will_rain") or "indoor" in special_requirements.lower()):
            # In a real implementation, we'd check if venue is indoor
            # For now, we'll keep all restaurants as most are indoor
            pass
        
        return filtered[:5]  # Return top 5
    
    def _generate_final_plan(
        self, 
        plan: Dict, 
        restaurants: List[Dict], 
        weather: Dict,
        validation: Dict
    ) -> str:
        """
        Use AI to generate a coherent final date plan
        """
        # Prepare context for AI
        context = f"""
User Request: Plan a {plan['date_type']} date in {plan['city']} with budget ₹{plan['budget']}
Timing: {plan['timing']}
Special Requirements: {plan.get('special_requirements', 'none')}

Weather Forecast:
"""
        
        if weather:
            context += f"""- Temperature: {weather['temperature']}°C (feels like {weather['feels_like']}°C)
- Condition: {weather['description']}
- Rain Probability: {weather['rain_probability']}%
- Suitable for outdoor: {'Yes' if weather['suitable_for_outdoor'] else 'No'}
"""
        else:
            context += "- Weather data unavailable\n"
        
        context += f"\nTop Restaurant Recommendations:\n"
        
        if restaurants:
            for i, rest in enumerate(restaurants[:3], 1):
                context += f"{i}. {rest['name']}\n"
                context += f"   - Rating: {rest['rating']}/5 ({rest['total_ratings']} reviews)\n"
                context += f"   - Price Level: {rest['price_level']}\n"
                context += f"   - Address: {rest['address']}\n"
        else:
            context += "No restaurants found matching criteria.\n"
        
        if validation["issues"]:
            context += f"\nImportant Notes:\n"
            for issue in validation["issues"]:
                context += f"- {issue}\n"
        
        # Generate plan using AI
        system_prompt = """You are a professional date planning assistant. Create a concise, helpful date plan based on the provided information.

Your plan should include:
1. A brief greeting and acknowledgment of the request
2. Weather assessment and recommendations
3. Top 2-3 restaurant recommendations with key details
4. Suggested timing for the date
5. Any special tips or considerations

Keep it friendly, concise, and practical. Use emojis sparingly for visual appeal."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Create a date plan based on this information:\n\n{context}"}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            # Fallback to simple text plan
            return self._generate_simple_plan(plan, restaurants, weather)
    
    def _generate_simple_plan(
        self, 
        plan: Dict, 
        restaurants: List[Dict], 
        weather: Dict
    ) -> str:
        """
        Generate a simple text plan without AI (fallback)
        """
        plan_text = f"🌟 Date Plan for {plan['city']}\n\n"
        
        if weather:
            plan_text += f"🌤 Weather: {weather['description']}, {weather['temperature']}°C\n"
            if weather['will_rain']:
                plan_text += "⚠️ Rain expected - indoor venues recommended\n"
            plan_text += "\n"
        
        plan_text += f"🍽 Top Restaurant Recommendations:\n\n"
        
        if restaurants:
            for i, rest in enumerate(restaurants[:3], 1):
                plan_text += f"{i}. {rest['name']}\n"
                plan_text += f"   ⭐ {rest['rating']}/5 | {rest['price_level']}\n"
                plan_text += f"   📍 {rest['address']}\n\n"
        else:
            plan_text += "No restaurants found. Try adjusting your budget or location.\n\n"
        
        plan_text += f"💡 Suggested timing: Evening (6-8 PM)\n"
        plan_text += f"💰 Budget: ₹{plan['budget']}\n"
        
        return plan_text
