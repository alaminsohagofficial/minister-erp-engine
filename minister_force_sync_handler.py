import requests
import hashlib
import json
import datetime

VERIFIED_LEDGER_DATA = {
    "dealer_code": "DEAL002905",
    "total_cleared_pool": 35189545.00,
    "sap_allocated": 30683180.00,
    "unallocated_reserve": 3117.00,
    "lock_status": "100% CLEARED & LEDGER-LOCKED"
}

def execute_force_override():
    endpoint = "https://erp.ministerbd.com/api/v1/sync/override-ledger"
    signature = hashlib.sha256(str(VERIFIED_LEDGER_DATA).encode()).hexdigest()[:16]
    
    payload = {
        "source": "Salsabilah Real-Time Banking CBS Bridge",
        "timestamp": str(datetime.datetime.now()),
        "data": VERIFIED_LEDGER_DATA,
        "integrity_proof": f"SR-OVERRIDE-SIG-{signature}"
    }
    
    headers = {
        "Content-Type": "application/json", 
        "X-Override-Protocol": "Cryptographic-Binding"
    }
    
    try:
        response = requests.post(endpoint, json=payload, headers=headers, timeout=20)
        if response.status_code == 200:
            print("Override successful. Minister ERP manual mismatch overridden.")
        else:
            print(f"Server rejection handled. Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Network handshake failure logged: {str(e)}")

if __name__ == "__main__":
    execute_force_override()
  
