# Quick Setup Guide

## Prerequisites
- Python 3.10 or higher
- Git installed
- API keys from OpenAI, OpenRouter, and Google

## Installation Steps

### 1. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/multi-llm-chat.git
cd multi-llm-chat
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure API Keys
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_key_here
OPENROUTER_API_KEY=your_openrouter_key_here
GOOGLE_API_KEY=your_google_key_here
```

### 6. Get API Keys

**OpenAI:**
1. Go to https://platform.openai.com/api-keys
2. Create new API key
3. Add $5 minimum credits

**OpenRouter:**
1. Go to https://openrouter.ai/keys
2. Sign up and create API key
3. Add $5 credits

**Google Gemini:**
1. Go to https://makersuite.google.com/app/apikey
2. Create API key (Free tier available)

### 7. Run Application
```bash
python app.py
```

### 8. Open Browser
Navigate to: `http://127.0.0.1:5000`

## Usage

1. **Compare Mode:** Type a question and press Send to get responses from all three models
2. **Continue Mode:** Click "Continue with this" on any model to chat with only that model
3. **Reset:** Click "Reset Chat" to start fresh

## Troubleshooting

**Issue:** Module not found
- **Solution:** Make sure virtual environment is activated and dependencies installed

**Issue:** API key errors
- **Solution:** Verify API keys in `.env` file and ensure you have credits

**Issue:** Port already in use
- **Solution:** Change port in `app.py`: `app.run(debug=True, port=5001)`

## Features

✅ Compare 3 LLMs side-by-side
✅ Continue conversation with selected model
✅ Modern, responsive UI
✅ Mobile-friendly design
✅ Toast notifications
✅ Modal popups
✅ Conversation history per model

## Support

For issues or questions, please open an issue on GitHub.

## License

MIT License - Free to use for educational purposes.
