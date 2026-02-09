#  AI Date Planner Assistant

An intelligent multi-agent system that helps you plan the perfect date using AI-powered insights, real-time weather data, and restaurant recommendations.

##  Features

- **Multi-Agent AI Architecture**: Coordinated system with Planner, Executor, and Verifier agents
- **Smart Intent Extraction**: Natural language understanding to extract date preferences
- **Real-time Restaurant Recommendations**: Powered by Google Places API (New v1)
- **Weather-Aware Planning**: Integrates OpenWeather API for weather-based suggestions
- **Budget-Conscious**: Filters recommendations based on your budget
- **Input Validation**: Built-in guardrails to ensure safe and valid inputs
- **Dual Interface**: CLI and beautiful Streamlit web interface

---

##  Quick Start

### Prerequisites

- Python 3.8 or higher
- API Keys for:
  - OpenAI (via OpenRouter)
  - Google Places API (New)
  - OpenWeather API

### Installation

1. **Clone the repository**
   ```bash
   cd /Users/jaybehera/Desktop/date_planner
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root with the following:
   ```env
   OPENAI_API_KEY=your_openrouter_api_key_here
   GOOGLE_PLACES_API=your_google_places_api_key_here
   OPEN_WEATHER_API=your_openweather_api_key_here
   ```

   See [`.env.example`](#environment-variables) below for details.

### Running the Project

**Option 1: Streamlit Web Interface (Recommended)**
```bash
streamlit run app.py
```
Then open your browser to `http://localhost:8501`

**Option 2: Command Line Interface**
```bash
python main.py
```

---

##  Environment Variables

Create a `.env` file with these required variables:

```env
# OpenAI API Key (via OpenRouter for cost-effective access)
# Get yours at: https://openrouter.ai/keys
OPENAI_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxx

# Google Places API Key (New API v1)
# Get yours at: https://console.cloud.google.com/apis/credentials
# Enable: Places API (New)
GOOGLE_PLACES_API=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# OpenWeather API Key
# Get yours at: https://openweathermap.org/api
OPEN_WEATHER_API=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Getting API Keys

1. **OpenRouter (OpenAI)**: Sign up at [openrouter.ai](https://openrouter.ai) and create an API key
2. **Google Places API**: 
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Enable "Places API (New)" 
   - Create credentials (API Key)
3. **OpenWeather**: Sign up at [openweathermap.org](https://openweathermap.org/api) and get a free API key

---

##  Architecture

The system uses a **multi-agent architecture** with three specialized agents:

```
User Input → Planner Agent → Executor Agent → Verifier Agent → Final Plan
```

### Agent Breakdown

#### 1. **Planner Agent** (`agents/planner.py`)
- **Role**: Intent extraction and understanding
- **Technology**: OpenAI GPT (via OpenRouter)
- **Responsibilities**:
  - Parses natural language date requests
  - Extracts structured data (city, budget, date type, timing)
  - Determines what data needs to be fetched
- **Output**: Structured plan dictionary

#### 2. **Executor Agent** (`agents/executor.py`)
- **Role**: Data collection and API orchestration
- **Technology**: Coordinates external API calls
- **Responsibilities**:
  - Calls Google Places API for restaurant recommendations
  - Fetches weather data from OpenWeather API
  - Handles API errors gracefully
- **Output**: Raw data from external services

#### 3. **Verifier Agent** (`agents/verifier.py`)
- **Role**: Validation and plan generation
- **Technology**: OpenAI GPT for natural language generation
- **Responsibilities**:
  - Validates data quality and completeness
  - Filters restaurants by budget and rating
  - Generates personalized date plan narrative
  - Provides weather-aware recommendations
- **Output**: Final formatted date plan

### Tools

#### **Google Places API Tool** (`tools/places_api.py`)
- Uses the **new Google Places API v1** with `searchText` endpoint
- Features:
  - Text-based search for restaurants
  - Price level filtering
  - Location-based search with 5km radius
  - Supports 20+ major Indian cities
  - Returns top 5 rated restaurants

#### **Weather API Tool** (`tools/weather_api.py`)
- Integrates OpenWeather API
- Features:
  - Current weather conditions
  - 5-day forecast
  - Rain probability calculation
  - Indoor/outdoor suitability assessment

### Input Validation (`validators.py`)
- **Guardrails** to ensure safe inputs:
  - Budget limits (₹100 - ₹50,000)
  - Supported cities validation
  - Date and Time validation 
---

##  Integrated APIs

| API | Purpose | Version | Documentation |
|-----|---------|---------|---------------|
| **OpenAI** (via OpenRouter) | Natural language processing, intent extraction, plan generation | stepfun/step-3.5-flash:free| [openrouter.ai](https://openrouter.ai) |
| **Google Places API** | Restaurant search and recommendations | **New API v1** (`searchText`) | [developers.google.com/maps/documentation/places/web-service/search-text](https://developers.google.com/maps/documentation/places/web-service/search-text) |
| **OpenWeather API** | Weather forecasts and current conditions | 2.5 | [openweathermap.org/api](https://openweathermap.org/api) |

---

##  Example Prompts

Try these prompts to test the system:

1. **Budget-Conscious Romantic Date**
   ```
   Plan a romantic dinner date in Mumbai under ₹2500
   ```

2. **Casual Weekend Date**
   ```
   Suggest a cozy café date in Delhi this weekend
   ```

3. **Weather-Aware Planning**
   ```
   Plan an indoor date in Bangalore if it rains
   ```

4. **First Date on a Budget**
   ```
   Find a budget-friendly first date in Pune under ₹1500
   ```

5. **Specific Date Type**
   ```
   Recommend a casual lunch date in Hyderabad tomorrow with outdoor seating
   ```

---

## 📁 Project Structure

```
date_planner/
├── agents/
│   ├── __init__.py
│   ├── planner.py          # Intent extraction agent
│   ├── executor.py         # API orchestration agent
│   └── verifier.py         # Validation and plan generation agent
├── tools/
│   ├── __init__.py
│   ├── places_api.py       # Google Places API integration
│   └── weather_api.py      # OpenWeather API integration
├── validators.py           # Input validation and guardrails
├── main.py                 # CLI entry point
├── app.py                  # Streamlit web interface
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── GUARDRAILS.md          # Security and validation documentation
└── README.md              # This file
```

---

##  Known Limitations & Tradeoffs

### Limitations

1. **Geographic Coverage**
   - Currently optimized for **20+ major Indian cities**
   - Coordinates are approximate city centers

2. **Weather Forecast Accuracy**
   - Free tier OpenWeather API provides 5-day forecasts
   - "This weekend" timing uses approximate dates
   - Weather predictions become less accurate beyond 3 days

3. **API Rate Limits**
   - OpenRouter: Depends on your plan
   - Google Places API: 1000 requests/month (free tier)
   - OpenWeather API: 1000 requests/day (free tier)

4. **Price Level Accuracy**
   - Google Places price levels are approximate
   - Budget filtering may not be 100% accurate
   - Some restaurants don't have price data

5. **Real-time Data**
   - Restaurant opening hours may be outdated
   - No real-time table availability
   - No reservation integration

### Tradeoffs

| Decision | Benefit | Tradeoff |
|----------|---------|----------|
| **OpenRouter instead of direct OpenAI** | Cost-effective, multiple model options | Extra API layer, slight latency |
| **New Google Places API v1** | Better search quality, modern API | Limited documentation, fewer examples |
| **Multi-agent architecture** | Modular, testable, clear separation of concerns | More complex than monolithic approach |
| **Free-tier APIs** | No cost to run | Rate limits, reduced features |
| **Hardcoded city coordinates** | Fast, no geocoding API needed | Limited to predefined cities |
| **Top 5 restaurant limit** | Focused recommendations, faster responses | May miss some good options |

### Future Improvements

- [ ] Add geocoding API for any city worldwide
- [ ] Integrate reservation systems (OpenTable, Zomato)
- [ ] Add more date activity types (movies, museums, parks)
- [ ] Implement user feedback loop for better recommendations
- [ ] Add cost estimation for complete date plan
- [ ] Support multiple languages
- [ ] Add date itinerary with timing suggestions

---

##  Security & Validation

The system includes comprehensive input validation (see [`GUARDRAILS.md`](GUARDRAILS.md)):

- Budget range validation (₹100 - ₹50,000)
- City whitelist (20+ supported cities)
- SQL injection prevention
- XSS attack prevention
- API key protection (never logged or exposed)

---

##  Testing

**Manual Testing:**
```bash
# Test CLI
python main.py

# Test Web Interface
streamlit run app.py
```

