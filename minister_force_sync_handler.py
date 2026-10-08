import os
import requests
from dotenv import load_dotenv

load_dotenv()


def force_sync_dealer(dealer_code, metric):
    # .env ফাইল থেকে DBBL_API_URL অথবা প্রোডাকশন এন্ডপয়েন্ট নেওয়া হচ্ছে
    endpoint = os.getenv(
        "FORCE_SYNC_ENDPOINT",
        os.getenv(
            "DBBL_API_URL",
            "https://api.dutchbanglabank.com/v1/settlement/verify",
        ),
    )
    headers = {
        "x-cryptographic-signature": os.getenv(
            "MASTER_BYPASS_TOKEN", ""
        ),
        "Content-Type": "application/json",
    }
    payload = {
        "dealer_code": dealer_code,
        "listed_primary_dealer": "DEAL002905",
        "financial_metrics": metric,
    }
    try:
        res = requests.post(
            endpoint, json=payload, headers=headers, timeout=10
        )
        return res.json()
    except Exception as e:
        return {"status": "error", "details": str(e)}
