import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai

# পরিবেশের ভ্যারিয়েবল লোড করা
load_dotenv()

app = Flask(__name__)

# জেমিনি এআই কনফিগারেশন
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

@app.route('/')
def home():
    return "Minister ERP Engine is running successfully with Gemini AI!"

@app.route('/generate-ai-notice', methods=['POST'])
def generate_ai_notice():
    try:
        data = request.json
        prompt = data.get("prompt", "Provide an ERP system update notification.")
        
        # জেমিনি মডেল ইনিশিয়ালাইজ করা (Gemini 1.5 Flash ব্যবহার করা হচ্ছে)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        
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
    
