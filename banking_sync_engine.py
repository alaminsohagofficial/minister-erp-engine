import os
import requests
from dotenv import load_dotenv

# এনভায়রনমেন্ট ভেরিয়েবল লোড করা
load_dotenv()

API_URL = os.getenv('SALSABILAH_ERP_API_URL', 'https://erp.salsabilah.com/api/v1/sync')
API_KEY = os.getenv('SALSABILAH_API_KEY', '')

def load_datanov():
    # ডেটা সোর্স থেকে পে-লোড ডেটা লোড বা তৈরি করার লজিক
    # আপনার রিকুইরমেন্ট অনুযায়ী এখানে ডেটা রিটার্ন করবে
    payload = {
        # উদাহরণের জন্য একটি বেসিক স্ট্রাকচার, আপনার আসল ডেটা এখানে বসবে
        "transaction_id": "TXN_SAMPLE_001",
        "amount": 0.00
    }
    return payload

def sync_salsabilah_erp(payload):
    headers = {
        'X-API-Key': API_KEY,
        'Content-Type': 'application/json'
    }
    try:
        # এপিআই রিকোয়েস্ট পাঠানো
        response = requests.post(API_URL, json=payload, headers=headers, timeout=15)
        
        # ডিবাগিংয়ের জন্য সার্ভারের স্ট্যাটাস কোড এবং রেসপন্স কনসোলে প্রিন্ট করা
        print(f"--- API Request Log ---")
        print(f"URL: {API_URL}")
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
        print(f"-----------------------")
        
        if response.status_code == 200:
            try:
                return response.json()
            except ValueError:
                return {'success': True, 'raw_response': response.text}
        else:
            return {'error': f"Server returned status {response.status_code}: {response.text}"}
            
    except Exception as e:
        print(f"Connection Error: {str(e)}")
        return {'error': str(e)}

if __name__ == "__main__":
    print("Starting Salsabilah ERP Sync Engine...")
    
    # ডেটা লোড করা
    payload_data = load_datanov()
    
    if payload_data:
        # সিঙ্ক ফাংশন কল করা
        result = sync_salsabilah_erp(payload_data)
        print("Sync Result:", result)
    else:
        print("No payload data found to sync.")
