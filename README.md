# 💘 AI Date Planner Assistant

A multi-agent GenAI system that plans complete dates using live APIs (Google Places & OpenWeather). Perfect for demonstrating real-world AI capabilities with practical applications.

## 🎯 What It Does

The AI Date Planner takes natural language requests and generates personalized date plans with:
- **Restaurant recommendations** based on location, budget, and preferences
- **Weather forecasts** to ensure optimal timing
- **Budget-conscious suggestions** within your price range
- **Contextual planning** (romantic, casual, cozy, etc.)

### Example Usage

**Input:**
```
"Plan a romantic dinner date in Mumbai under ₹2500"
```

**Output:**
- Top 3-5 restaurant recommendations with ratings and addresses
- Weather forecast for the evening
- Budget validation
- Suggested timing
- Complete date plan summary

## 🧠 Multi-Agent Architecture

The system uses three specialized AI agents working in sequence:

### 1️⃣ **Planner Agent**
- Understands user intent using OpenAI GPT
- Extracts structured data: city, budget, date type, timing
- Outputs JSON with parameters for execution

### 2️⃣ **Executor Agent**
- Orchestrates API calls based on planner output
- Fetches real-time data from:
  - **Google Places API** (restaurants, ratings, prices)
  - **OpenWeather API** (weather forecasts)
- Collects and formats results

### 3️⃣ **Verifier Agent**
- Validates recommendations against constraints
- Filters inappropriate suggestions (e.g., outdoor venues during rain)
- Uses AI to generate coherent, personalized date plans
- Ensures budget compliance and weather suitability

## 🛠 Tech Stack

- **Python 3.8+**
- **OpenAI API** (GPT-4o-mini for cost-effectiveness)
- **Google Places API** (restaurant search and details)
- **OpenWeather API** (weather forecasts)
- **Libraries:** `openai`, `requests`, `python-dotenv`

## 📁 Project Structure

```
genai-date-planner/
│
├── agents/
│   ├── __init__.py
│   ├── planner.py          # Intent extraction with OpenAI
│   ├── executor.py         # API orchestration
│   └── verifier.py         # Validation and plan generation
│
├── tools/
│   ├── __init__.py
│   ├── places_api.py       # Google Places integration
│   └── weather_api.py      # OpenWeather integration
│
├── main.py                 # Main orchestration logic
├── requirements.txt        # Python dependencies
├── .env                    # API keys (DO NOT COMMIT)
├── .env.example            # Template for environment variables
└── README.md               # This file
```

## 🚀 Setup Instructions

### 1. Clone or Download the Project

```bash
cd /path/to/date_planner
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys

You need three API keys. Copy `.env.example` to `.env` and add your keys:

```bash
cp .env.example .env
```

#### Get Your API Keys:

**OpenAI API:**
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create an account or sign in
3. Generate a new API key
4. Add to `.env`: `OPENAI_API_KEY=sk-...`

**Google Places API (New):**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable "Places API (New)" 
4. Create credentials (API Key)
5. Add to `.env`: `GOOGLE_PLACES_API=AIza...`

> **Note:** Make sure to enable "Places API (New)" not the legacy "Places API"

**OpenWeather API:**
1. Visit [OpenWeather](https://openweathermap.org/api)
2. Sign up for free account
3. Get your API key from dashboard
4. Add to `.env`: `OPEN_WEATHER_API=...`

### 4. Run the Application

**Option 1: Command Line Interface (CLI)**
```bash
python3 main.py
```

**Option 2: Web Interface (Streamlit)**
```bash
streamlit run app.py
```

The web interface will open automatically in your browser at `http://localhost:8501`

> **Recommended:** Use the Streamlit web interface for a better visual experience with interactive components and real-time updates!

## 💡 Example Prompts

Try these prompts to test the system:

1. **"Plan a romantic dinner date in Mumbai under ₹2500"**
   - Tests budget constraints and romantic venue filtering

2. **"Suggest a cozy café date in Delhi this weekend"**
   - Tests timing parsing and café-specific search

3. **"Plan an indoor date in Bangalore if it rains"**
   - Tests weather integration and indoor filtering

4. **"Find a budget-friendly first date in Pune"**
   - Tests budget optimization and casual venue search

## 🔗 Required Third-Party APIs (Easy & Stable)

**1️⃣ Google Places API (New)**

Used for:
- Restaurant search using searchText endpoint
- Ratings and reviews
- Price level information
- Current opening hours

**2️⃣ OpenWeather API**

Used for:
- Weather forecast
- Rain / temperature check

Both are:
- Free tier available
- Easy to integrate
- Reliable

## 🧪 Example Prompts (README ready)

```
User Input
    ↓
┌─────────────────┐
│ Planner Agent   │ → Extracts: city, budget, date_type, timing
└─────────────────┘
    ↓
┌─────────────────┐
│ Executor Agent  │ → Calls: Google Places API + OpenWeather API
└─────────────────┘
    ↓
┌─────────────────┐
│ Verifier Agent  │ → Validates, filters, generates final plan
└─────────────────┘
    ↓
Final Date Plan
```

## ✅ Features Checklist

- ✅ **Multi-agent architecture** (Planner, Executor, Verifier)
- ✅ **Tool calling** (Google Places API, OpenWeather API)
- ✅ **Real-time data** (live restaurant and weather info)
- ✅ **Natural language processing** (OpenAI GPT)
- ✅ **Budget validation** (filters by price level)
- ✅ **Weather-aware planning** (indoor/outdoor recommendations)
- ✅ **Structured outputs** (JSON for agent communication)
- ✅ **Error handling** (graceful degradation)
- ✅ **User-friendly interface** (clear console output)

## 🎓 Why This Project?

This project demonstrates:

1. **Multi-agent systems** - Clear separation of concerns
2. **API integration** - Real-world data from multiple sources
3. **Practical AI application** - Solves a real problem
4. **Domain relevance** - Perfect for dating/social apps
5. **Production-ready patterns** - Error handling, validation, modularity

## 🔒 Security Notes

- **Never commit `.env`** - Add to `.gitignore`
- **Use environment variables** - Keep API keys secure
- **Rotate keys regularly** - Especially for production use
- **Monitor API usage** - Set up billing alerts

## 🐛 Troubleshooting

**"Error initializing agents"**
- Check that all API keys are set in `.env`
- Verify API keys are valid and active

**"No restaurants found"**
- Try a different city or increase budget
- Check Google Places API quota

**"Weather data unavailable"**
- Verify OpenWeather API key
- Check city name spelling

**Import errors**
- Run `pip install -r requirements.txt`
- Ensure Python 3.8+ is installed

## 📝 License

This project is open source and available for educational purposes.

## 🙏 Acknowledgments

- OpenAI for GPT models
- Google for Places API
- OpenWeather for weather data

---

**Built with ❤️ for demonstrating multi-agent GenAI systems**
