from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
from llm_service import LLMService
import os
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

llm_service = LLMService()

# Store conversation history per session
conversations = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    session_id = data.get('session_id', 'default')
    
    # Initialize conversation history if not exists
    if session_id not in conversations:
        conversations[session_id] = {
            'openai': [{"role": "system", "content": "You are a helpful assistant."}],
            'claude': [{"role": "system", "content": "You are a helpful assistant."}],
            'gemini': [{"role": "system", "content": "You are a helpful assistant."}]
        }
    
    # Add user message to all histories
    for model in ['openai', 'claude', 'gemini']:
        conversations[session_id][model].append({"role": "user", "content": user_message})
    
    # Call all LLMs in parallel
    with ThreadPoolExecutor(max_workers=3) as executor:
        openai_future = executor.submit(llm_service.call_openai, conversations[session_id]['openai'])
        claude_future = executor.submit(llm_service.call_claude, conversations[session_id]['claude'])
        gemini_future = executor.submit(llm_service.call_gemini, conversations[session_id]['gemini'])
        
        responses = {
            'openai': openai_future.result(),
            'claude': claude_future.result(),
            'gemini': gemini_future.result()
        }
    
    # Add responses to conversation history
    conversations[session_id]['openai'].append({"role": "assistant", "content": responses['openai']})
    conversations[session_id]['claude'].append({"role": "assistant", "content": responses['claude']})
    conversations[session_id]['gemini'].append({"role": "assistant", "content": responses['gemini']})
    
    return jsonify(responses)

@app.route('/continue', methods=['POST'])
def continue_chat():
    data = request.json
    user_message = data.get('message')
    selected_model = data.get('model')
    session_id = data.get('session_id', 'default')
    
    if session_id not in conversations:
        return jsonify({'error': 'Session not found'}), 400
    
    # Add user message to selected model's history
    conversations[session_id][selected_model].append({"role": "user", "content": user_message})
    
    # Call only the selected model
    if selected_model == 'openai':
        response = llm_service.call_openai(conversations[session_id][selected_model])
    elif selected_model == 'claude':
        response = llm_service.call_claude(conversations[session_id][selected_model])
    elif selected_model == 'gemini':
        response = llm_service.call_gemini(conversations[session_id][selected_model])
    
    # Add response to history
    conversations[session_id][selected_model].append({"role": "assistant", "content": response})
    
    return jsonify({'response': response, 'model': selected_model})

@app.route('/reset', methods=['POST'])
def reset():
    data = request.json
    session_id = data.get('session_id', 'default')
    if session_id in conversations:
        del conversations[session_id]
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
