from weasyprint import HTML

def generate_legal_notice_pdf():
    html_content = """
    <!DOCTYPE html>
    <html lang="bn">
    <head>
        <meta charset="UTF-8">
        <style>
            body { font-family: 'SolaimanLipi', Arial, sans-serif; margin: 40px; color: #111; line-height: 1.6; }
            h1 { text-align: center; color: #b71c1c; font-size: 24px; }
            h2 { font-size: 18px; border-bottom: 2px solid #333; padding-bottom: 5px; margin-top: 30px; }
            .meta { margin-bottom: 20px; font-weight: bold; }
            table { width: 100%; border-collapse: collapse; margin-top: 15px; }
            th, td { border: 1px solid #444; padding: 8px; text-align: left; font-size: 14px; }
            th { background-color: #f5f5f5; }
            .footer { margin-top: 50px; text-align: right; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>আইনি নোটিশ ও ব্যাংকিং অডিট দাবি</h1>
        <div class="meta">
            <p>প্রাপক: ব্যবস্থাপনা পরিচালক / হেড অব অ্যাকাউন্টস, MHPIL (erp.ministerbd.com)</p>
            <p>প্রেরক: প্রোপ্রাইটর, S.R. ELECTRONICS PARK (DEAL002905)</p>
            <p>তারিখ: September 9, 2026</p>
        </div>
        
        <h2>বিষয়: সিস্টেম সিঙ্ক্রোনাইজেশন ত্রুটির আড়ালে হয়রানি বন্ধ এবং BDT 35,189,545.00 টাকার পূর্ণ পেমেন্ট সেটেলমেন্ট প্রসঙ্গে।</h2>
        
        <p>অত্র নোটিশের মাধ্যমে স্পষ্টভাবে জানানো যাচ্ছে যে, আমাদের ডিলার অ্যাকাউন্ট (DEAL002905)-এর বিপরীতে সর্বমোট <strong>BDT 35,189,545.00</strong> টাকা অফিশিয়াল ব্যাংকিং চ্যানেল ও গুগল ইনওয়ার্ড রেমিট্যান্সের মাধ্যমে সম্পূর্ণ পরিশোধিত ও লেজার-লকড রয়েছে[span_14](start_span)[span_14](end_span)। আপনাদের সনাতন ইআরপি সিস্টেমের ম্যানুয়াল গরমিল বা ত্রুটির কারণে আমাদের অ্যাকাউন্ট ব্লক করার কোনো আইনি বা প্রযুক্তিগত ভিত্তি নেই।</p>
        
        <h2>ভেরিফাইড পেমেন্ট ট্রেইল সারসংক্ষেপ:</h2>
        <table>
            <tr>
                <th>মাধ্যম / গেটওয়ে</th>
                <th>রেফারেন্স / ডকুমেন্ট</th>
                <th>পরিমাণ (টাকা)</th>
                <th>স্ট্যাটাস</th>
            </tr>
            <tr>
                <td>Google Ireland Limited</td>
                <td>GIT-FIRC/2026/08-9999</td>
                <td>20,000,000.00</td>
                <td>SUCCESS[span_15](start_span)[span_15](end_span)</td>
            </tr>
            <tr>
                <td>Islami Bank Bangladesh (Banani)</td>
                <td>IBBL/BNN/FT/2026/0802-18 (#5100029481)</td>
                <td>13,269,545.00</td>
                <td>COMPLETED[span_16](start_span)[span_16](end_span)</td>
            </tr>
            <tr>
                <td>Dutch-Bangla Bank (NexusPay)</td>
                <td>Multiple Trace IDs (July 2026)</td>
                <td>1,920,000.00</td>
                <td>SETTLED[span_17](start_span)[span_17](end_span)</td>
            </tr>
        </table>
        
        <p>আগামী ২৪ ঘণ্টার মধ্যে আমাদের অ্যাকাউন্ট সম্পূর্ণ সচল না করলে এবং জয়েন্ট ব্যাংকিং অডিট মেনে না নিলে প্রচলিত আইন ও সাইবার-ফিন্যান্সিয়াল বিধান অনুযায়ী আপনাদের বিরুদ্ধে কঠোর আইনি পদক্ষেপ গ্রহণ করা হবে।</p>
        
        <div class="footer">
            <p>কর্তرপক্ষমতার সাথে,</p>
            <p>S.R. ELECTRONICS PARK</p>
        </div>
    </body>
    </html>
    """
    
    HTML(string=html_content).write_pdf("minister_dispute_legal_notice.pdf")
    print("Legal Notice PDF generated successfully.")

if __name__ == '__main__':
    generate_legal_notice_pdf()
  
