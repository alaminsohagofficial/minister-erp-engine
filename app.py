import os
from flask import Flask, jsonify, request
import sqlite3
from banking_sync_engine import sync_transaction, DATABASE_NAME

app = Flask(__name__)

# Environment থেকে Gemini API Key নিরাপদে লোড করা
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "default-placeholder-key")

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "system": "Minister ERP Engine",
        "message": "Banking Synchronization & Gemini AI Engine is running.",
        "ai_status": "API Key Configured" if GEMINI_API_KEY != "default-placeholder-key" else "Warning: Default Key Active"
    })

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    """ডাটাবেজ থেকে সমস্ত সিঙ্ক হওয়া ট্রানজেকশন দেখার এপিআই"""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    
    transactions = [dict(row) for row in rows]
    return jsonify({
        "success": True,
        "total_count": len(transactions),
        "data": transactions
    })

@app.route('/api/sync', methods=['POST'])
def api_sync_transaction():
    """নতুন ট্রানজেকশন রিসিভ করে সিঙ্ক করার এপিআই এন্ডপয়েন্ট"""
    incoming_data = request.get_json()
    if not incoming_data or 'lid' not in incoming_data:
        return jsonify({"success": False, "error": "Invalid data or missing LID"}), 400
        
    success = sync_transaction(incoming_data)
    if success:
        return jsonify({"success": True, "message": "Transaction synchronized successfully."}), 201
    else:
        return jsonify({"success": False, "message": "Duplicate LID or database error."}), 409

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
