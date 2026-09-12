import os
import requests
from dotenv import load_dotenv

load_dotenv()

def force_sync_dealer(dealer_code, metrics):
    endpoint = os.getenv('FORCE_SYNC_ENDPOINT', 'http://localhost:3000/api/v1/sync/override-ledger')
    headers = {
        'x-cryptographic-signature': os.getenv('MASTER_BYPASS_TOKEN', ''),
        'Content-Type': 'application/json'
    }
    payload = {
        'dealer_code': dealer_code,
        'linked_primary_dealer': 'DEAL002905',
        'firc_reference': os.getenv('FIRC_REFERENCE', 'GIT-FIRC/2026/08-9999'),
        'financial_metrics': metrics
    }
    try:
        res = requests.post(endpoint, json=payload, headers=headers, timeout=10)
        return res.json()
    except Exception as e:
        return {'status': 'error', 'details': str(e)}
