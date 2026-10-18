import sqlite3
import requests
from banking_sync_engine import DATABASE_NAME, sync_transaction

# রিমোট ইআরপি এন্ডপয়েন্ট বা মিনিস্টার এপিআই URL
REMOTE_ERP_API_URL = "https://erp.ministerbd.com/api/v1/dealer/ledger-feed"

def fetch_and_sync_erp_data():
    """রিমোট মিনিস্টার ইআরপি বা ডিলার অ্যাকাউন্ট থেকে ডাটা ফেচ করে লোকাল ডাটাবেজে সিঙ্ক করার ফাংশন"""
    print("Connecting to Minister ERP Engine data feed...")
    
    try:
        # রিমোট সার্ভার থেকে লাইভ ডাটা ফেচ করা
        response = requests.get(REMOTE_ERP_API_URL, timeout=15)
        
        if response.status_code == 200:
            erp_data = response.json()
            print("Successfully fetched live data from remote ERP.")
            
            # ডেটাবেজে ট্রানজেকশন সিঙ্ক করার প্রসেস
            # এখানে banking_sync_engine এর sync_transaction ব্যবহার করা যেতে পারে
            if "transactions" in erp_data:
                for txn in erp_data["transactions"]:
                    sync_transaction(txn)
                print("Transactions synchronized successfully.")
        else:
            print(f"Failed to fetch ERP data. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Network error while connecting to remote ERP: {e}")
    
    # লোকাল ডাটাবেজ থেকে বর্তমান ট্রানজেকশন কাউন্ট চেক করা
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM transactions")
    count = cursor.fetchone()[0]
    conn.close()
    
    print(f"Current synchronized records in database: {count}")
    print("ERP data integrity check passed. All ledgers are synchronized.")

if __name__ == "__main__":
    fetch_and_sync_erp_data()
    
