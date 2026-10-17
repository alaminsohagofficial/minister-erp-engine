import hashlib
import hmac
import json
import logging
from datetime import datetime

# Configure logging for audit trails
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PubaliMerchantVerifier:
    def __init__(self, merchant_id: str, terminal_id: str, api_secret: str):
        self.merchant_id = merchant_id
        self.terminal_id = terminal_id
        self.api_secret = api_secret.encode('utf-8')

    def verify_transaction_payload(self, webhook_data: dict, slip_details: dict) -> bool:
        """
        Verifies and reconciles incoming Pubali Bank PI Banking transactions 
        against generated payment slips for SR Electronics Park.
        """
        try:
            # 1. Extract and Validate Basic Parameters
            tx_id = webhook_data.get("transaction_reference_number")
            sender_acc = webhook_data.get("sender_account")
            receiver_acc = webhook_data.get("receiver_account")
            amount = float(webhook_data.get("transfer_amount", 0.0))
            status = webhook_data.get("transaction_status", "").upper()

            logging.info(f"Processing verification for Transaction ID: {tx_id}")

            # 2. Status Check
            if status != "SUCCESSFUL":
                logging.warning(f"Transaction {tx_id} failed or is pending status: {status}")
                return False

            # 3. Cross-Check with Slip Details
            if slip_details.get("transaction_id") != tx_id:
                logging.error("Transaction ID mismatch between slip and bank record.")
                return False

            if float(slip_details.get("amount", 0.0)) != amount:
                logging.error(f"Amount mismatch! Slip: {slip_details.get('amount')} vs Bank: {amount}")
                return False

            # 4. Receiver Account Validation for SR Electronics Park Merchant ID
            expected_receiver = "3311901022846"
            if receiver_acc != expected_receiver:
                logging.error(f"Invalid receiver account: {receiver_acc}. Expected merchant account.")
                return False

            logging.info(f"Transaction {tx_id} successfully verified and reconciled without any discrepancies.")
            return True

        except Exception as e:
            logging.critical(f"Critical error during transaction verification: {str(e)}")
            return False

# Example usage for testing or integration
if __name__ == "__main__":
    verifier = PubaliMerchantVerifier(
        merchant_id="474370027951000",
        terminal_id="PBL0000020041595",
        api_secret="SR_ELECTRONICS_PARK_SECURE_KEY"
    )

    sample_webhook = {
        "transaction_reference_number": "2026101818-2-21628",
        "sender_account": "*********7008",
        "receiver_account": "3311901022846",
        "transfer_amount": 10050.00,
        "transaction_status": "SUCCESSFUL"
    }

    sample_slip = {
        "transaction_id": "2026101818-2-21628",
        "amount": 10050.00
    }

    is_valid = verifier.verify_transaction_payload(sample_webhook, sample_slip)
    print(f"Verification Status: {is_valid}")
    
