from flask import Flask, jsonify, request
from datetime import datetime
import sqlite3

app = Flask(__name__)

# ডাটাবেস ইনিশিয়ালাইজেশন (SQLite)
def init_db():
    conn = sqlite3.connect('erp_sync.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settlements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dealer_id TEXT,
            txn_id TEXT UNIQUE,
            sap_lid TEXT,
            amount REAL,
            status TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# রিয়েল-টাইম এপিআই রিসিভার এবং সিংক এন্ডপয়েন্ট
@app.route('/api/v1/sync-settlement', methods=['POST'])
def sync_settlement():
    incoming_data = request.json
    
    if not incoming_data or 'transactions' not in incoming_data:
        return jsonify({"status": "ERROR", "message": "Invalid JSON payload"}), 400

    dealer_id = incoming_data.get("dealer_id")
    transactions = incoming_data.get("transactions", [])

    conn = sqlite3.connect('erp_sync.db')
    cursor = conn.cursor()
    
    synced_count = 0
    for txn in transactions:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO settlements (dealer_id, txn_id, sap_lid, amount, status, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                dealer_id,
                txn.get("txn_id"),
                txn.get("sap_lid"),
                txn.get("amount"),
                txn.get("status"),
                datetime.utcnow().isoformat()
            ))
            if cursor.rowcount > 0:
                synced_count += 1
        except Exception as e:
            print(f"Error inserting transaction: {e}")

    conn.commit()
    conn.close()

    return jsonify({
        "status": "SUCCESS",
        "dealer_id": dealer_id,
        "total_synced": synced_count,
        "sync_timestamp": datetime.utcnow().isoformat(),
        "message": "Real-time synchronization completed successfully without manual intervention."
    }), 200

# লাইভ স্ট্যাটাস চেক করার জন্য
@app.route('/api/v1/status', methods=['GET'])
def system_status():
    return jsonify({
        "engine": "Minister & SR Dual ERP Sync Engine",
        "status": "ONLINE",
        "mode": "Real-Time API Active"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
