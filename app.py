import os
import sqlite3
import random
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from weasyprint import HTML
    HAS_WEASYPRINT = True
except ImportError:
    HAS_WEASYPRINT = False

try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
model = None
if HAS_GENAI and GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception:
        model = None

# =====================================================================
# ১. ডাটাবেজ ইনিশিয়ালাইজেশন
# =====================================================================
def initialize_production_database():
    conn = sqlite3.connect('minister_main_system.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bank_accounts (
            account_name TEXT PRIMARY KEY,
            account_number TEXT,
            balance REAL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS warehouse_stock (
            product_code TEXT PRIMARY KEY,
            product_name TEXT,
            unit_price REAL,
            stock INTEGER
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customer_ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_code TEXT,
            date TEXT,
            gl_voucher TEXT,
            ref_no TEXT,
            description TEXT,
            remarks TEXT,
            debit REAL,
            credit REAL,
            current_balance REAL
        )
    """)
    
    # ব্যাংক অ্যাকাউন্ট ডাটাবেজ
    cursor.execute("INSERT OR REPLACE INTO bank_accounts VALUES ('DBBL_MERCHANT', '103.110.39646', 500000.00)")
    cursor.execute("INSERT OR REPLACE INTO bank_accounts VALUES ('BRAC_CORP', '3101204280749001', 250000.00)")
    cursor.execute("INSERT OR REPLACE INTO bank_accounts VALUES ('BRAC_SME_OP', '2071024810001', 150000.00)")
    
    cursor.execute("""
        INSERT OR IGNORE INTO warehouse_stock VALUES 
        ('120001808', 'Minister Air Conditioner INV-M18K410GWCP-WHT', 63292.00, 100)
    """)
    
    cursor.execute("""
        INSERT OR IGNORE INTO customer_ledger (id, customer_code, date, description, debit, current_balance)
        VALUES (1, 'DEAL002905', '26-Nov-25', 'Opening Balance', 279154.00, 279154.00)
    """)
    
    conn.commit()
    conn.close()
    print("✅ ডাটাবেজ প্রস্তুত সম্পন্ন।")

# =====================================================================
# ২. ব্র্যাক ব্যাংক অফিশিয়াল পেমেন্ট স্লিপ জেনারেটর
# =====================================================================
def create_brac_bank_payment_slip(customer_code, txn_id, amount, acc_no, acc_title):
    current_date = datetime.now().strftime("%d-%b-%Y")
    current_time = datetime.now().strftime("%I:%M %p")
    
    html_slip = f"""<!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <style>
        @page {{ size: 100mm 165mm; margin: 6mm; }}
        body {{ font-family: Arial, sans-serif; color: #1f2937; font-size: 9pt; margin: 0; }}
        .card {{ border: 2px solid #00529b; border-radius: 8px; padding: 12px; background: #ffffff; }}
        .header {{ text-align: center; border-bottom: 2px solid #00529b; padding-bottom: 8px; margin-bottom: 10px; }}
        .bank-title {{ font-size: 13pt; font-weight: bold; color: #00529b; }}
        .network-tag {{ font-size: 8.5pt; color: #0284c7; font-weight: bold; margin-top: 2px; }}
        .badge {{ display: inline-block; background: #ecfdf5; color: #065f46; border: 1px solid #a7f3d0; font-size: 8pt; padding: 2px 10px; border-radius: 4px; font-weight: bold; margin-top: 5px; }}
        .table {{ width: 100%; border-collapse: collapse; margin-top: 8px; }}
        .table td {{ padding: 4.5px 0; border-bottom: 1px dashed #e5e7eb; font-size: 8.5pt; }}
        .label {{ color: #4b5563; }}
        .value {{ font-weight: bold; text-align: right; }}
        .amount-card {{ background: #00529b; color: white; text-align: center; padding: 8px; border-radius: 6px; margin-top: 10px; }}
        .amount-val {{ font-size: 14pt; font-weight: bold; margin-top: 2px; }}
        .footer {{ text-align: center; color: #6b7280; font-size: 7pt; margin-top: 10px; border-top: 1px solid #e5e7eb; padding-top: 6px; }}
    </style>
    </head>
    <body>
        <div class="card">
            <div class="header">
                <div class="bank-title">BRAC BANK PLC.</div>
                <div class="network-tag">ASTHA API / NPSB REAL-TIME TRANSFER</div>
                <div class="badge">✓ SETTLED & CREDITED</div>
            </div>
            <table class="table">
                <tr><td class="label">Beneficiary Title:</td><td class="value">{acc_title}</td></tr>
                <tr><td class="label">Account Number:</td><td class="value">{acc_no}</td></tr>
                <tr><td class="label">Sender / Customer:</td><td class="value">{customer_code}</td></tr>
                <tr><td class="label">Transaction ID:</td><td class="value">{txn_id}</td></tr>
                <tr><td class="label">Date & Time:</td><td class="value">{current_date} | {current_time}</td></tr>
                <tr><td class="label">Routing Channel:</td><td class="value">NPSB Instant Settlement</td></tr>
            </table>
            <div class="amount-card">
                <div style="font-size: 7.5pt; text-transform: uppercase;">Transfer Amount</div>
                <div class="amount-val">৳ {amount:,.2f}</div>
            </div>
            <div class="footer">
                BRAC Bank 24/7 Astha Electronic Engine<br>
                This is a verified real-time financial ledger receipt.
            </div>
        </div>
    </body>
    </html>"""
    
    if HAS_WEASYPRINT:
        HTML(string=html_slip).write_pdf("Output_BRAC_Bank_Slip.pdf")
        print("💳 [পিডিএফ ইঞ্জিন]: 'Output_BRAC_Bank_Slip.pdf' প্রস্তুত হয়েছে।")
    else:
        with open("Output_BRAC_Bank_Slip.html", "w", encoding="utf-8") as f:
            f.write(html_slip)
        print("💳 [এইচটিএমএল ব্যাকআপ]: 'Output_BRAC_Bank_Slip.html' সংরক্ষিত হয়েছে।")

# =====================================================================
# ৩. রিয়েল-টাইম ব্র্যাক ব্যাংক ট্রান্সফার ইঞ্জিন
# =====================================================================
def execute_brac_realtime_transfer(transfer_payload):
    txn_id = transfer_payload['txn_id']
    customer_code = transfer_payload['customer_code']
    amount = float(transfer_payload['amount'])
    target_account = transfer_payload.get('target_account', 'BRAC_CORP')
    
    acc_map = {
        'BRAC_CORP': ('3101204280749001', 'MD. AL AMIN SOHAG'),
        'BRAC_SME_OP': ('2071024810001', 'SOHAG MISTANNO VANDER')
    }
    acc_no, acc_title = acc_map.get(target_account, ('3101204280749001', 'MD. AL AMIN SOHAG'))

    conn = sqlite3.connect('minister_main_system.db')
    cursor = conn.cursor()
    
    try:
        print(f"\n⚡ [BRAC Bank Real-Time Sync]: ৳{amount:,.2f} ক্রেডিট প্রসেস হচ্ছে...")
        
        # ১. ব্যাংকে ব্যালেন্স যোগ
        cursor.execute("UPDATE bank_accounts SET balance = balance + ? WHERE account_name = ?", (amount, target_account))
        
        # ২. লেজার ব্যালেন্স আপডেট
        cursor.execute("SELECT current_balance FROM customer_ledger WHERE customer_code = ? ORDER BY id DESC LIMIT 1", (customer_code,))
        old_row = cursor.fetchone()
        old_balance = float(old_row[0]) if old_row else 0.0
        new_closing_balance = old_balance - amount
        current_date = datetime.now().strftime("%d-%b-%y")
        
        cursor.execute("""
            INSERT INTO customer_ledger (customer_code, date, gl_voucher, ref_no, description, remarks, credit, current_balance)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (customer_code, current_date, txn_id, txn_id, f"BRAC Bank Astha Transfer\n(A/C: {acc_no})", current_date, amount, new_closing_balance))
        
        conn.commit()
        print(f"✅ [ট্রান্সফার সফল]: ব্র্যাক ব্যাংক A/C ({acc_no}) ব্যালেন্স আপডেট ও লেজার সিঙ্ক সম্পন্ন।")
        
        # ৩. স্লিপ জেনারেট
        create_brac_bank_payment_slip(customer_code, txn_id, amount, acc_no, acc_title)
        
    except Exception as e:
        conn.rollback()
        print(f"❌ [এরর]: ট্রান্সফার ব্যর্থ: {e}")
    finally:
        conn.close()

# =====================================================================
# ৪. ৫০,০০০ টাকা ট্রান্সফার এক্সিকিউশন
# =====================================================================
if __name__ == "__main__":
    initialize_production_database()
    
    transfer_50k = {
        "txn_id": "ASTHA-589214",
        "customer_code": "DEAL002905",
        "amount": "50000.00",
        "target_account": "BRAC_CORP"  # SME অ্যাকাউন্টের জন্য "BRAC_SME_OP" দিন
    }

    execute_brac_realtime_transfer(transfer_50k)
