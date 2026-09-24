import os
from flask import Flask, render_template, send_file, request, jsonify
from weasyprint import HTML
from dotenv import load

load_dotenv()
app = Flask(__name__)

@app.route('/api/generate-pdf/<dealer_id>', methods=['GET'])
def generate_pdf(dealer_id):
    # Sample financial ledger data for WeasyPrint PDF Generation
    dealer_data = {
        "DEAL002905": {"name": "Minister High-Tech Park", "allocation": "BDT 35,189,545.00", "status": "RECONCILED"},
        "MDEL000215": {"name": "Salsabila Electronics Park", "allocation": "BDT 35,189,545.00", "status": "RECONCILED"}
    }
    
    info = dealer_data.get(dealer_id, {"name": "Unknown Dealer", "allocation": "BDT 0.00", "status": "PENDING"})

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: 'Helvetica', sans-serif; color: #333; margin: 40px; }}
            .header {{ text-align: center; border-bottom: 2px solid #0056b3; padding-bottom: 20px; }}
            .title {{ color: #0056b3; font-size: 24px; font-weight: bold; }}
            .details {{ margin-top: 30px; font-size: 16px; line-height: 1.6; }}
            .footer {{ margin-top: 50px; text-align: center; font-size: 12px; color: #777; }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="title">Minister ERP & Dual-Dealer Ledger Engine</div>
            <p>Official Financial Reconciliation & SAP Allocation Report</p>
        </div>
        <div class="details">
            <p><strong>Dealer ID:</strong> {dealer_id}</p>
            <p><strong>Dealer Name:</strong> {info['name']}</p>
            <p><strong>SAP Allocation Balance:</strong> {info['allocation']}</p>
            <p><strong>Reconciliation Status:</strong> {info['status']}</p>
            <p><strong>Security Bypass Protocol:</strong> SECURE-SEC-2026-ACTIVE</p>
        </div>
        <div class="footer">
            <p>Generated securely via WeasyPrint & Gemini AI Enterprise Bridge.</p>
        </div>
    </body>
    </html>
    """
    
    pdf_path = f"report_{dealer_id}.pdf"
    HTML(string=html_content).write_pdf(pdf_path)
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
