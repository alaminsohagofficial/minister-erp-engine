import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv('SALSABILAH_ERP_API_URL', 'https://erp.salsabilah.com/api/v1/sync')
API_KEY = os.getenv('SALSABILAH_API_KEY', '')

def sync_salsabilah_erp(payload):
    headers = {
        'X-API-Key': API_KEY,
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=15)
        return response.json() if response.status_code == 200 else {'error': response.text}
    except Exception as e:
        return {'error': str(e)}
