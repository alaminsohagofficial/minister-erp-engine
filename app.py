import os
import io
import sqlite3
from flask import Flask, request, jsonify, send_file, render_template_string
from weasyprint import HTML
from google import genai

app = Flask(__name__)

# Your Direct Gemini API Key
API_KEY = "AQ.Ab8RN6IuRuD6TNCENfAGU1riEjRbflzz5KIwyvnPT65zuffi2g"
ai = genai.Client(api_key=API_KEY)

# Database Setup
DB_NAME = "erp_ledger.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ledgers (
            dealer_id TEXT PRIMARY KEY,
            dealer_name TEXT,
            sap_allocation REAL,
            current_balance REAL,
            status TEXT
        )
    ''')
    cursor.execute('''
        INSERT OR IGNORE INTO ledgers VALUES 
        ('DEAL002905', 'Minister High-Tech Park', 35189545.00, 35189545.00, 'ACTIVE'),
        ('MDEL000215', 'Salsabila Electronics Park', 35189545.00, 35189545.00, 'ACTIVE')
    ''')
    conn.commit()
    conn.close()

init_db()

# Dashboard UI Route
@app.route('/')
def home():
    return render_template_string('''
    
    
    
        
        Minister ERP - Single Service Engine
