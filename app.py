from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
from llm_service import LLMService
from database import Database
import os
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

llm_service = LLMService()
db = Database()

# Remove in-memory storage - now using database
# conversations = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    session_id = data.get('session_id', 'default')
    
    # Load conversation history from database
    conversations = {}
    for model in ['openai', 'claude', 'gemini']:
        messages = db.get_conversation(session_id, model)
        if messages:
            conversations[model] = [{"role": role, "content": content} for role, content in messages]
        else:
            conversations[model] = [{"role": "system", "content": "You are a helpful assistant."}]
    
    # Add user message to all histories and save to DB
    for model in ['openai', 'claude', 'gemini']:
        conversations[model].append({"role": "user", "content": user_message})
        db.save_message(session_id, model, "user", user_message)
    
    # Call all LLMs in parallel
    with ThreadPoolExecutor(max_workers=3) as executor:
        openai_future = executor.submit(llm_service.call_openai, conversations['openai'])
        claude_future = executor.submit(llm_service.call_claude, conversations['claude'])
        gemini_future = executor.submit(llm_service.call_gemini, conversations['gemini'])
        
        responses = {
            'openai': openai_future.result(),
            'claude': claude_future.result(),
            'gemini': gemini_future.result()
        }
    
    # Save responses to database
    for model in ['openai', 'claude', 'gemini']:
        db.save_message(session_id, model, "assistant", responses[model])
    
    return jsonify(responses)

@app.route('/continue', methods=['POST'])
def continue_chat():
    data = request.json
    user_message = data.get('message')
    selected_model = data.get('model')
    session_id = data.get('session_id', 'default')
    
    # Load conversation history from database
    messages = db.get_conversation(session_id, selected_model)
    if messages:
        conversation = [{"role": role, "content": content} for role, content in messages]
    else:
        conversation = [{"role": "system", "content": "You are a helpful assistant."}]
    
    # Add user message and save to DB
    conversation.append({"role": "user", "content": user_message})
    db.save_message(session_id, selected_model, "user", user_message)
    
    # Call only the selected model
    if selected_model == 'openai':
        response = llm_service.call_openai(conversation)
    elif selected_model == 'claude':
        response = llm_service.call_claude(conversation)
    elif selected_model == 'gemini':
        response = llm_service.call_gemini(conversation)
    
    # Save response to database
    db.save_message(session_id, selected_model, "assistant", response)
    
    return jsonify({'response': response, 'model': selected_model})

@app.route('/reset', methods=['POST'])
def reset():
    data = request.json
    session_id = data.get('session_id', 'default')
    db.clear_session(session_id)
    return jsonify({'status': 'success'})

@app.route('/history', methods=['GET'])
def get_history():
    """Get all saved sessions"""
    sessions = db.get_all_sessions()
    return jsonify({'sessions': [{'session_id': s[0], 'created_at': s[1], 'last_activity': s[2]} for s in sessions]})

if __name__ == '__main__':
    app.run(debug=True)
