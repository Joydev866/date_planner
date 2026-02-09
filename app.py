"""
Streamlit Web Interface for AI Date Planner Assistant
Beautiful, modern UI for planning dates with AI
"""

import streamlit as st
from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent
from agents.verifier import VerifierAgent
import sys

# Page configuration
st.set_page_config(
    page_title="💘 AI Date Planner",
    page_icon="💘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .restaurant-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
        color: black;
    }
    
    .restaurant-card h3 {
        color: black;
    }
    
    .restaurant-card p {
        color: black;
    }
    
    .weather-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'agents_initialized' not in st.session_state:
    st.session_state.agents_initialized = False
    st.session_state.planner = None
    st.session_state.executor = None
    st.session_state.verifier = None

# Header
st.markdown("""
<div class="main-header">
    <h1>💘 AI Date Planner Assistant</h1>
    <p style="font-size: 1.2rem; margin-top: 0.5rem;">Plan the perfect date with AI-powered insights!</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This AI-powered date planner uses:
    - 🧠 **Multi-Agent AI** for intelligent planning
    - 🍽️ **Google Places API** for restaurant recommendations
    - 🌤️ **OpenWeather API** for weather forecasts
    
    Simply describe your ideal date, and let AI do the rest!
    """)
    
    st.divider()
    
    st.header("📝 Example Prompts")
    example_prompts = [
        "Plan a romantic dinner date in Mumbai under ₹2500",
        "Suggest a cozy café date in Delhi this weekend",
        "Plan an indoor date in Bangalore if it rains",
        "Find a budget-friendly first date in Pune"
    ]
    
    for prompt in example_prompts:
        if st.button(f"💡 {prompt[:30]}...", key=prompt, use_container_width=True):
            st.session_state.user_input = prompt

# Initialize agents
if not st.session_state.agents_initialized:
    with st.spinner("🔧 Initializing AI agents..."):
        try:
            st.session_state.planner = PlannerAgent()
            st.session_state.executor = ExecutorAgent()
            st.session_state.verifier = VerifierAgent()
            st.session_state.agents_initialized = True
            st.success("✅ All agents ready!")
        except Exception as e:
            st.error(f"❌ Error initializing agents: {e}")
            st.info("""
            Please ensure:
            1. OPENAI_API_KEY is set in .env file
            2. GOOGLE_PLACES_API is set in .env file
            3. OPEN_WEATHER_API is set in .env file
            """)
            st.stop()

# Main input area
st.header("🎯 Tell me about your ideal date!")

# Get user input
user_input = st.text_area(
    "Describe your perfect date:",
    value=st.session_state.get('user_input', ''),
    height=100,
    placeholder="e.g., Plan a romantic dinner date in Mumbai under ₹2500 on February 14th",
    key="main_input"
)

# Plan Date button
if st.button("🚀 Plan My Date", type="primary", use_container_width=True):
    if not user_input.strip():
        st.warning("⚠️ Please describe your ideal date first!")
    else:
        # Step 1: Planner Agent
        with st.spinner("🧠 Step 1: Understanding your request..."):
            try:
                plan = st.session_state.planner.extract_intent(user_input)
                
                # Validate the plan with guardrails
                from validators import InputValidator
                validator = InputValidator()
                is_valid, error_msg, corrected_plan = validator.validate_plan(plan)
                
                if not is_valid:
                    st.warning(f"⚠️ Validation warnings: {error_msg}")
                    st.info("Using corrected values...")
                    plan = corrected_plan
                
                # Display extracted plan
                st.success("✅ Extracted plan:")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("📍 City", plan['city'])
                with col2:
                    st.metric("💰 Budget", f"₹{plan['budget']}")
                with col3:
                    st.metric("💕 Date Type", plan['date_type'].title())
                with col4:
                    st.metric("⏰ Timing", plan['timing'].title())
                
                if plan.get('special_requirements') != 'none':
                    st.info(f"⚠️ Special: {plan['special_requirements']}")
                    
            except Exception as e:
                st.error(f"❌ Error in planning: {e}")
                st.stop()
        
        st.divider()
        
        # Step 2: Executor Agent
        with st.spinner("⚙️ Step 2: Fetching live data from APIs..."):
            try:
                execution_results = st.session_state.executor.execute(plan)
                
                restaurants_count = len(execution_results.get('restaurants', []))
                weather_available = execution_results.get('weather') is not None
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("🍽️ Restaurants Found", restaurants_count)
                with col2:
                    st.metric("🌤️ Weather Data", "Available" if weather_available else "Unavailable")
                
                if execution_results.get('errors'):
                    with st.expander("⚠️ Warnings"):
                        for error in execution_results['errors']:
                            st.warning(error)
                            
            except Exception as e:
                st.error(f"❌ Error executing plan: {e}")
                st.stop()
        
        st.divider()
        
        # Step 3: Verifier Agent
        with st.spinner("✅ Step 3: Verifying and generating your date plan..."):
            try:
                final_result = st.session_state.verifier.verify_and_generate_plan(execution_results)
                
                validation = final_result['validation']
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    status = "✅ Found" if validation['has_restaurants'] else "❌ Not found"
                    st.metric("Restaurants", status)
                with col2:
                    status = "✅ Available" if validation['has_weather'] else "❌ Unavailable"
                    st.metric("Weather", status)
                with col3:
                    status = "✅ Satisfied" if validation['budget_satisfied'] else "⚠️ Needs adjustment"
                    st.metric("Budget", status)
                    
            except Exception as e:
                st.error(f"❌ Error in verification: {e}")
                st.stop()
        
        
        st.divider()
        
        # Display final plan
        st.header("🎉 Your Personalized Date Plan")
        
        # Display the plan with proper formatting
        if final_result.get('final_plan'):
            # Use st.write for better markdown rendering
            st.write(final_result['final_plan'])
        else:
            # Fallback if plan is empty
            st.warning("⚠️ Unable to generate personalized plan. Here's the summary:")
            st.write(f"**City:** {plan['city']}")
            st.write(f"**Budget:** ₹{plan['budget']}")
            st.write(f"**Date Type:** {plan['date_type']}")
            st.write(f"**Timing:** {plan['timing']}")
        
        st.divider()
        
        # Display weather information
        if final_result['weather_info']:
            st.header("🌤️ Weather Forecast")
            weather = final_result['weather_info']
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("🌡️ Temperature", f"{weather['temperature']}°C")
            with col2:
                st.metric("💨 Feels Like", f"{weather['feels_like']}°C")
            with col3:
                st.metric("☁️ Condition", weather['condition'])
            with col4:
                st.metric("🌧️ Rain Chance", f"{weather['rain_probability']}%")
            
            if weather['will_rain']:
                st.warning("⚠️ Rain expected - indoor venues recommended!")
            elif weather['suitable_for_outdoor']:
                st.success("✅ Perfect weather for outdoor activities!")
        
        st.divider()
        
        # Display detailed restaurant info
        if final_result['filtered_restaurants']:
            st.header("📋 Restaurant Recommendations")
            
            for i, restaurant in enumerate(final_result['filtered_restaurants'][:5], 1):
                with st.container():
                    st.markdown(f"""
                    <div class="restaurant-card">
                        <h3>{i}. {restaurant['name']}</h3>
                        <p><strong>⭐ Rating:</strong> {restaurant['rating']}/5 ({restaurant['total_ratings']} reviews)</p>
                        <p><strong>💵 Price:</strong> {restaurant['price_level']}</p>
                        <p><strong>📍 Address:</strong> {restaurant['address']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if restaurant.get('is_open') is not None:
                        if restaurant['is_open']:
                            st.success("🟢 Open now")
                        else:
                            st.error("🔴 Closed now")
                    
                    st.divider()
        
        # Success message
        st.balloons()
        st.success("✨ Your date plan is ready! Enjoy your date! ✨")

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem 0;">
    <p>Built with ❤️ using Multi-Agent AI Architecture</p>
    <p style="font-size: 0.9rem;">Powered by OpenAI, Google Places API (New), and OpenWeather API</p>
</div>
""", unsafe_allow_html=True)
