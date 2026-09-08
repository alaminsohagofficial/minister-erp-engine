import requests
import json

def fetch_minister_erp_ledger():
    # Target ERP endpoint for Dealer DEAL002905
    erp_url = "https://erp.ministerbd.com/api/v1/dealer/ledger"
    headers = {
        "Authorization": "Bearer TOKEN_OR_API_KEY",
        "Content-Type": "application/json"
    }
    payload = {
        "dealer_code": "DEAL002905",
        "query_type": "FULL_LEDGER_AUDIT"
    }
    
    try:
        response = requests.post(erp_url, json=payload, headers=headers, timeout=15)
        if response.status_code == 200:
            erp_data = response.json()
            print("Successfully fetched data from erp.ministerbd.com")
            # Compare with our verified pool BDT 35,189,545.00[span_3](start_span)[span_3](end_span)
            return erp_data
        else:
            print(f"ERP Error Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Connection to Minister ERP failed: {str(e)}")

if __name__ == '__main__':
    fetch_minister_erp_ledger()
  
