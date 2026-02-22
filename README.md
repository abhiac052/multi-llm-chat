# Multi-LLM Chat Comparison

A web application that allows users to compare responses from multiple Large Language Models (OpenAI GPT, Claude, and Gemini) side-by-side, with the ability to continue conversations with a selected model.

## Features

- **Parallel Querying**: Send questions to OpenAI, Claude, and Gemini simultaneously
- **Side-by-Side Comparison**: View all model responses in a three-column layout
- **Model Selection**: Click "Continue with this" to keep chatting with your preferred model
- **Conversation History**: Each model maintains its own chat context
- **Clean UI**: Simple, responsive interface

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **LLM APIs**: OpenAI, Anthropic (Claude), Google (Gemini)

## Setup Instructions

### 1. Prerequisites

- Python 3.10 or higher
- API keys for:
  - OpenAI (https://platform.openai.com/api-keys)
  - Anthropic (https://console.anthropic.com/)
  - Google AI (https://makersuite.google.com/app/apikey)

### 2. Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

### 4. Run the Application

```bash
python app.py
```

Open your browser and navigate to: `http://127.0.0.1:5000`

## Usage

1. **Compare Mode**: Type a question and press Send. All three models will respond simultaneously.
2. **Continue Mode**: Click "Continue with this" on any model to switch to single-model conversation.
3. **Reset**: Click "Reset Chat" to start a new conversation.

## Project Structure

```
multi-llm-chat/
├── app.py              # Flask backend with API routes
├── llm_service.py      # LLM API integration
├── requirements.txt    # Python dependencies
├── .env               # API keys (create this)
├── .env.example       # Template for API keys
├── .gitignore         # Git ignore rules
├── README.md          # This file
├── static/
│   ├── style.css      # UI styling
│   └── script.js      # Frontend logic
└── templates/
    └── index.html     # Main HTML page
```

## How It Works

1. **User sends a message** → Frontend sends POST request to `/chat`
2. **Backend calls all 3 LLMs in parallel** using ThreadPoolExecutor
3. **Responses displayed side-by-side** in three columns
4. **User selects a model** → Frontend switches to `/continue` endpoint
5. **Conversation continues** with only the selected model

## API Endpoints

- `GET /` - Serve the main page
- `POST /chat` - Send message to all models (compare mode)
- `POST /continue` - Send message to selected model (continue mode)
- `POST /reset` - Clear conversation history

## Notes

- Each model uses its own conversation history
- System prompts can be customized in `app.py`
- API costs apply based on usage
- Keep your `.env` file secure and never commit it

## Troubleshooting

**Issue**: API key errors
- **Solution**: Verify your API keys in `.env` file

**Issue**: Module not found
- **Solution**: Ensure virtual environment is activated and dependencies installed

**Issue**: Port already in use
- **Solution**: Change port in `app.py`: `app.run(debug=True, port=5001)`

## Future Enhancements

- Add more LLM providers (Llama, Mistral, etc.)
- Export conversation history
- Customize system prompts via UI
- Add streaming responses
- Deploy to cloud platform

## License

MIT License - Feel free to use for educational purposes.
