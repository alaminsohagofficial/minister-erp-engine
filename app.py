import os
from flask import Flask, render_template, request, jsonify
from dotenv import load

load()

app = Flask(__name__)

# Mock Database / Live Memory State for Minister & MyOne ERP Sync
live_erp_database = {
    "dealerCode": "DEAL002905",
    "entity": "Minister Hi-Tech Park & MyOne Electronics",
    "surplusBalance": 330563297.00,
    "sapStatus": "DZ Cleared & Fully Reconciled",
    "lastSync": "2026-09-08 14:38:03"
}

@app.route('/')
def home():
    return render_template('index.html') if os.path.exists('templates/index.html') else "Minister ERP Real-Time Sync Engine is active."

@app.route('/api/live-sync', methods=['GET'])
def get_live_sync():
    """Fetches real-time ledger balance and SAP status for ministerbd.com & myonebd.com"""
    try:
        # Here you can also plug in direct database queries or external API fetching
        return jsonify({
            "success": True,
            "data": live_erp_database
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/update-ledger', methods=['POST'])
def update_ledger():
    """Real-time webhook listener for incoming banking transactions or inventory dispatch"""
    req_data = request.json
    if req_data:
        live_erp_database["surplusBalance"] = req_data.get("balance", live_erp_database["surplusBalance"])
        live_erp_database["sapStatus"] = req_data.get("status", live_erp_database["sapStatus"])
        live_erp_database["lastSync"] = req_data.get("timestamp", "Just now")
        
        return jsonify({
            "success": True,
            "message": "Real-time ledger synchronized successfully with ERP.",
            "updatedData": live_erp_database
        })
    return jsonify({"success": False, "message": "Invalid payload"}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    
