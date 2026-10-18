import os
from datetime import datetime, timezone
from flask import Flask, jsonify
import requests

app = Flask(__name__)

# ১. এনভায়রনমেন্ট কনফিগারেশন এবং সিকিউরিটি টোকেন লোড করা
CORPORATE_ERP_WEBHOOK_URL = os.getenv(
    "ERP_WEBHOOK_URL", "https://erp.ministerbd.com/api/v1/dealer/receive-ledger"
)
DEALER_SECURE_TOKEN = os.getenv(
    "DEALER_SECURE_TOKEN", "DEAL002905_SECURE_TOKEN"
)

# ২. ডিলার এবং লেজার ডেটা মাস্টার পে-লোড (S.R. Electronics Park - DEAL002905)
MINISTER_LEDGER_PAYLOAD = {
    "account_title": "MyOne Electronics Industries Ltd.",
    "account_number": "3311901022846",  # সঠিক পূবালী ব্যাংক কর্পোরেট অ্যাকাউন্ট
    "dealer_id": "DEAL002905",
    "remitter_ref": "S. R. ELECTRONICS PARK (DEAL002905)",
    "statement_period": "18-OCT-2026",
    "total_credit_amount_bdt": 100050.00,
    "closing_balance_bdt": 100050.00,
    "clearing_bank": "Pubali Bank PLC",
    "audit_ref": "PUBALI-SYS-AUDIT/2026/21628",
    "transactions": [
        {
            "si_no": 1,
            "txn_date": "18-OCT-2026 02:40 AM",
            "txn_id": "2026101818-2-21628",
            "sap_lid": "LID02026101801",
            "particulars": (
                "FT/PUBALI/2026101818-2-21628/DEAL002905 (Pubali Merchant"
                " Payment)"
            ),
            "amount": 100050.00,
            "status": "SETTLED",
        }
    ],
}


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": "Minister & S.R. Electronics Park Secure Ledger Engine",
        "status": "ONLINE",
        "dealer_code": "DEAL002905",
        "endpoints": ["/api/minister/sync", "/api/minister/trigger-sync"],
    })


@app.route("/api/minister/sync", methods=["GET"])
def get_minister_sync():
    return jsonify({
        "status": "API PAYLOAD SYNCED",
        "dealer_code": "DEAL002905",
        "client": "MD. AL AMIN SOHAG",
        "audit_ref": "PUBALI-SYS-AUDIT/2026/21628",
        "data": MINISTER_LEDGER_PAYLOAD,
    })


@app.route("/api/minister/trigger-sync", methods=["POST"])
def trigger_corporate_sync():
    headers = {
        "Content-Type": "application/json",
        "X-Dealer-Authorization": f"Bearer {DEALER_SECURE_TOKEN}",
    }

    try:
        response = requests.post(
            CORPORATE_ERP_WEBHOOK_URL,
            json=MINISTER_LEDGER_PAYLOAD,
            headers=headers,
            timeout=15,
        )

        try:
            res_data = response.json()
        except Exception:
            res_data = response.text

        if response.status_code == 200:
            sync_result = {
                "status": "SUCCESS",
                "code": response.status_code,
                "response": res_data,
            }
        else:
            sync_result = {
                "status": "FAILED",
                "code": response.status_code,
                "error_response": res_data,
                "message": "Corporate ERP Webhook returned an error status.",
            }

    except requests.exceptions.RequestException as e:
        sync_result = {
            "status": "CONNECTION_FAILED",
            "error_detail": str(e),
            "message": "Failed to connect to Corporate ERP Webhook server.",
        }

    return jsonify({
        "engine_status": "PROCESSED",
        "dealer_id": "DEAL002905",
        "total_amount_hit": "100,050.00 BDT",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "corporate_hit_result": sync_result,
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
    
