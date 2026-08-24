# ⚡ Minister ERP Real-Time Sync & AI Notification Engine

একটি প্রোডাকশন-রেডি সিঙ্গেল-ফাইল পাইথন আর্কিটেকচার, যা পেমেন্ট গেটওয়ে নোটিফিকেশন পাওয়ার সাথে সাথে ব্যাংক অ্যাকাউন্ট, ওয়্যারহাউজ ইনভেন্টরি এবং কাস্টমার লেজার ব্যালেন্স রিয়েল-টাইমে সিনক্রোনাইজ করে[span_0](start_span)[span_0](end_span)। এছাড়া জেমিনী এআই (Gemini API) দিয়ে তাৎক্ষণিক ডায়নামিক বাংলা নোটিফিকেশন তৈরি এবং উইজপ্রিন্ট (WeasyPrint) ইঞ্জিনের সাহায্যে অফিসিয়াল ৩টি ডকুমেন্ট (PDF) প্রস্তুত করে[span_1](start_span)[span_1](end_span)।

---

## 🌟 মূল ফিচারসমূহ (Key Features)

- **ACID ডাটাবেজ ট্রানজেকশন:** পেমেন্ট আসার সাথে সাথে ডাটাবেজ রোলব্যাক (`conn.rollback()`) সুরক্ষা সহ ব্যাংক ব্যালেন্স বৃদ্ধি, স্টক হ্রাস এবং কাস্টমার লেজার আপডেট নিশ্চিত করে[span_2](start_span)[span_2](end_span)।
- **জেমিনী এআই (Gemini AI) নোটিফিকেশন:** লেনদেন ও বকেয়া ব্যালেন্সের ওপর ভিত্তি করে রিয়েল-টাইমে পেশাদার বাংলা এসএমএস জেনারেট করে[span_3](start_span)[span_3](end_span)।
- **উইজপ্রিন্ট (WeasyPrint) পিডিএফ ইঞ্জিন:** স্বয়ংক্রিয়ভাবে ৩টি অফিশিয়াল ডকুমেন্ট তৈরি করে[span_4](start_span)[span_4](end_span):
  1. `Output_Customer_Invoice.pdf`: প্রফেশনাল A4 সাইজ কাস্টমার ইনভয়েস[span_5](start_span)[span_5](end_span)[span_6](start_span)[span_6](end_span)।
  2. `Output_NexusPay_Slip.pdf`: ডাচ-বাংলা ব্যাংক Nexus-Pro থিমড POS পেমেন্ট স্লিপ[span_7](start_span)[span_7](end_span)[span_8](start_span)[span_8](end_span)।
  3. `Output_Statement_Of_Account.pdf`: A4 Landscape ফরম্যাটে সম্পূর্ণ কাস্টমার খতিয়ান বা স্টেটমেন্ট[span_9](start_span)[span_9](end_span)[span_10](start_span)[span_10](end_span)।
- **সিকিউর কনফিগারেশন:** `.env` ফাইলের মাধ্যমে API Key এবং কনফিগারেশন সুরক্ষিত রাখা[span_11](start_span)[span_11](end_span)।

---

## 🛠️ টেক স্ট্যাক (Tech Stack)

- **Language:** Python 3.9+[span_12](start_span)[span_12](end_span)
- **Database:** SQLite3 (Embedded ACID Engine)[span_13](start_span)[span_13](end_span)
- **AI Integration:** Google Generative AI (Gemini 1.5 Flash / Gemini Pro)[span_14](start_span)[span_14](end_span)
- **PDF Engine:** WeasyPrint (HTML/CSS to PDF)[span_15](start_span)[span_15](end_span)
- **Environment:** python-dotenv[span_16](start_span)[span_16](end_span)

---

## 📁 প্রজেক্ট স্ট্রাকচার (Repository Structure)

```text
├── app.py                         # মূল পাইথন সোর্স কোড
├── .env.example                   # এনভায়রনমেন্ট ভ্যারিয়েবল টেমপ্লেট
├── .gitignore                     # গিট ইগনোর ফাইল
├── requirements.txt               # ডিপেন্ডেন্সি লিস্ট
└── README.md                      # ডকুমেন্টেশন
