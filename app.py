import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai

# পরিবেশের ভ্যারিয়েবল লোড করা
load_dotenv()

app = Flask(__name__)

# জেমিনি এআই কনফিগারেশন
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

@app.route('/')
def home():
    return "Minister ERP Engine is running successfully with Gemini AI!"

@app.route('/dealer-ledger/<dealer_id>', methods=['GET'])
def get_dealer_ledger(dealer_id):
    try:
        # ডিলার আইডি চেক করা
        if dealer_id == "DEAL002905":
            ledger_data = {
                "dealer_id": "DEAL002905",
                "dealer_name": "Minister Dealer Point",
                "current_balance": "১২,৫০০ টাকা বকেয়া",
                "last_transaction": "৫,০০০ টাকা জমা",
                "status": "Active"
            }
        else:
            return jsonify({"status": "error", "message": "Dealer not found"}), 404

        # জেমিনি এআই দিয়ে রিয়েল-টাইম ডেটার প্রফেশনাল সামারি তৈরি করা
        prompt = f"""
        Below is the real-time ledger data for Dealer ID {ledger_data['dealer_id']} ({ledger_data['dealer_name']}):
        - Current Balance: {ledger_data['current_balance']}
        - Last Transaction: {ledger_data['last_transaction']}
        - Status: {ledger_data['status']}
        
        Please provide a professional, concise summary of this dealer's financial status in Bengali.
        """

        # আপডেট করা জেমিনি ক্লায়েন্ট কল পদ্ধতি
        client = genai.GenerativeModel('gemini-1.5-flash')
        ai_response = client.generate_content(prompt)

        return jsonify({
            "status": "success",
            "dealer_data": ledger_data,
            "ai_summary": ai_response.text
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/generate-ai-notice', methods=['POST'])
def generate_ai_notice():
    try:
        data = request.json
        prompt = data.get("prompt", "Provide an ERP system update notification.")
        
        client = genai.GenerativeModel('gemini-1.5-flash')
        response = client.generate_content(prompt)
        
        return jsonify({
            "status": "success",
            "ai_response": response.text
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
