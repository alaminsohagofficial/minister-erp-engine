import os
from flask import Flask, request, jsonify, render_template_string, send_file
from dotenv import load_dotenv
from weasyprint import HTML
from datetime import datetime

load_dotenv()

app = Flask(__name__)

# ইনভয়েস ও অফিশিয়াল লেজার পিডিএফ টেমপ্লেট (বাংলা ফন্ট সাপোর্টসহ)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <style>
        /* কালপুরুষ বা সোলাইমানলিপি লিনাক্স সার্ভারে না থাকলে যাতে ডিফল্ট বাংলা ফন্ট পায় */
        body { font-family: 'Kalpurush', 'SolaimanLipi', 'Noto Sans Bengali', Arial, sans-serif; margin: 40px; color: #333; }
        .header { text-align: center; border-bottom: 2px solid #0056b3; padding-bottom: 10px; margin-bottom: 20px; }
        .header h2 { color: #0056b3; margin: 0; font-size: 24px; }
        .header p { margin: 5px 0 0 0; color: #555; }
        .details { margin-bottom: 30px; font-size: 14px; }
        .details p { margin: 6px 0; }
        .details table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        .details th, .details td { border: 1px solid #ddd; padding: 10px; text-align: left; font-size: 14px; }
        .details th { background-color: #f4f6f9; color: #0056b3; }
        .footer { margin-top: 50px; text-align: right; font-size: 12px; color: #777; border-top: 1px dashed #ccc; padding-top: 10px; }
    </style>
</head>
<body>
    <div class="header">
        <h2>Minister Hi-Tech Park & Salsabilah Electronics</h2>
        <p>Dual-Dealer Financial Ledger & Reconciliation Engine</p>
    </div>
    
    <div class="details">
        <p><strong>Dealer Code / ID:</strong> {{ dealer_code }}</p>
        <p><strong>Linked Primary Dealer:</strong> {{ linked_primary_dealer }}</p>
        <p><strong>FIRC Reference:</strong> {{ firc_reference }}</p>
        <p><strong>Date:</strong> {{ date }}</p>

        <table>
            <tr>
                <th>Financial Metric</th>
                <th>Amount (BDT)</th>
            </tr>
            <tr>
                <td>Total Verified Pool</td>
                <td>৳ {{ total_verified_pool }}</td>
            </tr>
            <tr>
                <td>SAP S/4HANA Allocation</td>
                <td>৳ {{ sap_s4hana_allocation }}</td>
            </tr>
        </table>
    </div>

    <div class="footer">
        <p>System Generated Official Reconciliation Document via WeasyPrint Engine</p>
    </div>
</body>
</html>
"""

@app.route('/api/v1/generate-pdf', methods=['POST'])
def generate_pdf():
    # রিকোয়েস্ট বডি চেক করা
    data = request.get_json()

    if not data or 'dealer_code' not in data or 'financial_metrics' not in data:
        return jsonify({'error': 'Missing required payload parameters', 'required': ['dealer_code', 'financial_metrics']}), 400

    dealer_code = data.get('dealer_code')
    linked_primary_dealer = data.get('linked_primary_dealer', 'DEAL002905')
    firc_reference = data.get('firc_reference', os.getenv('FIRC_REFERENCE', 'GIT-FIRC/2026/08-9999'))
    metrics = data.get('financial_metrics', {})

    total_verified_pool = metrics.get('total_verified_pool', '0.00')
    sap_allocation = metrics.get('sap_s4hana_allocation', '0.00')

    # পাইথনের স্ট্যান্ডার্ড লাইব্রেরি দিয়ে সেফলি কারেন্ট ডেট ফরম্যাট করা
    current_date = datetime.now().strftime('%d/%m/%Y')

    # রেন্ডার করার জন্য ডেটা প্রস্তুত করা
    rendered_html = render_template_string(
        HTML_TEMPLATE,
        dealer_code=dealer_code,
        linked_primary_dealer=linked_primary_dealer,
        firc_reference=firc_reference,
        date=current_date,
        total_verified_pool=total_verified_pool,
        sap_s4hana_allocation=sap_allocation
    )

    pdf_filename = f"reconciliation_{dealer_code}.pdf"
    
    # ওএস পারমিশন সেফ রাখতে /tmp ফোল্ডার ব্যবহার করা (Render বা লিনাক্সে ডিরেক্ট রুটে ফাইল রাইট ব্লক থাকে)
    tmp_dir = '/tmp' if os.name != 'nt' else '.'
    pdf_path = os.path.join(tmp_dir, pdf_filename)

    try:
        # WeasyPrintEngine দিয়ে পিডিএফ তৈরি
        HTML(string=rendered_html).write_pdf(pdf_path)
    except Exception as e:
        return jsonify({
            'error': 'PDF generation failed', 
            'details': str(e),
            'hint': 'Ensure system dependencies like pango, cairo, and shared fonts are installed on your host.'
        }), 500

    # ফাইলটি ডাউনলোড শেষে মেমোরি থেকে রিলিজ করার জন্য সেফলি সেন্ড করা
    try:
        return send_file(pdf_path, as_attachment=True, download_name=pdf_filename, mimetype='application/pdf')
    except Exception as e:
        return jsonify({'error': 'Failed to send PDF file', 'details': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    # প্রোডাকশনে debug=False রাখা ভালো
    app.run(host='0.0.0.0', port=port, debug=False)
