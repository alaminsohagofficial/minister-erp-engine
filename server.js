const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const { GoogleGenAI } = require('@google/genai');
const path = require('path');
require('dotenv').config();

const app = express();
app.use(express.json());
app.use(express.static(path.join(__dirname)));

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

// Database Setup (SQLite)
const db = new sqlite3.Database('./erp_ledger.db', (err) => {
    if (err) console.error('Database connection error:', err.message);
    else console.log('Connected to SQLite database.');
});

db.serialize(() => {
    db.run(`CREATE TABLE IF NOT EXISTS ledgers (
        dealer_id TEXT PRIMARY KEY,
        dealer_name TEXT,
        sap_allocation REAL,
        current_balance REAL,
        status TEXT
    )`);

    // Seed initial data for the dual dealers
    db.run(`INSERT OR IGNORE INTO ledgers VALUES 
        ('DEAL002905', 'Minister High-Tech Park', 35189545.00, 35189545.00, 'ACTIVE'),
        ('MDEL000215', 'Salsabila Electronics Park', 35189545.00, 35189545.00, 'ACTIVE')
    `);
});

// API: Get Ledger Data
app.get('/api/ledger/:dealerId', (req, res) => {
    const { dealerId } = req.params;
    db.get(`SELECT * FROM ledgers WHERE dealer_id = ?`, [dealerId], (err, row) => {
        if (err) return res.status(500).json({ error: err.message });
        if (!row) return res.status(404).json({ error: 'Dealer not found' });
        res.json(row);
    });
});

// API: Process Secure Bypass & Payment
app.post('/api/bypass-transaction', async (req, res) => {
    const { dealer_id, amount, transaction_type } = req.body;

    db.serialize(async () => {
        db.run('BEGIN TRANSACTION');

        db.get(`SELECT * FROM ledgers WHERE dealer_id = ?`, [dealer_id], async (err, dealer) => {
            if (err || !dealer) {
                db.run('ROLLBACK');
                return res.status(400).json({ error: 'Invalid dealer or transaction failed.' });
            }

            let newBalance = dealer.current_balance;
            if (transaction_type === 'CREDIT') newBalance += parseFloat(amount);
            else if (transaction_type === 'DEBIT') newBalance -= parseFloat(amount);

            db.run(`UPDATE ledgers SET current_balance = ? WHERE dealer_id = ?`, [newBalance, dealer_id], async (updateErr) => {
                if (updateErr) {
                    db.run('ROLLBACK');
                    return res.status(500).json({ error: updateErr.message });
                }

                db.run('COMMIT', async () => {
                    // Generate Gemini AI Bengali Notification
                    try {
                        const prompt = `ডিলার ${dealer.dealer_name} (${dealer_id})-এর একটি সফল লেনদেন সম্পন্ন হয়েছে। টাকার পরিমাণ: BDT ${amount}. নতুন লেজার ব্যালেন্স: BDT ${newBalance}. এই তথ্যের ওপর ভিত্তি করে ১ লাইনের একটি পেশাদার এবং শুভেচ্ছা মূলক বাংলা এসএমএস নোটিফিকেশন তৈরি করুন।`;
                        
                        const response = await ai.models.generateContent({
                            model: 'gemini-2.5-flash',
                            contents: prompt,
                        });

                        res.json({
                            success: true,
                            message: 'Transaction reconciled successfully via Secure Bypass.',
                            dealer_id,
                            updated_balance: newBalance,
                            ai_notification: response.text
                        });
                    } catch (aiErr) {
                        res.json({
                            success: true,
                            message: 'Transaction reconciled, but AI notification failed.',
                            dealer_id,
                            updated_balance: newBalance,
                            ai_notification: 'সফলভাবে লেনদেন সম্পন্ন হয়েছে।'
                        });
                    }
                });
            });
        });
    });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`ERP Engine running on port ${PORT}`));
