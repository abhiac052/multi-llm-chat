# Firebase Setup Guide

## Step 1: Create Firebase Project

1. Go to https://console.firebase.google.com/
2. Click "Add project"
3. Enter project name: `multi-llm-chat`
4. Disable Google Analytics (optional)
5. Click "Create project"

## Step 2: Enable Firestore Database

1. In Firebase Console, click "Firestore Database"
2. Click "Create database"
3. Select "Start in test mode" (for development)
4. Choose location (closest to you)
5. Click "Enable"

## Step 3: Generate Service Account Key

1. Go to Project Settings (gear icon) → Service accounts
2. Click "Generate new private key"
3. Click "Generate key" (downloads JSON file)
4. Save the file as `firebase-key.json` in your project root

## Step 4: Update .env File

Add this line to your `.env` file:
```
FIREBASE_CREDENTIALS_PATH=firebase-key.json
```

## Step 5: Update .gitignore

Add to `.gitignore`:
```
firebase-key.json
```

## Step 6: Install Firebase SDK

```bash
pip install firebase-admin
```

## Step 7: Update app.py

Replace this line:
```python
from database import Database
db = Database()
```

With:
```python
from firebase_database import FirebaseDatabase
db = FirebaseDatabase()
```

## Step 8: Run the App

```bash
python app.py
```

## View Data in Firebase Console

1. Go to https://console.firebase.google.com/
2. Select your project
3. Click "Firestore Database"
4. Browse collections: `sessions` and `conversations`
5. View data in real-time!

## Firestore Collections Structure

### sessions
- session_id (string)
- created_at (timestamp)
- last_activity (timestamp)

### conversations
- session_id (string)
- model (string)
- role (string)
- content (string)
- timestamp (timestamp)

## Benefits of Firebase

✅ Cloud-based (accessible anywhere)
✅ Real-time updates
✅ Beautiful web console
✅ Free tier (50K reads/day, 20K writes/day)
✅ Automatic backups
✅ No server management needed
