from datetime import datetime
import os
import sqlite3

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

DB_NAME = "minister_main_system.db"


def initialize_production_database():
    """Initializes bank accounts and customer ledger tables."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bank_accounts (
            account_name TEXT PRIMARY KEY,
            account_title TEXT,
            account_number TEXT,
            routing_number TEXT,
            branch_name TEXT,
            swift_code TEXT,
            balance REAL
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
            debit REAL DEFAULT 0.0,
            credit REAL DEFAULT 0.0,
            current_balance REAL
        )
    """)

    cursor.execute("""
        INSERT OR REPLACE INTO bank_accounts VALUES 
        ('BRAC_AGENT_SME', 'SOHAG MISTANNO VANDER', '2071024810001', '060270609', 'AGENT BANKING SUB FIVE', 'BRAKBDDH', 150000.00)
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO customer_ledger (id, customer_code, date, description, debit, current_balance)
        VALUES (1, 'DEAL002905', '26-Nov-25', 'Opening Balance', 279154.00, 279154.00)
    """)

    conn.commit()
    conn.close()
    print("✅ ব্র্যাক ব্যাংক এজেন্ট ব্যাংকিং ডাটাবেজ প্রস্তুত।")


def create_brac_bank_payment_slip(
    customer_code, txn_id, amount, acc_details, output_filename="BRAC_Slip"
):
    """Generates an HTML/PDF confirmation slip."""
    current_date = datetime.now().strftime("%d-%b-%Y")
    current_time = datetime.now().strftime("%I:%M %p")

    html_slip = f"""<!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <style>
        @page {{ size: 100mm 180mm; margin: 6mm; }}
        body {{ font-family: Arial, sans-serif; color: #1f2937; font-size: 8.5pt; margin: 0; }}
        .card {{ border: 2px solid #00529b; border-radius: 8px; padding: 12px; background: #ffffff; }}
        .header {{ text-align: center; border-bottom: 2px solid #00529b; padding-bottom: 8px; margin-bottom: 8px; }}
        .bank-title {{ font-size: 13pt; font-weight: bold; color: #00529b; }}
        .network-tag {{ font-size: 8pt; color: #0284c7; font-weight: bold; margin-top: 2px; }}
        .badge {{ display: inline-block; background: #ecfdf5; color: #065f46; border: 1px solid #a7f3d0; font-size: 7.5pt; padding: 2px 8px; border-radius: 4px; font-weight: bold; margin-top: 4px; }}
        .table {{ width: 100%; border-collapse: collapse; margin-top: 6px; }}
        .table td {{ padding: 3.5px 0; border-bottom: 1px dashed #e5e7eb; font-size: 8pt; }}
        .label {{ color: #4b5563; }}
        .value {{ font-weight: bold; text-align: right; }}
        .amount-card {{ background: #00529b; color: white; text-align: center; padding: 8px; border-radius: 6px; margin-top: 8px; }}
        .amount-val {{ font-size: 13pt; font-weight: bold; margin-top: 2px; }}
        .footer {{ text-align: center; color: #6b7280; font-size: 7pt; margin-top: 8px; border-top: 1px solid #e5e7eb; padding-top: 5px; }}
    </style>
    </head>
    <body>
        <div class="card">
            <div class="header">
                <div class="bank-title">BRAC BANK PLC</div>
                <div class="network-tag">NPSB / BEFTN / AGENT REAL-TIME SETTLEMENT</div>
                <div class="badge">✓ SETTLED & CREDITED</div>
            </div>
            <table class="table">
                <tr><td class="label">Beneficiary Title:</td><td class="value">{acc_details['title']}</td></tr>
                <tr><td class="label">Account Number:</td><td class="value">{acc_details['acc_no']}</td></tr>
                <tr><td class="label">Branch Name:</td><td class="value">{acc_details['branch']}</td></tr>
                <tr><td class="label">Routing Number:</td><td class="value">{acc_details['routing']}</td></tr>
                <tr><td class="label">SWIFT Code:</td><td class="value">{acc_details['swift']}</td></tr>
                <tr><td class="label">Sender / Customer:</td><td class="value">{customer_code}</td></tr>
                <tr><td class="label">Transaction ID:</td><td class="value">{txn_id}</td></tr>
                <tr><td class="label">Date & Time:</td><td class="value">{current_date} | {current_time}</td></tr>
            </table>
            <div class="amount-card">
                <div style="font-size: 7pt; text-transform: uppercase;">Transfer Amount</div>
                <div class="amount-val">৳ {amount:,.2f}</div>
            </div>
            <div class="footer">
                BRAC Bank 24/7 Astha Electronic Engine<br>
                Official Ledger Credit Confirmation
            </div>
        </div>
    </body>
    </html>"""

    if HAS_WEASYPRINT:
        pdf_path = f"Output_{output_filename}.pdf"
        HTML(string=html_slip).write_pdf(pdf_path)
        print(f"💳 [পিডিএফ ইঞ্জিন]: '{pdf_path}' প্রস্তুত হয়েছে।")
    else:
        html_path = f"Output_{output_filename}.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_slip)
        print(f"💳 [এইচটিএমএল ব্যাকআপ]: '{html_path}' সংরক্ষিত হয়েছে।")


def execute_brac_realtime_transfer(transfer_payload, account_key="BRAC_AGENT_SME"):
    """Executes atomic transfer and updates customer ledger."""
    txn_id = transfer_payload["txn_id"]
    customer_code = transfer_payload["customer_code"]
    amount = float(transfer_payload["amount"])

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        # ১. ডাটাবেজ থেকে ব্যাংক অ্যাকাউন্টের বিবরণ নেওয়া
        cursor.execute(
            "SELECT account_title, account_number, branch_name, routing_number, swift_code FROM bank_accounts WHERE account_name = ?",
            (account_key,),
        )
        bank_row = cursor.fetchone()

        if not bank_row:
            raise ValueError(f"Bank account key '{account_key}' not found.")

        acc_details = {
            "title": bank_row[0],
            "acc_no": bank_row[1],
            "branch": bank_row[2],
            "routing": bank_row[3],
            "swift": bank_row[4],
        }

        print(f"\n⚡ [BRAC Bank Real-Time Transfer]: ৳{amount:,.2f} ক্রেডিট হচ্ছে...")

        # ২. অ্যাকাউন্টে ব্যালেন্স যোগ
        cursor.execute(
            "UPDATE bank_accounts SET balance = balance + ? WHERE account_name = ?",
            (amount, account_key),
        )

        # ৩. কাস্টমার লেজার ব্যালেন্স এডজাস্টমেন্ট
        cursor.execute(
            "SELECT current_balance FROM customer_ledger WHERE customer_code = ? ORDER BY id DESC LIMIT 1",
            (customer_code,),
        )
        old_row = cursor.fetchone()
        old_balance = float(old_row[0]) if old_row else 0.0
        new_closing_balance = old_balance - amount
        current_date = datetime.now().strftime("%d-%b-%y")

        cursor.execute(
            """
            INSERT INTO customer_ledger (customer_code, date, gl_voucher, ref_no, description, remarks, credit, current_balance)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                customer_code,
                current_date,
                txn_id,
                txn_id,
                f"BRAC Bank Transfer\n(A/C: {acc_details['acc_no']})",
                current_date,
                amount,
                new_closing_balance,
            ),
        )

        conn.commit()
        print(
            f"✅ [সফল]: ব্র্যাক ব্যাংক A/C ({acc_details['acc_no']}) এ ৳{amount:,.2f} সফলভাবে জমা হয়েছে।"
        )
        print(f"📊 [আপডেট লেজার ব্যালেন্স]: ৳{new_closing_balance:,.2f}")

        # ৪. স্লিপ জেনারেট
        create_brac_bank_payment_slip(
            customer_code,
            txn_id,
            amount,
            acc_details,
            output_filename=f"BRAC_{txn_id}",
        )

    except Exception as e:
        conn.rollback()
        print(f"❌ [এরর]: ট্রান্সফার ব্যর্থ: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    initialize_production_database()

    transfer_50k = {
        "txn_id": "BRAC-NPSB-984210",
        "customer_code": "DEAL002905",
        "amount": "50000.00",
    }

    execute_brac_realtime_transfer(transfer_50k)
