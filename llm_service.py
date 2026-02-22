import os
from openai import OpenAI
import google.generativeai as genai

class LLMService:
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.openrouter_client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv('OPENROUTER_API_KEY')
        )
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        self.gemini_model = genai.GenerativeModel('gemini-2.5-flash')
    
    def call_openai(self, messages):
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
    
    def call_claude(self, messages):
        try:
            response = self.openrouter_client.chat.completions.create(
                model="anthropic/claude-3.5-haiku",
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
    
    def call_gemini(self, messages):
        try:
            # Convert messages to Gemini format
            prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages if m['role'] != 'system'])
            response = self.gemini_model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
