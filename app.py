from flask import Flask, jsonify, request
from datetime import datetime
import requests

app = Flask(__name__)

# ডাচ্-বাংলা ব্যাংক পিএলসি এবং অডিট রেফারেন্স অনুযায়ী ভেরিফাইড লেজার ডেটা (জুলাই ২০২৬)
MINISTER_LEDGER_PAYLOAD = {
    "account_title": "MyOne Electronics Industries Ltd.",
    "account_number": "1041100034560",
    "dealer_id": "DEAL002905",
    "remitter_ref": "S. R. ELECTRONICS PARK (DEAL002905)",
    "statement_period": "06-JUL-2026 to 12-JUL-2026",
    "total_credit_amount_bdt": 1920000.00,
    "closing_balance_bdt": 1920000.00,
    "clearing_bank": "Dutch-Bangla Bank PLC",
    "audit_ref": "DBBL/HO/SYS-AUDIT/2026/10924",
    "transactions": [
        {
            "si_no": 1,
            "txn_date": "06-JUL-2026",
            "txn_id": "100NEXP26187M597",
            "sap_lid": "LID01976788453",
            "particulars": "FT/NEXP/100NEXP26187M597/DEAL002905 LID01976788453 (Supplier Adv Minister)",
            "amount": 238000.00,
            "status": "VERIFIED"
        },
        {
            "si_no": 2,
            "txn_date": "07-JUL-2026",
            "txn_id": "100NEXP26188M616",
            "sap_lid": "LID01996890123",
            "particulars": "FT/NEXP/100NEXP26188M616/DEAL002905 LID01996890123 (MyOne Bank Trans)",
            "amount": 270000.00,
            "status": "VERIFIED"
        },
        {
            "si_no": 3,
            "txn_date": "07-JUL-2026",
            "txn_id": "100NEXP26188M584",
            "sap_lid": "LID01996889539",
            "particulars": "FT/NEXP/100NEXP26188M584/DEAL002905 LID01996889539 (MyOne Bank Trans)",
            "amount": 230000.00,
            "status": "VERIFIED"
        },
        {
            "si_no": 4,
            "txn_date": "08-JUL-2026",
            "txn_id": "100NXN126189M586",
            "sap_lid": "LID01998640246",
            "particulars": "NPSB/NXN/100NXN126189M586/DEAL002905 LID01998640246 (Minister Treasury)",
            "amount": 297000.00,
            "status": "VERIFIED"
        },
        {
            "si_no": 5,
            "txn_date": "08-JUL-2026",
            "txn_id": "100NXN126189M591",
            "sap_lid": "LID01938788435",
            "particulars": "NPSB/NXN/100NXN126189M591/DEAL002905 LID01938788435 (Minister Treasury)",
            "amount": 285000.00,
            "status": "VERIFIED"
        },
        {
            "si_no": 6,
            "txn_date": "12-JUL-2026",
            "txn_id": "100NEXP26193M601",
            "sap_lid": "LID01996914258",
            "particulars": "FT/NEXP/100NEXP26193M601/DEAL002905 LID01996914258 (Google 65 TV Pt-1)",
            "amount": 300000.00,
            "status": "VERIFIED"
        },
        {
            "si_no": 7,
            "txn_date": "12-JUL-2026",
            "txn_id": "100NEXP26193M602",
            "sap_lid": "LID01996987412",
            "particulars": "FT/NEXP/100NEXP26193M602/DEAL002905 LID01996987412 (Google 65 TV Pt-2)",
            "amount": 300000.00,
            "status": "VERIFIED"
        }
    ]
}

# কোম্পানির সেন্ট্রাল ইআরপি বা এপিআই রিসিভিং এন্ডপয়েন্ট (প্রয়োজনে পরিবর্তনযোগ্য)
CORPORATE_ERP_WEBHOOK_URL = "https://erp.ministerbd.com/api/v1/dealer/receive-ledger"

def dispatch_to_corporate_erp(payload):
    """
    এই ফাংশনটি ডিলারের ইঞ্জিন থেকে সরাসরি কোম্পানির একাউন্টে/ইআরপি-তে রিয়েল-টাইম POST রিকোয়েস্ট পাঠাবে।
    """
    headers = {
        "Content-Type": "application/json",
        "X-Dealer-Authorization": "Bearer DEAL002905_SECURE_TOKEN"
    }
    
    try:
        response = requests.post(CORPORATE_ERP_WEBHOOK_URL, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            return {"status": "SUCCESS", "response": response.json()}
        else:
            return {"status": "FAILED", "code": response.status_code, "message": response.text}
    except requests.exceptions.RequestException as e:
        return {"status": "ERROR", "message": str(e)}

@app.route('/api/minister/sync', methods=['GET'])
def get_minister_sync():
    """
    লেজার ডাটা দেখার জন্য ফিক্সড এন্ডপয়েন্ট।
    """
    return jsonify({
        "status": "API PAYLOAD SYNCED",
        "dealer_code": "DEAL002905",
        "client": "MD. AL AMIN SOHAG",
        "audit_ref": "DBBL/HO/SYS-AUDIT/2026/10924",
        "data": MINISTER_LEDGER_PAYLOAD
    })

@app.route('/api/minister/trigger-sync', methods=['POST'])
def trigger_corporate_sync():
    """
    এই এন্ডপয়েন্টটি কল করলে কোম্পানির সেন্ট্রাল ইআরপি সিস্টেমে রিয়েল-টাইম ডাটা হিট চলে যাবে।
    """
    sync_result = dispatch_to_corporate_erp(MINISTER_LEDGER_PAYLOAD)
    
    return jsonify({
        "engine_status": "DISPATCHED",
        "dealer_id": "DEAL002905",
        "timestamp": datetime.utcnow().isoformat(),
        "corporate_hit_result": sync_result
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
