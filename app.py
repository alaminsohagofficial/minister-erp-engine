import os
from flask import Flask, render_template, request, jsonify
from dotenv import load

load()

app = Flask(__name__)

@app.route('/')
def home():
    return "Minister ERP Real-Time Sync & AI Notification Engine is running..."

@app.route('/api/sync', methods=['POST'])
def sync_ledger():
    data = request.json
    # Process SQLite ACID transaction & Gemini AI notification here
    return jsonify({"success": True, "message": "Synced successfully with Minister ERP"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
