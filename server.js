require('dotenv').config();
const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const { GoogleGenAI } = require('@google/genai');

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

// ১. ডাটাবেজ সংযোগ
const db = new sqlite3.Database('./minister_main_system.db', (err) => {
    if (err) {
        console.error('❌ Database Connection Error:', err.message);
    } else {
        console.log('✅ Connected to SQLite database.');
    }
});

// ২. জেমিনী এআই কনফিগারেশন (Official @google/genai SDK)
const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY || '' });

// ৩. লাইভ ড্যাশবোর্ড / স্ট্যাটাস রুট
app.get('/', (req, res) => {
    res.send('⚡ Minister ERP & Logistics Live Webhook Server Running!');
});

app.get('/api/status', (req, res) => {
    res.status(200).json({
        status: 'active',
        system: 'Minister ERP Engine',
        dealer: 'DEAL002905',
        timestamp: new Date().toISOString()
    });
});

// ৪. রিয়েল-টাইম পেমেন্ট ওয়েবহুক এন্ডপয়েন্ট
app.post('/api/payment-webhook', async (req, res) => {
    const { txn_id, customer_code, amount, product_code, quantity } = req.body;

    if (!txn_id || !customer_code || !amount) {
        return res.status(400).json({ error: 'Missing required transaction fields' });
    }

    const amountPaid = parseFloat(amount);
    const qty = parseInt(quantity) || 1;

    db.serialize(() => {
        // ট্রানজেকশন শুরু
        db.run('BEGIN TRANSACTION');

        // ক) ব্যাংক অ্যাকাউন্টে টাকা যোগ
        db.run(
            `UPDATE bank_accounts SET balance = balance + ? WHERE account_name = 'DBBL_MERCHANT'`,
            [amountPaid]
        );

        // খ) ইনভেন্টরি থেকে স্টক মাইনাস
        db.run(
            `UPDATE warehouse_stock SET stock = stock - ? WHERE product_code = ?`,
            [qty, product_code]
        );

        // গ) কাস্টমার লেজার ব্যালেন্স চেক ও আপডেট
        db.get(
            `SELECT current_balance FROM customer_ledger WHERE customer_code = ? ORDER BY id DESC LIMIT 1`,
            [customer_code],
            async (err, row) => {
                if (err) {
                    db.run('ROLLBACK');
                    return res.status(500).json({ error: 'Database query error' });
                }

                const currentBal = row ? row.current_balance : 0;
                const newBalance = currentBal - amountPaid;
                const currentDate = new Date().toLocaleDateString('en-GB');

                db.run(
                    `INSERT INTO customer_ledger (customer_code, date, gl_voucher, ref_no, description, credit, current_balance)
                     VALUES (?, ?, ?, ?, ?, ?, ?)`,
                    [
                        customer_code,
                        currentDate,
                        txn_id,
                        txn_id,
                        'DBBL Gateway Payment Received',
                        amountPaid,
                        newBalance
                    ],
                    async (insertErr) => {
                        if (insertErr) {
                            db.run('ROLLBACK');
                            return res.status(500).json({ error: 'Ledger update failed' });
                        }

                        // সব সফল হলে কমিট
                        db.run('COMMIT');

                        // এআই নোটিফিকেশন এসএমএস
                        let aiMessage = `পেমেন্ট সফল! ৳${amountPaid} জমা হয়েছে। বর্তমান বকেয়া: ৳${newBalance}`;
                        try {
                            if (process.env.GEMINI_API_KEY) {
                                const prompt = `কাস্টমার ${customer_code} ৳${amountPaid} পরিশোধ করেছেন। বর্তমান বকেয়া ৳${newBalance}। মালামাল ছাড়ার জন্য ১ লাইনের সুন্দর বাংলা নোটিফিকেশন দাও।`;
                                const response = await ai.models.generateContent({
                                    model: 'gemini-2.5-flash',
                                    contents: prompt,
                                });
                                aiMessage = response.text;
                            }
                        } catch (e) {
                            console.log('AI SMS Fallback used:', e.message);
                        }

                        return res.status(200).json({
                            status: 'success',
                            message: 'Transaction synchronized successfully',
                            closing_balance: newBalance,
                            notification: aiMessage
                        });
                    }
                );
            }
        );
    });
});

app.listen(port, () => {
    console.log(`🚀 Server running on port ${port}`);
});
