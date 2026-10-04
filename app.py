import os
import io
import sqlite3
from flask import Flask, request, jsonify, send_file, render_template_string
from weasyprint import HTML
from google import genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Secure Gemini API Key from Environment Variables
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is missing!")

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
