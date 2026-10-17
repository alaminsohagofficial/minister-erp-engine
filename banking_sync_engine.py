from datetime import datetime
import os
import requests
from dotenv import load_dotenv

# এনভায়রনমেন্ট ভেরিয়েবল লোড করা
load_dotenv()

CORPORATE_ERP_WEBHOOK_URL = os.getenv(
    "ERP_WEBHOOK_URL", "https://erp.ministerbd.com/api/v1/dealer/receive-ledger"
)
DEALER_SECURE_TOKEN = os.getenv(
    "DEALER_SECURE_TOKEN", "DEAL002905_SECURE_TOKEN"
)

# রসিদ এবং সঠিক তথ্য অনুযায়ী ভেরিফাইড লেজার পে-লোড
BANK_SYNC_CONTROLLER_PAYLOAD = {
    "account_title": "Minister Electronics (Pubali Bank Merchant)",
    "account_number": "3311901022846",  # সঠিক রিসিভার অ্যাকাউন্ট
    "dealer_id": "DEAL002905",
    "remitter_ref": "S. R. ELECTRONICS PARK (DEAL002905)",
    "sender_account": "437*******008",
    "statement_period": "18-OCT-2026",
    "total_credit_amount_bdt": 100050.00,  # সঠিক ট্রানজেকশন অ্যামাউন্ট
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


def execute_bank_sync_controller():
  headers = {
      "Content-Type": "application/json",
      "X-Dealer-Authorization": f"Bearer {DEALER_SECURE_TOKEN}",
  }

  print("Executing Bank Sync Controller -> Connecting to Corporate ERP...")
  print(f"Target URL: {CORPORATE_ERP_WEBHOOK_URL}")

  try:
    response = requests.post(
        CORPORATE_ERP_WEBHOOK_URL,
        json=BANK_SYNC_CONTROLLER_PAYLOAD,
        headers=headers,
        timeout=15,
    )

    try:
      res_data = response.json()
    except Exception:
      res_data = response.text

    if response.status_code == 200:
      print("--- Bank Sync Controller: Success ---")
      return {
          "status": "SUCCESS",
          "code": response.status_code,
          "response": res_data,
      }
    else:
      print(f"--- Bank Sync Controller: Failed [{response.status_code}] ---")
      return {
          "status": "FAILED",
          "code": response.status_code,
          "error_response": res_data,
      }

  except requests.exceptions.RequestException as e:
    print(f"Connection Error: {str(e)}")
    return {"status": "CONNECTION_FAILED", "error_detail": str(e)}


if __name__ == "__main__":
  print("Starting Bank_sync_controller.py execution...")
  result = execute_bank_sync_controller()
  print("Controller Execution Result:", result)
    
