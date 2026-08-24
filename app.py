import os
import sqlite3
import random
import json
from datetime import datetime

# Safe import for dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Safe import for WeasyPrint
try:
    from weasyprint import HTML
    HAS_WEASYPRINT = True
except ImportError:
    HAS_WEASYPRINT = False

# Safe import for Google Generative AI
try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

# =====================================================================
# ১. এনভায়রনমেন্ট ও জেমিনী এআই কনফিগারেশন (100% Secure)
# =====================================================================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

model = None
if HAS_GENAI and GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception:
        model = None

# =====================================================================
# ২. ডাটাবেজ ইঞ্জিন ও ইনিশিয়াল ডাটা সেটআপ
# =====================================================================
def initialize_production_database():
    """ডাটাবেজ টেবিল কাঠামো এবং ডেমো ডাটা তৈরি করার মূল ফাংশন"""
    conn = sqlite3.connect('minister_main_system.db')
    cursor = conn.cursor()
    
    # ক) ব্যাংক অ্যাকাউন্ট টেবিল
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bank_accounts (
            account_name TEXT PRIMARY KEY,
            balance REAL
        )
    """)
    
    # খ) ওয়্যারহাউজ ইনভেন্টরি বা স্টক টেবিল
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS warehouse_stock (
            product_code TEXT PRIMARY KEY,
            product_name TEXT,
            unit_price REAL,
            stock INTEGER
        )
    """)
    
    # গ) কাস্টমার লেজার বা খতিয়ান টেবিল
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
    
    # ডেমো ডাটা ইনসার্ট (যদি আগে থেকে না থাকে)
    cursor.execute("INSERT OR IGNORE INTO bank_accounts VALUES ('DBBL_MERCHANT', 500000.00)")
    
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
    print("✅ ডাটাবেজ সিস্টেম ১০০% সফলভাবে প্রস্তুত করা হয়েছে।")

# =====================================================================
# ৩. জেমিনী এআই স্মার্ট নোটিফিকেশন ইঞ্জিন
# =====================================================================
def generate_ai_notifications(customer_code, amount, balance, method):
    """জেমিনী এআই দিয়ে পেমেন্ট ও গাড়ি ছাড়ার তাৎক্ষণিক ডাইনামিক বাংলা এসএমএস জেনারেট করা"""
    if model:
        try:
            prompt = f"""
            কাস্টমার {customer_code} পেমেন্ট গেটওয়ে {method}-এর মাধ্যমে ৳{amount:,.2f} পরিশোধ করেছেন। 
            তার বর্তমান বকেয়া লেজার ব্যালেন্স হলো ৳{balance:,.2f}। 
            পেমেন্টটি সফল হওয়ায় গুদাম (ওয়্যাহাউজ) থেকে মালামাল ট্রাকে বা গাড়িতে লোড করে রিলিজ করার অনুমতি দেওয়া হলো। 
            গ্রাহক এবং লজিস্টিকস টিমের জন্য ১ লাইনের একটি অত্যন্ত প্রফেশনাল এবং সুন্দর বাংলা এসএমএস তৈরি করো।
            """
            response = model.generate_content(prompt)
            msg = response.text.strip()
            print(f"\n📱 [এআই ডাইনামিক এসএমএস]: {msg}")
            return msg
        except Exception:
            pass
    
    fallback_msg = f"পেমেন্ট সফল! {method}-এর মাধ্যমে ৳{amount:,.2f} জমা হয়েছে। মালামাল গাড়িতে লোড করার ক্লিয়ারেন্স দেওয়া হলো। বর্তমান বকেয়া: ৳{balance:,.2f}"
    print(f"\n📱 [অটো-এসএমএস (Fallback)]: {fallback_msg}")
    return fallback_msg

# =====================================================================
# ৪. পিডিএফ ডকুমেন্ট জেনারেটর মডিউল (উইজপ্রিন্ট ইঞ্জিন)
# =====================================================================
def create_pdf_invoice(customer_code, invoice_no, product_name, qty, price, total):
    """কাস্টমারের জন্য প্রফেশনাল A4 সাইজ ইনভয়েস পিডিএফ তৈরি করা"""
    current_date = datetime.now().strftime("%d/%m/%Y")
    
    html_invoice = f"""<!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <style>
        @page {{ size: A4 portrait; margin: 15mm; }}
        body {{ font-family: Arial, sans-serif; color: #333; font-size: 10pt; line-height: 1.4; margin: 0; }}
        .header {{ width: 100%; border-bottom: 2px solid #1a365d; padding-bottom: 10px; margin-bottom: 20px; }}
        .company-name {{ font-size: 18pt; font-weight: bold; color: #1a365d; }}
        .doc-type {{ font-size: 16pt; font-weight: bold; color: #c53030; text-align: right; }}
        .info-grid {{ width: 100%; margin-bottom: 25px; border-collapse: collapse; }}
        .info-grid td {{ vertical-align: top; width: 50%; }}
        .card {{ background: #f7fafc; padding: 12px; border-radius: 6px; border: 1px solid #e2e8f0; margin-right: 10px; }}
        .table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
        .table th {{ background: #1a365d; color: white; padding: 8px; font-size: 9.5pt; text-transform: uppercase; }}
        .table td {{ padding: 8px; border-bottom: 1px solid #e2e8f0; }}
        .total-box {{ width: 40%; margin-left: auto; margin-top: 20px; border-collapse: collapse; }}
        .total-box td {{ padding: 6px; font-size: 10pt; }}
        .grand-total {{ background: #1a365d; color: white; font-weight: bold; }}
    </style>
    </head>
    <body>
        <table class="header" style="width:100%;">
            <tr>
                <td><div class="company-name">Minister Hi-Tech Park Ltd.</div></td>
                <td><div class="doc-type">CUSTOMER INVOICE</div></td>
            </tr>
        </table>
        <table class="info-grid">
            <tr>
                <td>
                    <div class="card">
                        <strong>কাস্টমার তথ্য:</strong><br>
                        কোড: {customer_code}<br>
                        S.R ELECTRONICS PARK<br>
                        ঠিকানা: চুয়াডাঙ্গা
                    </div>
                </td>
                <td>
                    <div class="card" style="margin-right:0; margin-left:10px;">
                        <strong>ইনভয়েস তথ্য:</strong><br>
                        নম্বর: {invoice_no}<br>
                        তারিখ: {current_date}<br>
                        ডেলিভারি স্টোর: ত্রিশাল স্টোর
                    </div>
                </td>
            </tr>
        </table>
        <table class="table">
            <thead>
                <tr>
                    <th style="text-align:center;">SL</th>
                    <th>Product Description</th>
                    <th style="text-align:center;">Qty</th>
                    <th style="text-align:right;">Dealer Price</th>
                    <th style="text-align:right;">Total Amount</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="text-align:center;">1</td>
                    <td>{product_name}</td>
                    <td style="text-align:center;">{qty} PC</td>
                    <td style="text-align:right;">{price:,.2f}</td>
                    <td style="text-align:right;">{total:,.2f}</td>
                </tr>
            </tbody>
        </table>
        <table class="total-box">
            <tr class="grand-total">
                <td>Net Amount (BDT):</td>
                <td style="text-align:right;">{total:,.2f} ৳</td>
            </tr>
        </table>
    </body>
    </html>"""
    
    if HAS_WEASYPRINT:
        HTML(string=html_invoice).write_pdf("Output_Customer_Invoice.pdf")
        print("📄 [পিডিএফ ইঞ্জিন]: 'Output_Customer_Invoice.pdf' সফলভাবে জেনারেট হয়েছে।")
    else:
        with open("Output_Customer_Invoice.html", "w", encoding="utf-8") as f:
            f.write(html_invoice)
        print("📄 [এইচটিএমএল ব্যাকআপ]: 'Output_Customer_Invoice.html' সফলভাবে সংরক্ষিত হয়েছে।")

def create_nexus_pro_payment_slip(customer_code, txn_id, amount):
    """ডাচ-বাংলা ব্যাংক Nexus-Pro MasterCard থিমড পিওএস পেমেন্ট স্লিপ তৈরি করা"""
    current_date = datetime.now().strftime("%d/%m/%Y")
    current_time = datetime.now().strftime("%I:%M %p")
    
    html_slip = f"""<!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <style>
        @page {{ size: 100mm 160mm; margin: 6mm; }}
        body {{ font-family: Arial, sans-serif; color: #222; font-size: 9.5pt; line-height: 1.4; margin: 0; }}
        .receipt-card {{ border: 1px solid #d4af37; padding: 12px; border-radius: 8px; background: #fff; }}
        .header {{ text-align: center; border-bottom: 2px solid #1a365d; padding-bottom: 8px; margin-bottom: 12px; }}
        .bank-title {{ font-size: 13pt; font-weight: bold; color: #1a365d; }}
        .card-brand {{ font-size: 10pt; font-weight: bold; color: #b49323; margin-top: 2px; }}
        .status-badge {{ display: inline-block; background: #e6fffa; color: #234e52; border: 1px solid #b2f5ea; font-size: 8pt; padding: 2px 12px; border-radius: 4px; font-weight: bold; margin-top: 6px; }}
        .row-table {{ width: 100%; margin-top: 10px; border-collapse: collapse; }}
        .row-table td {{ padding: 5px 0; border-bottom: 1px dashed #edf2f7; font-size: 9pt; }}
        .label {{ color: #4a5568; }}
        .value {{ font-weight: bold; text-align: right; }}
        .amount-box {{ background: #1a365d; color: white; text-align: center; padding: 10px; margin-top: 12px; border-radius: 6px; }}
        .amount-val {{ font-size: 15pt; font-weight: bold; margin-top: 2px; }}
        .footer-note {{ text-align: center; color: #718096; font-size: 7.5pt; margin-top: 15px; border-top: 1px solid #e2e8f0; padding-top: 8px; }}
    </style>
    </head>
    <body>
        <div class="receipt-card">
            <div class="header">
                <div class="bank-title">Dutch-Bangla Bank</div>
                <div class="card-brand">NEXUS-PRO TRANSACTION</div>
                <div class="status-badge">✓ SUCCESSFUL / সফল</div>
            </div>
            <table class="row-table">
                <tr>
                    <td class="label">মার্চেন্ট নাম:</td>
                    <td class="value">Minister Hi-Tech Park Ltd.</td>
                </tr>
                <tr>
                    <td class="label">পেমেন্ট মোড:</td>
                    <td class="value">Nexus-Pro MasterCard (Debit)</td>
                </tr>
                <tr>
                    <td class="label">কার্ড নম্বর:</td>
                    <td class="value">**** **** **** 5576</td>
                </tr>
                <tr>
                    <td class="label">ট্রানজেকশন আইডি:</td>
                    <td class="value">{txn_id}</td>
                </tr>
                <tr>
                    <td class="label">তারিখ ও সময়:</td>
                    <td class="value">{current_date} | {current_time}</td>
                </tr>
                <tr>
                    <td class="label">গ্রাহকের কোড:</td>
                    <td class="value">{customer_code}</td>
                </tr>
            </table>
            <div class="amount-box">
                <div style="font-size: 8pt; text-transform: uppercase;">TRANSACTION AMOUNT</div>
                <div class="amount-val">৳ {amount:,.2f}</div>
            </div>
            <div class="footer-note">
                Thank you for using DBBL Electronic Banking!<br>
                পেমেন্ট সফলভাবে রিয়েল-টাইম সিনক্রোনাইজড হয়েছে।
            </div>
        </div>
    </body>
    </html>"""
    
    if HAS_WEASYPRINT:
        HTML(string=html_slip).write_pdf("Output_NexusPay_Slip.pdf")
        print("💳 [পিডিএফ ইঞ্জিন]: 'Output_NexusPay_Slip.pdf' সফলভাবে জেনারেট হয়েছে।")
    else:
        with open("Output_NexusPay_Slip.html", "w", encoding="utf-8") as f:
            f.write(html_slip)
        print("💳 [এইচটিএমএল ব্যাকআপ]: 'Output_NexusPay_Slip.html' সফলভাবে সংরক্ষিত হয়েছে।")

def create_pdf_ledger_statement(customer_code):
    """ডাটাবেজ থেকে লাইভ খতিয়ান ডাটা রিড করে অফিসিয়াল লেজার স্টেটমেন্ট পিডিএফ তৈরি করা"""
    conn = sqlite3.connect('minister_main_system.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date, gl_voucher, ref_no, description, remarks, debit, credit, current_balance 
        FROM customer_ledger WHERE customer_code = ?
    """, (customer_code,))
    rows = cursor.fetchall()
    conn.close()

    table_rows_html = ""
    total_debit = 0.0
    total_credit = 0.0
    final_balance = 0.0

    for row in rows:
        date, voucher, ref, desc, remarks, debit, credit, balance = row
        debit_val = debit if debit else 0.0
        credit_val = credit if credit else 0.0
        debit_str = f"{debit_val:,.2f}" if debit_val else ""
        credit_str = f"{credit_val:,.2f}" if credit_val else ""
        balance_str = f"{balance:,.2f}" if balance is not None else ""
        
        total_debit += debit_val
        total_credit += credit_val
        if balance is not None:
            final_balance = balance

        voucher_display = voucher if voucher else "-"
        ref_display = ref if ref else "-"
        remarks_display = remarks if remarks else "-"

        table_rows_html += f"""
        <tr>
            <td style="text-align:center;">{date}</td>
            <td style="text-align:center;">{voucher_display}</td>
            <td style="text-align:center;">{ref_display}</td>
            <td>{desc.replace(chr(10), '<br>')}</td>
            <td style="text-align:center;">{remarks_display}</td>
            <td style="text-align:right;">{debit_str}</td>
            <td style="text-align:right;">{credit_str}</td>
            <td style="text-align:right; font-weight:bold;">{balance_str}</td>
        </tr>
        """

    html_statement = f"""<!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <style>
        @page {{ size: A4 landscape; margin: 12mm; }}
        body {{ font-family: Arial, sans-serif; font-size: 9pt; color: #000; margin: 0; }}
        .header-bar {{ background-color: #d1d5db; text-align: center; padding: 6px 0; font-size: 13pt; font-weight: bold; border-radius: 4px; }}
        .date-range {{ text-align: center; font-size: 9.5pt; font-weight: bold; padding: 4px 0; border-bottom: 1px solid #9ca3af; margin-bottom: 12px; }}
        .customer-meta {{ width: 100%; margin-bottom: 12px; border-collapse: collapse; font-size: 9.5pt; }}
        .customer-meta td {{ padding: 3px 0; }}
        .ledger-table {{ width: 100%; border-collapse: collapse; margin-top: 5px; }}
        .ledger-table th {{ border: 1px solid #4b5563; padding: 6px; font-weight: bold; text-align: center; background-color: #f3f4f6; font-size: 8.5pt; }}
        .ledger-table td {{ border: 1px solid #9ca3af; padding: 6px; vertical-align: middle; font-size: 8.5pt; }}
        .total-row td {{ font-weight: bold; border-top: 2px solid #111827; border-bottom: 2px solid #111827; background-color: #f9fafb; }}
    </style>
    </head>
    <body>
        <div class="header-bar">Minister Hi-Tech Park Electronics Ltd.</div>
        <div class="date-range">Customer Statement of Account | As on {datetime.now().strftime('%d-%b-%Y')}</div>
        
        <table class="customer-meta">
            <tr>
                <td style="width: 50%;"><strong>Customer Code:</strong> {customer_code}</td>
                <td style="width: 50%; text-align: right;"><strong>Customer Name:</strong> S.R ELECTRONICS PARK</td>
            </tr>
            <tr>
                <td><strong>Location:</strong> Chuadanga</td>
                <td style="text-align: right;"><strong>Print Time:</strong> {datetime.now().strftime('%d-%b-%Y %I:%M %p')}</td>
            </tr>
        </table>

        <table class="ledger-table">
            <thead>
                <tr>
                    <th style="width: 10%;">Date</th>
                    <th style="width: 12%;">GL Voucher</th>
                    <th style="width: 12%;">Ref No</th>
                    <th style="width: 26%;">Description</th>
                    <th style="width: 10%;">Remarks</th>
                    <th style="width: 10%;">Debit (৳)</th>
                    <th style="width: 10%;">Credit (৳)</th>
                    <th style="width: 10%;">Balance (৳)</th>
                </tr>
            </thead>
            <tbody>
                {table_rows_html}
                <tr class="total-row">
                    <td colspan="5" style="text-align: right; font-weight: bold;">Total / Closing Balance:</td>
                    <td style="text-align: right;">{total_debit:,.2f}</td>
                    <td style="text-align: right;">{total_credit:,.2f}</td>
                    <td style="text-align: right; color: #b91c1c;">{final_balance:,.2f}</td>
                </tr>
            </tbody>
        </table>
    </body>
    </html>"""
    
    if HAS_WEASYPRINT:
        HTML(string=html_statement).write_pdf("Output_Statement_Of_Account.pdf")
        print("📊 [পিডিএফ ইঞ্জিন]: 'Output_Statement_Of_Account.pdf' সফলভাবে আপডেট ও জেনারেট হয়েছে।")
    else:
        with open("Output_Statement_Of_Account.html", "w", encoding="utf-8") as f:
            f.write(html_statement)
        print("📊 [এইচটিএমএল ব্যাকআপ]: 'Output_Statement_Of_Account.html' সফলভাবে সংরক্ষিত হয়েছে।")

# =====================================================================
# ৫. কোয়ান্টাম লাইভ রিয়েল-টাইম সিনক্রোনাইজেশন ইঞ্জিন (Webhook Server Core)
# =====================================================================
def execute_quantum_realtime_sync(webhook_payload):
    """
    পেমেন্ট গেটওয়ে মার্চেন্ট নোটিফিকেশন আসার সাথে সাথে
    ব্যাংক অ্যাকাউন্ট, ইনভেন্টরি স্টক এবং কাস্টমার খতিয়ানকে ১০০% সিনক্রোনাইজ করে
    """
    txn_id = webhook_payload['txn_id']
    customer_code = webhook_payload['customer_code']
    amount_paid = float(webhook_payload['amount'])
    product_code = webhook_payload['product_code']
    qty_purchased = int(webhook_payload['quantity'])
    
    conn = sqlite3.connect('minister_main_system.db')
    cursor = conn.cursor()
    
    try:
        print("\n⚡ [রিয়েল-টাইম সিঙ্ক ইঞ্জিন সচল]: চেইন রিঅ্যাকশন প্রসেস শুরু হচ্ছে...")
        
        # ১. ব্যাংকিং এপিআই সিঙ্ক: ডাচ-বাংলা ব্যাংক মার্চেন্ট অ্যাকাউন্টে টাকা যোগ করা
        cursor.execute("UPDATE bank_accounts SET balance = balance + ? WHERE account_name = 'DBBL_MERCHANT'", (amount_paid,))
        
        # ২. ওয়্যারহাউজ স্টক সিঙ্ক: গুদাম থেকে রিয়েল-টাইমে প্রোডাক্টের স্টক মাইনাস করা
        cursor.execute("UPDATE warehouse_stock SET stock = stock - ? WHERE product_code = ?", (qty_purchased, product_code))
        
        # প্রোডাক্টের নাম এবং একক মূল্য তুলে আনা ইনভয়েসের জন্য
        cursor.execute("SELECT product_name, unit_price FROM warehouse_stock WHERE product_code = ?", (product_code,))
        prod_row = cursor.fetchone()
        p_name, p_price = prod_row[0], prod_row[1]
        order_total_value = p_price * qty_purchased
        
        # ৩. কাস্টমার লেজার বা খতিয়ান সিঙ্ক: বকেয়া এবং পেমেন্ট ক্যালকুলেশন
        cursor.execute("SELECT current_balance FROM customer_ledger WHERE customer_code = ? ORDER BY id DESC LIMIT 1", (customer_code,))
        old_balance_row = cursor.fetchone()
        old_balance = float(old_balance_row[0]) if old_balance_row else 0.0
        
        # দেনা-পাওনার নতুন ক্লোজিং ব্যালেন্স হিসাব
        new_closing_balance = old_balance - amount_paid
        current_date = datetime.now().strftime("%d-%b-%y")
        
        # ৪. কাস্টমার লেজারে নতুন পেমেন্ট ক্রেডিট রেজিস্টার করা
        cursor.execute("""
            INSERT INTO customer_ledger (customer_code, date, gl_voucher, ref_no, description, remarks, credit, current_balance)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (customer_code, current_date, txn_id, txn_id, f"DBBL-103.110.39646\n(Minister Hi-Tech Park Electronics Ltd.)", current_date, amount_paid, new_closing_balance))
        
        # ডাটাবেজের সব পরিবর্তন রিয়েল-টাইমে সেভ করা (ACID Core Commit)
        conn.commit()
        print(f"✅ [১০০% সিঙ্ক সম্পন্ন]: ডাটাবেজ লক রিলিজড। কাস্টমার ক্লোজিং ব্যালেন্স: ৳{new_closing_balance:,.2f}")
        
        # ৫. ডাইনামিক এআই এসএমএস জেনারেশন (জেমিনী এপিআই ট্রিগার)
        generate_ai_notifications(customer_code, amount_paid, new_closing_balance, "Nexus-Pro MasterCard")
        
        # ৬. ৩টি প্রফেশনাল ডকুমেন্ট পিডিএফ ফরম্যাটে একসাথে অটো-আপডেট করা
        create_pdf_invoice(customer_code, f"INV-{random.randint(10000,99999)}", p_name, qty_purchased, p_price, order_total_value)
        create_nexus_pro_payment_slip(customer_code, txn_id, amount_paid)
        create_pdf_ledger_statement(customer_code)
        
        print("\n🎉 [অভিনন্দন]: টাকা ব্যাংকে জমা হয়েছে, স্টক মাইনাস হয়েছে এবং গাড়ি গুদাম থেকে রওনা দিয়েছে!")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ [ক্রিটিক্যাল এরর]: রিয়েল-টাইম সিঙ্ক ব্যর্থ! ডাটা সুরক্ষার্থে রোলব্যাক করা হয়েছে। কারণ: {e}")
    finally:
        conn.close()

# =====================================================================
# 🚀 টেস্ট রান বা এক্সিকিউশন পয়েন্ট
# =====================================================================
if __name__ == "__main__":
    if os.path.exists('minister_main_system.db'):
        os.remove('minister_main_system.db')
    initialize_production_database()
    live_incoming_webhook_payload = {
        "txn_id": "RCT-057649",
        "customer_code": "DEAL002905",
        "amount": "135000.00",
        "product_code": "120001808",
        "quantity": 2
    }
    execute_quantum_realtime_sync(live_incoming_webhook_payload)
