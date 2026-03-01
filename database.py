import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os

class Database:
    def __init__(self):
        # Initialize Firebase (only once)
        if not firebase_admin._apps:
            # Use service account key file
            cred = credentials.Certificate(os.getenv('FIREBASE_CREDENTIALS_PATH', 'firebase-key.json'))
            firebase_admin.initialize_app(cred)
        
        self.db = firestore.client()
    
    def save_message(self, session_id, model, role, content):
        """Save a message to Firestore"""
        # Update session
        session_ref = self.db.collection('sessions').document(session_id)
        session_data = session_ref.get()
        
        if session_data.exists:
            session_ref.update({
                'last_activity': firestore.SERVER_TIMESTAMP
            })
        else:
            session_ref.set({
                'session_id': session_id,
                'created_at': firestore.SERVER_TIMESTAMP,
                'last_activity': firestore.SERVER_TIMESTAMP
            })
        
        # Save message
        self.db.collection('conversations').add({
            'session_id': session_id,
            'model': model,
            'role': role,
            'content': content,
            'timestamp': firestore.SERVER_TIMESTAMP
        })
    
    def get_conversation(self, session_id, model=None):
        """Retrieve conversation history"""
        query = self.db.collection('conversations').where('session_id', '==', session_id)
        
        if model:
            query = query.where('model', '==', model)
        
        query = query.order_by('timestamp')
        
        messages = []
        for doc in query.stream():
            data = doc.to_dict()
            if model:
                messages.append((data['role'], data['content']))
            else:
                messages.append((data['model'], data['role'], data['content']))
        
        return messages
    
    def clear_session(self, session_id):
        """Clear all messages for a session"""
        # Delete all conversations
        conversations = self.db.collection('conversations').where('session_id', '==', session_id).stream()
        for doc in conversations:
            doc.reference.delete()
        
        # Delete session
        self.db.collection('sessions').document(session_id).delete()
    
    def get_all_sessions(self):
        """Get all session IDs"""
        sessions = []
        docs = self.db.collection('sessions').order_by('last_activity', direction=firestore.Query.DESCENDING).stream()
        
        for doc in docs:
            data = doc.to_dict()
            sessions.append((
                data['session_id'],
                data.get('created_at'),
                data.get('last_activity')
            ))
        
        return sessions
