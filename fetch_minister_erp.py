import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv('MINISTER_ERP_API_URL', 'https://erp.ministerbd.com/api/v1/ledger')
API_KEY = os.getenv('MINISTER_ERP_API_KEY', '')

def fetch_dealer_ledger(dealer_code="DEAL002905"):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(f"{API_URL}/{dealer_code}", headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return {'error': f'HTTP Error: {response.status_code}'}
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    print(fetch_dealer_ledger())
