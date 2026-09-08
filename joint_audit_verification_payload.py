import requests
import json

def push_audit_payload():
    payload = {
        "dealer_code": "DEAL002905",
        "dealer_name": "S.R. ELECTRONICS PARK",
        "beneficiary_account": "20503910100020103",
        "total_verified_pool_bdt": 35189545.00,
        "sync_action": "FORCE_UNCOMPROMISING_RECONCILIATION",
        "demand": "Acknowledge full payment and cease manual ERP harassment immediately."
    }

    target_url = "https://erp.ministerbd.com/api/v1/sync/verify-ledger"
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(target_url, data=json.dumps(payload), headers=headers, timeout=15)
        print(f"Status Code: {response.status_code}")
        print(f"Server Response: {response.text}")
    except Exception as e:
        print(f"API Synchronization Handshake Error Logged: {str(e)}")

if __name__ == '__main__':
    push_audit_payload()
  
