"""
AI Date Planner Assistant
Main orchestration logic for multi-agent date planning system
"""

import sys
from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent
from agents.verifier import VerifierAgent

def print_banner():
    """Print welcome banner"""
    banner = """
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║        💘 AI Date Planner Assistant 💘                    ║
║                                                          ║
║     Plan the perfect date with AI-powered insights!      ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""
    print(banner)

def print_separator():
    """Print a visual separator"""
    print("\n" + "="*60 + "\n")

def main():
    """Main orchestration function"""
    print_banner()
    
    # Initialize agents
    try:
        print("🔧 Initializing AI agents...")
        planner = PlannerAgent()
        executor = ExecutorAgent()
        verifier = VerifierAgent()
        print("✅ All agents ready!\n")
    except Exception as e:
        print(f"❌ Error initializing agents: {e}")
        print("\nPlease ensure:")
        print("1. OPENAI_API_KEY is set in .env file")
        print("2. GOOGLE_PLACES_API is set in .env file")
        print("3. OPEN_WEATHER_API is set in .env file")
        sys.exit(1)
    
    print_separator()
    
    # Get user input
    print("📝 Tell me about your ideal date!")
    print("\nExamples:")
    print('  • "Plan a romantic dinner date in Mumbai under ₹2500"')
    print('  • "Suggest a cozy café date in Delhi this weekend"')
    print('  • "Plan an indoor date in Bangalore if it rains"')
    print('  • "Find a budget-friendly first date in Pune"\n')
    
    user_prompt = input("Your request: ").strip()
    
    if not user_prompt:
        print("❌ No input provided. Exiting.")
        sys.exit(0)
    
    print_separator()
    
    # Step 1: Planner Agent
    print("🧠 Step 1: Understanding your request...")
    try:
        plan = planner.extract_intent(user_prompt)
        print(f"✅ Extracted plan:")
        print(f"   📍 City: {plan['city']}")
        print(f"   💰 Budget: ₹{plan['budget']}")
        print(f"   💕 Date Type: {plan['date_type']}")
        print(f"   ⏰ Timing: {plan['timing']}")
        if plan.get('special_requirements') != 'none':
            print(f"   ⚠️  Special: {plan['special_requirements']}")
        
        # Validate the plan with guardrails
        from validators import InputValidator
        validator = InputValidator()
        is_valid, error_msg, corrected_plan = validator.validate_plan(plan)
        
        if not is_valid:
            print(f"\n⚠️  Validation warnings: {error_msg}")
            print("   Using corrected values...")
            plan = corrected_plan
            print(f"   📍 City: {plan['city']}")
            print(f"   💰 Budget: ₹{plan['budget']}")
            print(f"   ⏰ Timing: {plan['timing']}")
            
    except Exception as e:
        print(f"❌ Error in planning: {e}")
        sys.exit(1)
    
    print_separator()
    
    # Step 2: Executor Agent
    print("⚙️  Step 2: Fetching live data from APIs...")
    try:
        execution_results = executor.execute(plan)
        
        restaurants_count = len(execution_results.get('restaurants', []))
        weather_available = execution_results.get('weather') is not None
        
        print(f"✅ Data collected:")
        print(f"   🍽  Found {restaurants_count} restaurants")
        print(f"   🌤  Weather data: {'Available' if weather_available else 'Unavailable'}")
        
        if execution_results.get('errors'):
            print(f"   ⚠️  Warnings:")
            for error in execution_results['errors']:
                print(f"      - {error}")
                
    except Exception as e:
        print(f"❌ Error executing plan: {e}")
        sys.exit(1)
    
    print_separator()
    
    # Step 3: Verifier Agent
    print("✅ Step 3: Verifying and generating your date plan...")
    try:
        final_result = verifier.verify_and_generate_plan(execution_results)
        
        validation = final_result['validation']
        print(f"✅ Validation complete:")
        print(f"   ✓ Restaurants: {'Found' if validation['has_restaurants'] else 'Not found'}")
        print(f"   ✓ Weather: {'Available' if validation['has_weather'] else 'Unavailable'}")
        print(f"   ✓ Budget: {'Satisfied' if validation['budget_satisfied'] else 'Needs adjustment'}")
        
    except Exception as e:
        print(f"❌ Error in verification: {e}")
        sys.exit(1)
    
    print_separator()
    
    # Display final plan
    print("🎉 YOUR PERSONALIZED DATE PLAN\n")
    print(final_result['final_plan'])
    
    print_separator()
    
    # Display detailed restaurant info
    if final_result['filtered_restaurants']:
        print("📋 DETAILED RESTAURANT INFORMATION\n")
        for i, restaurant in enumerate(final_result['filtered_restaurants'][:3], 1):
            print(f"{i}. {restaurant['name']}")
            print(f"   ⭐ Rating: {restaurant['rating']}/5 ({restaurant['total_ratings']} reviews)")
            print(f"   💵 Price: {restaurant['price_level']}")
            print(f"   📍 Address: {restaurant['address']}")
            if restaurant.get('is_open') is not None:
                status = "🟢 Open now" if restaurant['is_open'] else "🔴 Closed now"
                print(f"   {status}")
            print()
    
    print_separator()
    print("✨ Enjoy your date! ✨\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Have a great day!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
