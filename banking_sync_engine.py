import os
import json
import sqlite3
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DB_NAME = os.getenv('DB_NAME', 'minister_main_system.db')

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/v1/banking/sync-ledger', methods=['POST'])
def sync_banking_ledger():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Invalid payload or empty request body'}), 400

    dealer_code = data.get('dealer_code')
    bank_txn_id = data.get('bank_txn_id')
    amount = data.get('amount')
    bank_name = data.get('bank_name', 'DBBL / EBL Gateway')

    if not dealer_code or not bank_txn_id or not amount:
        return jsonify({'error': 'Missing required banking sync parameters (dealer_code, bank_txn_id, amount)'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # ট্রানজেকশন শুরু করা (ACID Compliance)
        cursor.execute('BEGIN TRANSACTION')

        # পূর্বের লেজার ব্যালেন্স চেক করা
        cursor.execute(
            'SELECT current_balance FROM customer_ledger WHERE customer_code = ? ORDER BY id DESC LIMIT 1',
            (dealer_code,)
        )
        row = cursor.fetchone()

        current_balance = row['current_balance'] if row else 0.0
        new_balance = float(current_balance) - float(amount)
        current_date = data.get('date', '12/09/2026')

        # লেজার এন্ট্রি ইনসার্ট করা
        cursor.execute(
            '''
            INSERT INTO customer_ledger 
            (customer_code, date, gl_voucher, ref_no, description, credit, current_balance)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                dealer_code,
                current_date,
                bank_txn_id,
                bank_txn_id,
                f'Automated Banking Sync via {bank_name}',
                amount,
                new_balance
            )
        )

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            'status': 'success',
            'message': f'Banking transaction {bank_txn_id} successfully synchronized for {dealer_code}',
            'previous_balance': current_balance,
            'amount_credited': amount,
            'closing_balance': new_balance,
            'timestamp': '2026-09-12T07:29:42+06:00'
        }), 200

    except Exception as e:
        if 'conn' in locals() and conn:
            conn.rollback()
            conn.close()
        return jsonify({'error': 'Banking sync database transaction failed', 'details': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('BANKING_PORT', 5001))
    app.run(host='0.0.0.0', port=port)
