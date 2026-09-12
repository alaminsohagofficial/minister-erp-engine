import os
from weasyprint import HTML

def generate_legal_notice(dealer_code, amount_due):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="bn">
    <head><meta charset="UTF-8"><style>body{{font-family:Arial,sans-serif;margin:40px;}}h1{{color:red;}}</style></head>
    <body>
        <h1>অফিসিয়াল লিগ্যাল নোটিশ / Official Legal Notice</h1>
        <p>ডিলার কোড: <strong>{dealer_code}</strong></p>
        <p>বকেয়া পরিমাণ: ৳ <strong>{amount_due}</strong></p>
        <p>নির্ধারিত সময়ের মধ্যে বকেয়া পরিশোধ করার জন্য অনুরোধ করা যাচ্ছে। অন্যথায় আইনগত ব্যবস্থা নেওয়া হবে।</p>
    </body>
    </html>
    """
    output_path = f"legal_notice_{dealer_code}.pdf"
    HTML(string=html_content).write_pdf(output_path)
    return output_path
