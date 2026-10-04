from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# মিনিস্টার হাই-টেক পার্কের ভেরিফাইড ট্রানজেকশন ডেটা ও JSON পেলোড
MINISTER_LEDGER_PAYLOAD = {
    "dealer_id": "DEAL002905",
    "client_name": "SR Electronics Park",
    "total_disputed_pool_bdt": 1920000.00,
    "clearing_bank": "Dutch-Bangla Bank PLC",
    "settlement_node": "Bangladesh Bank NPSB Switch",
    "payload_generation_timestamp": "2026-07-15T06:00:00Z",
    "transactions": [
        {"date": "2026-07-06", "txn_id": "100NEXP26187M597", "sap_lid": "LID01976788453", "amount": 238000.00, "status": "SUCCESS"},
        {"date": "2026-07-07", "txn_id": "100NEXP26188M616", "sap_lid": "LID01996890123", "amount": 270000.00, "status": "SUCCESS"},
        {"date": "2026-07-07", "txn_id": "100NEXP26188M584", "sap_lid": "LID01996889539", "amount": 230000.00, "status": "SUCCESS"},
        {"date": "2026-07-08", "txn_id": "100NXN126189M586", "sap_lid": "LID01998640246", "amount": 297000.00, "status": "SUCCESS"},
        {"date": "2026-07-08", "txn_id": "100NXN126189M591", "sap_lid": "LID01938788435", "amount": 285000.00, "status": "SUCCESS"},
        {"date": "2026-07-12", "txn_id": "100NEXP26193M601", "sap_lid": "LID01996914258", "amount": 300000.00, "status": "SUCCESS"},
        {"date": "2026-07-12", "txn_id": "100NEXP26193M602", "sap_lid": "LID01996987412", "amount": 300000.00, "status": "SUCCESS"}
    ]
}

@app.route('/api/minister/sync', methods=['GET'])
def get_minister_sync():
    return jsonify({
        "status": "API PAYLOAD READY",
        "dealer_code": "DEAL002905",
        "client": "MD. AL AMIN SOHAG",
        "data": MINISTER_LEDGER_PAYLOAD
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
