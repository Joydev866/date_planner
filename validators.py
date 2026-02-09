"""
Input Validation and Guardrails
Validates user inputs and ensures safe, reasonable date planning
"""

from datetime import datetime, timedelta
from typing import Dict, Tuple
import re

class InputValidator:
    """Validates and sanitizes user inputs for date planning"""
    
    # Supported cities with coordinates
    SUPPORTED_CITIES = {
        "mumbai", "delhi", "bangalore", "bengaluru", "hyderabad", 
        "chennai", "kolkata", "pune", "ahmedabad", "jaipur",
        "surat", "lucknow", "kanpur", "nagpur", "indore",
        "thane", "bhopal", "visakhapatnam", "pimpri-chinchwad", 
        "patna", "gurgaon", "gurugram", "noida", "ghaziabad"
    }
    
    # Budget constraints
    MIN_BUDGET = 500
    MAX_BUDGET = 50000
    
    def __init__(self):
        self.current_date = datetime.now()
    
    def validate_plan(self, plan: Dict) -> Tuple[bool, str, Dict]:
        """
        Validate the extracted plan from Planner Agent
        
        Args:
            plan: Dictionary with extracted parameters
        
        Returns:
            Tuple of (is_valid, error_message, corrected_plan)
        """
        corrected_plan = plan.copy()
        errors = []
        
        # 1. Validate City
        city_valid, city_error, corrected_city = self._validate_city(plan.get('city', ''))
        if not city_valid:
            errors.append(city_error)
        corrected_plan['city'] = corrected_city
        
        # 2. Validate Budget
        budget_valid, budget_error, corrected_budget = self._validate_budget(plan.get('budget', 0))
        if not budget_valid:
            errors.append(budget_error)
        corrected_plan['budget'] = corrected_budget
        
        # 3. Validate Date/Time (most important guardrail)
        date_valid, date_error, corrected_timing = self._validate_date_time(plan.get('timing', 'today'))
        if not date_valid:
            errors.append(date_error)
        corrected_plan['timing'] = corrected_timing
        
        # 4. Validate Date Type
        date_type_valid, type_error, corrected_type = self._validate_date_type(plan.get('date_type', ''))
        if not date_type_valid:
            errors.append(type_error)
        corrected_plan['date_type'] = corrected_type
        
        # Return validation result
        if errors:
            return False, " | ".join(errors), corrected_plan
        return True, "", corrected_plan
    
    def _validate_city(self, city: str) -> Tuple[bool, str, str]:
        """Validate city is supported"""
        city_lower = city.lower().strip()
        
        if not city_lower:
            return False, "City not specified", "Bangalore"
        
        if city_lower not in self.SUPPORTED_CITIES:
            return False, f"City '{city}' not supported. Using Bangalore instead.", "Bangalore"
        
        return True, "", city
    
    def _validate_budget(self, budget: int) -> Tuple[bool, str, int]:
        """Validate budget is within reasonable range"""
        try:
            budget = int(budget)
        except (ValueError, TypeError):
            return False, f"Invalid budget. Using default ₹2000.", 2000
        
        if budget < self.MIN_BUDGET:
            return False, f"Budget too low (minimum ₹{self.MIN_BUDGET}). Adjusted to ₹{self.MIN_BUDGET}.", self.MIN_BUDGET
        
        if budget > self.MAX_BUDGET:
            return False, f"Budget too high (maximum ₹{self.MAX_BUDGET}). Adjusted to ₹{self.MAX_BUDGET}.", self.MAX_BUDGET
        
        return True, "", budget
    
    def _validate_date_time(self, timing: str) -> Tuple[bool, str, str]:
        """
        Validate that the date/time is not in the past
        This is the main guardrail to prevent planning dates that have already passed
        """
        timing_lower = timing.lower().strip()
        
        # Handle common timing keywords
        if timing_lower in ['today', 'tonight', 'this evening']:
            return True, "", timing
        
        if timing_lower in ['tomorrow']:
            return True, "", timing
        
        if 'weekend' in timing_lower or 'this week' in timing_lower:
            return True, "", timing
        
        # Try to parse specific dates
        date_patterns = [
            (r'(\d{1,2})(st|nd|rd|th)?\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)', '%d %b'),
            (r'(\d{1,2})(st|nd|rd|th)?\s+(january|february|march|april|may|june|july|august|september|october|november|december)', '%d %B'),
            (r'(\d{1,2})/(\d{1,2})/(\d{4})', '%d/%m/%Y'),
            (r'(\d{4})-(\d{1,2})-(\d{1,2})', '%Y-%m-%d'),
        ]
        
        for pattern, date_format in date_patterns:
            match = re.search(pattern, timing_lower, re.IGNORECASE)
            if match:
                try:
                    # Extract date string
                    date_str = match.group(0)
                    # Remove ordinal suffixes (st, nd, rd, th)
                    date_str = re.sub(r'(st|nd|rd|th)', '', date_str)
                    
                    # Parse the date
                    parsed_date = datetime.strptime(date_str, date_format)
                    
                    # If year is not specified, assume current year
                    if parsed_date.year == 1900:
                        parsed_date = parsed_date.replace(year=self.current_date.year)
                    
                    # Check if date is in the past
                    if parsed_date.date() < self.current_date.date():
                        # If it's in the past, it might be next year
                        if parsed_date.month < self.current_date.month:
                            parsed_date = parsed_date.replace(year=self.current_date.year + 1)
                            return True, f"⚠️ Date adjusted to {parsed_date.strftime('%B %d, %Y')} (next year)", parsed_date.strftime('%B %d')
                        else:
                            return False, f"❌ Date '{timing}' is in the past. Please choose a future date.", "today"
                    
                    return True, "", timing
                    
                except ValueError:
                    continue
        
        # If we can't parse it, assume it's okay (might be relative like "next week")
        return True, "", timing
    
    def _validate_date_type(self, date_type: str) -> Tuple[bool, str, str]:
        """Validate date type is reasonable"""
        valid_types = ['romantic', 'casual', 'cozy', 'budget', 'budget-friendly', 'formal', 'fun']
        
        date_type_lower = date_type.lower().strip()
        
        if not date_type_lower:
            return False, "Date type not specified. Using 'casual'.", "casual"
        
        if date_type_lower not in valid_types:
            # Allow it but note it
            return True, "", date_type
        
        return True, "", date_type
    
    def get_supported_cities_list(self) -> str:
        """Get formatted list of supported cities"""
        cities = sorted(list(self.SUPPORTED_CITIES))
        return ", ".join([city.title() for city in cities[:10]]) + ", and more..."
