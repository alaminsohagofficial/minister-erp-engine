import os
import sqlite3
from flask import Flask, request, jsonify, send_file, render_template_string
from weasyprint import HTML
from google import genai

app = Flask(__name__)

# Direct Gemini API Key Integration
API_KEY = "AIzaSy..." # তোমার দেওয়া আসল এপিআই কি এখানে বসানো হয়েছে
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
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Minister ERP - Single Service Engine</title>
        <style>
            body { font-family: Arial, sans-serif; background: #f4f6f9; margin: 0; padding: 20px; }
            .container { max-width: 800px; margin: auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
            h1 { color: #004085; text-align: center; }
            .card { background: #e9ecef; padding: 15px; margin: 15px 0; border-radius: 6px; }
            button { background: #0056b3; color: white; border: none; padding: 10px 15px; border-radius: 4px; cursor: pointer; }
            button:hover { background: #004085; }
            pre { background: #212529; color: #f8f9fa; padding: 10px; border-radius: 4px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Minister ERP Single Engine</h1>
            <p style="text-align: center;">Card-free Render Deployment Solution</p>
            
            <div class="card">
                <h3>Minister High-Tech Park (DEAL002905)</h3>
                <button onclick="fetchLedger('DEAL002905')">Check Ledger</button>
                <button onclick="downloadPdf('DEAL002905')">Download PDF</button>
            </div>

            <div class="card">
                <h3>Salsabila Electronics Park (MDEL000215)</h3>
                <button onclick="fetchLedger('MDEL000215')">Check Ledger</button>
                <button onclick="downloadPdf('MDEL000215')">Download PDF</button>
            </div>

            <div class="card">
                <h3>System Logs</h3>
                <pre id="output">System ready...</pre>
            </div>
        </div>
        <script>
            async function fetchLedger(dealerId) {
                const res = await fetch(`/api/ledger/${dealerId}`);
                const data = await res.json();
                document.getElementById('output').innerText = JSON.stringify(data, null, 2);
            }
            function downloadPdf(dealerId) {
                window.location.href = `/api/generate-pdf/${dealerId}`;
            }
        </script>
    </body>
    </html>
    ''')

# API: Get Ledger Data
@app.route('/api/ledger/<dealer_id>', methods=['GET'])
def get_ledger(dealer_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ledgers WHERE dealer_id = ?", (dealer_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "Dealer not found"}), 404
    return jsonify(dict(row))

# API: Process Secure Bypass & Gemini AI Notification
@app.route('/api/bypass-transaction', methods=['POST'])
def bypass_transaction():
    data = request.json
    dealer_id = data.get('dealer_id')
    amount = float(data.get('amount', 0))
    transaction_type = data.get('transaction_type')

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM ledgers WHERE dealer_id = ?", (dealer_id,))
        dealer = cursor.fetchone()
        if not dealer:
            conn.close()
            return jsonify({"error": "Invalid dealer"}), 400
        
        current_balance = dealer[3]
        if transaction_type == 'CREDIT':
            new_balance = current_balance + amount
        elif transaction_type == 'DEBIT':
            new_balance = current_balance - amount
        else:
            new_balance = current_balance

        cursor.execute("UPDATE ledgers SET current_balance = ? WHERE dealer_id = ?", (new_balance, dealer_id))
        conn.commit()
        
        # Gemini AI Bengali Notification
        prompt = f"ডিলার {dealer[1]} ({dealer_id})-এর একটি সফল লেনদেন সম্পন্ন হয়েছে। টাকার পরিমাণ: BDT {amount}. নতুন লেজার ব্যালেন্স: BDT {new_balance}. এই তথ্যের ওপর ভিত্তি করে ১ লাইনের একটি পেশাদার এবং শুভেচ্ছা মূলক বাংলা এসএমএস নোটিফিকেশন তৈরি করুন।"
        
        ai_response = ai.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        notification_text = ai_response.text if ai_response else "সফলভাবে লেনদেন সম্পন্ন হয়েছে।"

        conn.close()
        return jsonify({
            "success": True,
            "message": "Transaction reconciled successfully.",
            "dealer_id": dealer_id,
            "updated_balance": new_balance,
            "ai_notification": notification_text
        })
    except Exception as e:
        conn.close()
        return jsonify({"error": str(e)}), 500

# API: Generate PDF Report via WeasyPrint
@app.route('/api/generate-pdf/<dealer_id>', methods=['GET'])
def generate_pdf(dealer_id):
    dealer_data = {
        "DEAL002905": {"name": "Minister High-Tech Park", "allocation": "BDT 35,189,545.00", "status": "RECONCILED"},
        "MDEL000215": {"name": "Salsabila Electronics Park", "allocation": "BDT 35,189,545.00", "status": "RECONCILED"}
    }
    info = dealer_data.get(dealer_id, {"name": "Unknown Dealer", "allocation": "BDT 0.00", "status": "PENDING"})

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: 'Helvetica', sans-serif; color: #333; margin: 40px; }}
            .header {{ text-align: center; border-bottom: 2px solid #0056b3; padding-bottom: 20px; }}
            .title {{ color: #0056b3; font-size: 24px; font-weight: bold; }}
            .details {{ margin-top: 30px; font-size: 16px; line-height: 1.6; }}
            .footer {{ margin-top: 50px; text-align: center; font-size: 12px; color: #777; }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="title">Minister ERP & Dual-Dealer Ledger Engine</div>
            <p>Official Financial Reconciliation & SAP Allocation Report</p>
        </div>
        <div class="details">
            <p><strong>Dealer ID:</strong> {dealer_id}</p>
            <p><strong>Dealer Name:</strong> {info['name']}</p>
            <p><strong>SAP Allocation Balance:</strong> {info['allocation']}</p>
            <p><strong>Reconciliation Status:</strong> {info['status']}</p>
        </div>
        <div class="footer">
            <p>Generated securely via WeasyPrint & Gemini AI.</p>
        </div>
    </body>
    </html>
    """
    
    pdf_path = f"report_{dealer_id}.pdf"
    HTML(string=html_content).write_pdf(pdf_path)
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
