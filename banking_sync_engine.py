import sqlite3
import os

DATABASE_NAME = "erp_database.db"

def init_db():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lid TEXT UNIQUE NOT NULL,
            receiver_name TEXT NOT NULL,
            receiver_bank TEXT NOT NULL,
            receiver_account TEXT NOT NULL,
            sender_card_type TEXT,
            sender_card_number TEXT,
            sender_account TEXT NOT NULL,
            nexuspay_id TEXT,
            amount REAL NOT NULL,
            transaction_date TEXT NOT NULL,
            status TEXT DEFAULT 'SUCCESSFUL',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def sync_transaction(data):
    init_db()
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO transactions (
                lid, receiver_name, receiver_bank, receiver_account, 
                sender_card_type, sender_card_number, sender_account, 
                nexuspay_id, amount, transaction_date, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '', (
            data.get('lid'),
            data.get('receiver_name'),
            data.get('receiver_bank'),
            data.get('receiver_account'),
            data.get('sender_card_type'),
            data.get('sender_card_number'),
            data.get('sender_account'),
            data.get('nexuspay_id'),
            data.get('amount'),
            data.get('transaction_date'),
            data.get('status', 'SUCCESSFUL')
        ))
        conn.commit()
        print(f"Success: Transaction {data.get('lid')} synchronized successfully.")
        return True
    except sqlite3.IntegrityError:
        print(f"Duplicate Error: Transaction LID {data.get('lid')} already exists in database.")
        return False
    except Exception as e:
        print(f"Error syncing transaction: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    # ছবি এবং লেজার ডাটা থেকে প্রাপ্ত ৯টি আসল ট্রানজেকশন ডেটাসেট
    transactions_list = [
        {
            "lid": "LID02037811634",
            "receiver_name": "MYONE ELECTRONICS INDUSTRIES LTD.",
            "receiver_bank": "Dutch-Bangla Bank PLC.",
            "receiver_account": "1041100034560",
            "sender_card_type": "Agent Banking Card",
            "sender_card_number": "0130 **** **** 5995",
            "sender_account": "7017511802593",
            "nexuspay_id": "01719732134",
            "amount": 30005.00,
            "transaction_date": "28-Jul-2026 07:27 PM",
            "status": "SUCCESSFUL"
        },
        {
            "lid": "LID02104465787",
            "receiver_name": "MYONE ELECTRONICS INDUSTRIES LTD.",
            "receiver_bank": "Dutch-Bangla Bank PLC.",
            "receiver_account": "1041100034560",
            "sender_card_type": "Agent Banking Card",
            "sender_card_number": "0130 **** **** 5995",
            "sender_account": "7017511802593",
            "nexuspay_id": "01719732134",
            "amount": 50000.00,
            "transaction_date": "31-Aug-2026 05:33 PM",
            "status": "SUCCESSFUL"
        },
        {
            "lid": "LID01976788453",
            "receiver_name": "MyOne Electronics Industries Ltd.",
            "receiver_bank": "Dutch-Bangla Bank PLC.",
            "receiver_account": "1041100034560",
            "sender_card_type": "FT/NEXP",
            "sender_card_number": "N/A",
            "sender_account": "DEAL002905",
            "nexuspay_id": "100NEXP26187M597",
            "amount": 238000.00,
            "transaction_date": "06-Jul-2026",
            "status": "SUCCESSFUL"
        },
        {
            "lid": "LID01996890123",
            "receiver_name": "MyOne Electronics Industries Ltd.",
            "receiver_bank": "Dutch-Bangla Bank PLC.",
            "receiver_account": "1041100034560",
            "sender_card_type": "FT/NEXP",
            "sender_card_number": "N/A",
            "sender_account": "DEAL002905",
            "nexuspay_id": "100NEXP26188M616",
            "amount": 270000.00,
            "transaction_date": "07-Jul-2026",
            "status": "SUCCESSFUL"
        },
        {
            "lid": "LID01996889539",
            "receiver_name": "MyOne Electronics Industries Ltd.",
            "receiver_bank": "Dutch-Bangla Bank PLC.",
            "receiver_account": "1041100034560",
            "sender_card_type": "FT/NEXP",
            "sender_card_number": "N/A",
            "sender_account": "DEAL002905",
            "nexuspay_id": "100NEXP26188M584",
            "amount": 230000.00,
            "transaction_date": "07-Jul-2026",
            "status": "SUCCESSFUL"
        },
        {
            "lid": "LID01998640246",
            "receiver_name": "MyOne Electronics Industries Ltd.",
            "receiver_bank": "Dutch-Bangla Bank PLC.",
            "receiver_account": "1041100034560",
            "sender_card_type": "NPSB/NXN",
            "sender_card_number": "N/A",
            "sender_account": "DEAL002905",
            "nexuspay_id": "100NXN126189M586",
            "amount": 297000.00,
            "transaction_date": "08-Jul-2026",
            "status": "SUCCESSFUL"
        },
        {
            "lid": "LID01938788435",
            "receiver_name": "MyOne Electronics Industries Ltd.",
            "receiver_bank": "Dutch-Bangla Bank PLC.",
            "receiver_account": "1041100034560",
            "sender_card_type": "NPSB/NXN",
            "sender_card_number": "N/A",
            "sender_account": "DEAL002905",
            "nexuspay_id": "100NXN126189M591",
            "amount": 285000.00,
            "transaction_date": "08-Jul-2026",
            "status": "SUCCESSFUL"
        },
        {
            "lid": "LID01996914258",
            "receiver_name": "MyOne Electronics Industries Ltd.",
            "receiver_bank": "Dutch-Bangla Bank PLC.",
            "receiver_account": "1041100034560",
            "sender_card_type": "FT/NEXP",
            "sender_card_number": "N/A",
            "sender_account": "DEAL002905",
            "nexuspay_id": "100NEXP26193M601",
            "amount": 300000.00,
            "transaction_date": "12-Jul-2026",
            "status": "SUCCESSFUL"
        },
        {
            "lid": "LID0199687412",
            "receiver_name": "MyOne Electronics Industries Ltd.",
            "receiver_bank": "Dutch-Bangla Bank PLC.",
            "receiver_account": "1041100034560",
            "sender_card_type": "FT/NEXP",
            "sender_card_number": "N/A",
            "sender_account": "DEAL002905",
            "nexuspay_id": "100NEXP26193M602",
            "amount": 300000.00,
            "transaction_date": "12-Jul-2026",
            "status": "SUCCESSFUL"
        }
    ]

    for tx in transactions_list:
        sync_transaction(tx)
        
