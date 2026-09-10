import os
import sqlite3
import logging
from flask import Flask, request, jsonify
import google.generativeai as genai

# Configure logging & Flask app
logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

# Configure Gemini API
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "your-gemini-api-key")
genai.configure(api_key=GEMINI_API_KEY)
ai_model = genai.GenerativeModel('gemini-2.5-flash')

# Initialize SQLite3 ACID Database
DB_NAME = "enterprise_erp.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id TEXT NOT NULL,
            amount REAL NOT NULL,
            type TEXT NOT NULL,
            description TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ai_audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id INTEGER,
            ai_analysis TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/api/transaction', methods=['POST'])
def process_transaction():
    data = request.json
    account_id = data.get('account_id')
    amount = data.get('amount')
    tx_type = data.get('type') # CREDIT / DEBIT
    description = data.get('description', '')

    # 1. ACID Database Insertion
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (account_id, amount, type, description)
        VALUES (?, ?, ?, ?)
    ''', (account_id, amount, tx_type, description))
    tx_id = cursor.lastrowid
    conn.commit()
    conn.close()

    # 2. Gemini AI Financial Validation & Anomaly Detection
    prompt = f"Analyze this enterprise transaction for anomalies or compliance check: Account: {account_id}, Amount: {amount}, Type: {tx_type}, Desc: {description}. Provide a concise JSON response with status ('APPROVED' or 'FLAGGED') and remarks."
    
    try:
        ai_response = ai_model.generate_content(prompt)
        analysis_text = ai_response.text
    except Exception as e:
        analysis_text = f"AI Error: {str(e)}"

    # 3. Log AI Audit Result
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO ai_audit_logs (transaction_id, ai_analysis)
        VALUES (?, ?)
    ''', (tx_id, analysis_text))
    conn.commit()
    conn.close()

    return jsonify({
        "status": "success",
        "transaction_id": tx_id,
        "ai_audit": analysis_text
    }), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
