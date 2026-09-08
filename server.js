require('dotenv').config();
const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const { GoogleGenAI } = require('@google/genai');

const app = express();
app.use(express.json());

const port = process.env.PORT || 3000;
const db = new sqlite3.Database(process.env.DB_NAME || 'minister_main_system.db');
const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

// পেমেন্ট ওয়েবহুক রুট
app.post('/api/v1/payment/webhook', (req, res) => {
    const { customer_code, amountPaid, txn_id } = req.body;

    if (!customer_code || !amountPaid) {
        return res.status(400).json({ error: 'Missing required payment parameters' });
    }

    db.serialize(() => {
        db.run('BEGIN TRANSACTION');

        db.get(`SELECT current_balance FROM customer_ledger WHERE customer_code = ? ORDER BY id DESC LIMIT 1`, [customer_code], (err, row) => {
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

                    db.run('COMMIT');

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
        });
    });
});

// ডুয়েল ডিলার বাইপাস এবং লেজার ওভাররাইড রুট (DEAL002905 & MDEL000215)
app.post('/api/v1/sync/override-ledger', (req, res) => {
    const { dealer_code, linked_primary_dealer, firc_reference, financial_metrics } = req.body;
    const signature = req.headers['x-cryptographic-signature'];

    if (!dealer_code || !financial_metrics) {
        return res.status(400).json({ error: 'Missing required override parameters' });
    }

    if (dealer_code !== 'DEAL002905' && dealer_code !== 'MDEL000215') {
        return res.status(403).json({ error: 'Unauthorized dealer code bypass attempt' });
    }

    db.serialize(() => {
        db.run('BEGIN TRANSACTION');

        db.run(
            `INSERT INTO customer_ledger (customer_code, date, gl_voucher, ref_no, description, credit, current_balance)
             VALUES (?, ?, ?, ?, ?, ?, ?)`,
            [
                dealer_code,
                new Date().toLocaleDateString('en-GB'),
                firc_reference || process.env.FIRC_REFERENCE || 'GIT-FIRC/2026/08-9999',
                linked_primary_dealer || 'DEAL002905',
                `Force Reconciled Pool via ${dealer_code} (FIRC: ${firc_reference})`,
                financial_metrics.total_verified_pool,
                financial_metrics.sap_s4hana_allocation
            ],
            (err) => {
                if (err) {
                    db.run('ROLLBACK');
                    return res.status(500).json({ error: 'Bypass ledger synchronization failed', details: err.message });
                }

                db.run('COMMIT');

                return res.status(200).json({
                    status: 'success',
                    message: `Ledger successfully overridden and synchronized via ${dealer_code}`,
                    verified_pool: financial_metrics.total_verified_pool,
                    sap_allocation: financial_metrics.sap_s4hana_allocation,
                    timestamp: new Date().toISOString()
                });
            }
        );
    });
});

app.listen(port, () => {
    console.log(`🚀 Server running on port ${port}`);
});
