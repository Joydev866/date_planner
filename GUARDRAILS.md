# AI Date Planner - Guardrails & Validation

## 🛡️ Input Validation Guardrails

The AI Date Planner now includes comprehensive validation to ensure safe and reasonable recommendations:

### 1. **Date/Time Validation** ⏰
- **No Past Dates**: Automatically detects and rejects dates that have already passed
- **Smart Date Parsing**: Handles multiple formats:
  - "12th February", "Feb 14", "14/02/2026"
  - "today", "tomorrow", "this weekend"
- **Year Adjustment**: If a date appears to be in the past, checks if it should be next year
- **Example**: "Plan a date on January 5th" (when current date is Feb 10) → Adjusted to January 5, 2027

### 2. **Budget Constraints** 💰
- **Minimum**: ₹500 (prevents unrealistic low budgets)
- **Maximum**: ₹50,000 (prevents excessive budgets)
- **Auto-correction**: Invalid budgets are adjusted to nearest valid value
- **Example**: Budget of ₹100 → Adjusted to ₹500

### 3. **City Validation** 📍
- **Supported Cities**: 25+ major Indian cities including:
  - Mumbai, Delhi, Bangalore, Hyderabad, Chennai
  - Pune, Ahmedabad, Jaipur, Kolkata
  - Gurgaon, Noida, and more
- **Fallback**: Unsupported cities default to Bangalore
- **Example**: "Plan a date in XYZ City" → "City not supported. Using Bangalore instead."

### 4. **Date Type Validation** 💕
- **Valid Types**: romantic, casual, cozy, budget-friendly, formal, fun
- **Flexible**: Allows custom types but validates common ones
- **Default**: Falls back to "casual" if not specified

## 🔧 How It Works

```python
# Validation flow in both CLI and Streamlit
1. User submits request
2. Planner Agent extracts intent
3. Validator checks all parameters
4. Invalid inputs are corrected with warnings
5. Corrected plan proceeds to execution
```

## ⚠️ Validation Warnings

Users will see warnings when inputs are corrected:
- "⚠️ Date 'Jan 5' is in the past. Please choose a future date."
- "⚠️ Budget too low (minimum ₹500). Adjusted to ₹500."
- "⚠️ City 'Unknown' not supported. Using Bangalore instead."

## ✅ Benefits

1. **Prevents Errors**: Catches invalid inputs before API calls
2. **Saves Costs**: Avoids wasted API calls for invalid requests
3. **Better UX**: Clear feedback on what was corrected
4. **Safety**: Ensures all recommendations are realistic and achievable
