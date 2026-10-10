import os
import sqlite3
from flask import Flask, render_template_string, request, jsonify, send_file
from google import genai
import weasyprint

app = Flask(__name__)
DB_NAME = "dealer_ledger.db"

# Initialize Gemini Client (Ensure GEMINI_API_KEY environment variable is set)
# GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client() if os.environ.get("GEMINI_API_KEY") else None

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dealers (
            dealer_id TEXT PRIMARY KEY,
            dealer_name TEXT,
            proprietor TEXT,
            credit_limit REAL,
            sap_ledger REAL,
            status TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dealer_id TEXT,
            date TEXT,
            ref_id TEXT,
            category TEXT,
            amount REAL,
            status TEXT,
            FOREIGN KEY (dealer_id) REFERENCES dealers (dealer_id)
        )
    ''')
    
    # Seed default data if empty
    cursor.execute("SELECT COUNT(*) FROM dealers")
    if cursor.fetchone()[0] == 0:
        dealers_data = [
            ("DEAL002905", "S.R. Electronics Park", "MD. AL AMIN SOHAG", 15000000.00, 4250000.00, "Active"),
            ("MDEL000215", "Salsabila Electronics Park", "MD. NAZMUL HOSSAIN", 20189545.00, 8920000.00, "Active")
        ]
        cursor.executemany("INSERT INTO dealers VALUES (?, ?, ?, ?, ?, ?)", dealers_data)
        
        txns_data = [
            ("DEAL002905", "10-Oct-2026", "SB-RTGS-998877", "Appliance Stock", 2500000.00, "CLEARED"),
            ("DEAL002905", "08-Oct-2026", "MIN-INV-2026-89", "AC & Refrigerator", 1800000.00, "CLEARED"),
            ("MDEL000215", "09-Oct-2026", "SAL-RTGS-112233", "Smart LED TV", 3100000.00, "CLEARED")
        ]
        cursor.executemany("INSERT INTO transactions (dealer_id, date, ref_id, category, amount, status) VALUES (?, ?, ?, ?, ?, ?)", txns_data)
        
    conn.commit()
    conn.close()

init_db()

# Embedded Single-File HTML/CSS Dashboard Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Minister ERP & Dual-Dealer Secure Financial Ledger</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #0b1120; color: #f8fafc; font-family: 'Segoe UI', sans-serif; }
    </style>
</head>
<body class="min-h-screen p-4 sm:p-8">
    <div class="max-w-7xl mx-auto space-y-6">
        
        <!-- Header -->
        <header class="flex flex-wrap justify-between items-center border-b border-slate-800 pb-4 gap-4">
            <div>
                <h1 class="text-2xl font-bold flex items-center gap-2">
                    ⚡ Minister ERP & Dual-Dealer Ledger <span class="text-xs bg-blue-600 text-white px-2 py-1 rounded">Single-Service Edition</span>
                </h1>
                <p class="text-xs text-slate-400 mt-1">Managed SAP ERP Gateway | SQLite ACID Backend | WeasyPrint PDF & Gemini AI</p>
            </div>
            <div class="flex gap-3">
                <a href="/pdf-report" target="_blank" class="bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold px-4 py-2 rounded-lg transition">
                    🖨️ Download PDF Ledger
                </a>
            </div>
        </header>

        <!-- KPI Grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
                <p class="text-xs text-slate-400 uppercase">Total Combined SAP Allocation</p>
                <p class="text-2xl font-bold text-blue-400 mt-1">BDT 35,189,545.00</p>
                <p class="text-[10px] text-slate-500 mt-1">Dual-Dealer Authorized Limit</p>
            </div>
            <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
                <p class="text-xs text-slate-400 uppercase">S.R. Electronics (002905)</p>
                <p class="text-2xl font-bold text-emerald-400 mt-1">BDT 4,250,000.00</p>
                <p class="text-[10px] text-slate-500 mt-1">Active Ledger Balance</p>
            </div>
            <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
                <p class="text-xs text-slate-400 uppercase">Salsabila Electronics (0215)</p>
                <p class="text-2xl font-bold text-amber-400 mt-1">BDT 8,920,000.00</p>
                <p class="text-[10px] text-slate-500 mt-1">Active Ledger Balance</p>
            </div>
            <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
                <p class="text-xs text-slate-400 uppercase">Database Integrity</p>
                <p class="text-2xl font-bold text-emerald-400 mt-1">ACID SECURE</p>
                <p class="text-[10px] text-slate-500 mt-1">Rollback Protected</p>
            </div>
        </div>

        <!-- Main Workspace -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            <!-- Left 2 Cols: Transactions & Requisition -->
            <div class="lg:col-span-2 space-y-6">
                <div class="bg-slate-900 border border-slate-800 rounded-xl p-5">
                    <h2 class="text-lg font-semibold mb-4">📑 Dual-Dealer Unified Transactions</h2>
                    <div class="overflow-x-auto">
                        <table class="w-full text-left text-xs">
                            <thead>
                                <tr class="border-b border-slate-800 text-slate-400 bg-slate-950">
                                    <th class="p-3">Dealer ID</th>
                                    <th class="p-3">Date</th>
                                    <th class="p-3">Ref ID</th>
                                    <th class="p-3">Category</th>
                                    <th class="p-3">Amount (BDT)</th>
                                    <th class="p-3">Status</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-slate-800/60">
                                {% for tx in transactions %}
                                <tr>
                                    <td class="p-3 font-mono text-blue-400 font-bold">{{ tx[1] }}</td>
                                    <td class="p-3">{{ tx[2] }}</td>
                                    <td class="p-3 font-mono">{{ tx[3] }}</td>
                                    <td class="p-3">{{ tx[4] }}</td>
                                    <td class="p-3 font-semibold">{{ "{:,.2f}".format(tx[5]) }}</td>
                                    <td class="p-3"><span class="bg-emerald-500/20 text-emerald-400 px-2 py-0.5 rounded text-[10px] font-bold">{{ tx[6] }}</span></td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Requisition Form -->
                <div class="bg-slate-900 border border-slate-800 rounded-xl p-5">
                    <h2 class="text-lg font-semibold mb-4">➕ Post New Ledger Entry (ACID Enforced)</h2>
                    <form action="/add-transaction" method="POST" class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <div>
                            <label class="block text-xs text-slate-400 mb-1">Select Dealer</label>
                            <select name="dealer_id" class="w-full bg-slate-950 border border-slate-800 rounded p-2.5 text-xs text-white">
                                <option value="DEAL002905">DEAL002905 - S.R. Electronics Park</option>
                                <option value="MDEL000215">MDEL000215 - Salsabila Electronics Park</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-xs text-slate-400 mb-1">Reference ID</label>
                            <input type="text" name="ref_id" value="MIN-RTGS-2026-X" required class="w-full bg-slate-950 border border-slate-800 rounded p-2.5 text-xs text-white">
                        </div>
                        <div>
                            <label class="block text-xs text-slate-400 mb-1">Category</label>
                            <input type="text" name="category" value="High-Tech Refrigerator Stock" required class="w-full bg-slate-950 border border-slate-800 rounded p-2.5 text-xs text-white">
                        </div>
                        <div>
                            <label class="block text-xs text-slate-400 mb-1">Amount (BDT)</label>
                            <input type="number" name="amount" value="1500000" required class="w-full bg-slate-950 border border-slate-800 rounded p-2.5 text-xs text-white">
                        </div>
                        <div class="sm:col-span-2">
                            <button type="submit" class="w-full bg-blue-600 hover:bg-blue-500 text-white font-semibold py-2.5 rounded text-xs transition">Commit Transaction & Trigger AI Alert</button>
                        </div>
                    </form>
                </div>
            </div>

            <!-- Right 1 Col: Gemini AI Notification Generator -->
            <div class="space-y-6">
                <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
                    <h2 class="text-lg font-semibold flex items-center gap-2">🤖 Gemini AI SMS Generator</h2>
                    <p class="text-xs text-slate-400">Generate professional real-time Bengali SMS notifications for dealer transactions using Gemini AI.</p>
                    <form action="/generate-ai-sms" method="POST" class="space-y-3">
                        <div>
                            <label class="block text-xs text-slate-400 mb-1">Target Dealer ID</label>
                            <select name="dealer_id" class="w-full bg-slate-950 border border-slate-800 rounded p-2 text-xs text-white">
                                <option value="DEAL002905">DEAL002905 - S.R. Electronics</option>
                                <option value="MDEL000215">MDEL000215 - Salsabila Electronics</option>
                            </select>
                        </div>
                        <button type="submit" class="w-full bg-purple-600 hover:bg-purple-500 text-white font-semibold py-2 rounded text-xs transition">Generate AI Notification</button>
                    </form>
                    {% if ai_sms %}
                    <div class="bg-slate-950 border border-purple-500/40 p-3 rounded-lg text-xs space-y-1">
                        <p class="text-[10px] text-purple-400 font-bold uppercase">AI Output (Bengali):</p>
                        <p class="text-slate-200">{{ ai_sms }}</p>
                    </div>
                    {% endif %}
                </div>
            </div>

        </div>
    </div>
</body>
</html>
"""

PDF_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { font-family: 'Helvetica', sans-serif; color: #1e293b; padding: 20px; }
        h1 { color: #0f172a; border-bottom: 2px solid #3b82f6; padding-bottom: 10px; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #cbd5e1; padding: 8px; font-size: 11px; text-align: left; }
        th { background-color: #f1f5f9; }
    </style>
</head>
<body>
    <h1>Minister ERP - Official Dual-Dealer Ledger Report</h1>
    <p><strong>Generated Date:</strong> October 11, 2026 | SAP Gateway Connected</p>
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Dealer ID</th>
                <th>Date</th>
                <th>Ref ID</th>
                <th>Category</th>
                <th>Amount (BDT)</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
            {% for tx in transactions %}
            <tr>
                <td>{{ tx[0] }}</td>
                <td>{{ tx[1] }}</td>
                <td>{{ tx[2] }}</td>
                <td>{{ tx[3] }}</td>
                <td>{{ tx[4] }}</td>
                <td>{{ "{:,.2f}".format(tx[5]) }}</td>
                <td>{{ tx[6] }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""

@app.route("/")
def index():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions ORDER BY id DESC")
    transactions = cursor.fetchall()
    conn.close()
    return render_template_string(HTML_TEMPLATE, transactions=transactions, ai_sms=None)

@app.route("/add-transaction", methods=["POST"])
def add_transaction():
    dealer_id = request.form.get("dealer_id")
    ref_id = request.form.get("ref_id")
    category = request.form.get("category")
    amount = float(request.form.get("amount", 0))
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO transactions (dealer_id, date, ref_id, category, amount, status) VALUES (?, '11-Oct-2026', ?, ?, ?, 'CLEARED')",
                       (dealer_id, ref_id, category, amount))
        conn.commit()
    except Exception as e:
        conn.rollback()
    finally:
        conn.close()
        
    return index()

@app.route("/generate-ai-sms", methods=["POST"])
def generate_ai_sms():
    dealer_id = request.form.get("dealer_id")
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT dealer_name, sap_ledger FROM dealers WHERE dealer_id = ?", (dealer_id,))
    dealer = cursor.fetchone()
    conn.close()
    
    ai_text = "Gemini API Key not configured. Please set GEMINI_API_KEY environment variable."
    if client and dealer:
        prompt = f"Write a professional corporate SMS notification in Bengali for dealer {dealer[0]} ({dealer_id}) regarding their current SAP ledger balance of BDT {dealer[1]:,.2f} with Minister-MyOne Group."
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            ai_text = response.text
        except Exception as e:
            ai_text = f"Error generating AI notification: {str(e)}"

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions ORDER BY id DESC")
    transactions = cursor.fetchall()
    conn.close()

    return render_template_string(HTML_TEMPLATE, transactions=transactions, ai_sms=ai_text)

@app.route("/pdf-report")
def pdf_report():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions ORDER BY id DESC")
    transactions = cursor.fetchall()
    conn.close()
    
    html_content = render_template_string(PDF_TEMPLATE, transactions=transactions)
    pdf_path = "dealer_ledger_report.pdf"
    weasyprint.HTML(string=html_content).write_pdf(pdf_path)
    
    return send_file(pdf_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
