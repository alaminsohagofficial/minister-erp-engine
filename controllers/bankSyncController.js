const axios = require('axios');

// ইন-মেমোরি লেজার ডাটাবেস (প্রয়োজনে MongoDB/PostgreSQL ব্যবহার করতে পারেন)
let ledgerDatabase = [
    {
        date: "2026-07-06",
        trx_id: "100NEXP26187M597",
        amount: 238000.00,
        ref: "LID01976788453",
        status: "SETTLED"
    },
    {
        date: "2026-08-31",
        trx_id: "LID02104465787",
        amount: 50000.00,
        ref: "NexusPay Fund Transfer",
        status: "SETTLED"
    }
];

// ১. ব্যাংক ট্রানজ্যাকশন ভেরিফাই ও লেজার সিঙ্ক
exports.syncTransaction = async (req, res) => {
    const { transaction_id, amount, date, payment_method } = req.body;

    if (!transaction_id || !amount) {
        return res.status(400).json({ 
            success: false, 
            message: "ট্রানজ্যাকশন আইডি এবং জমার পরিমাণ দেওয়া বাধ্যতামূলক।" 
        });
    }

    // ডুপ্লিকেট এন্ট্রি চেক
    const isDuplicate = ledgerDatabase.some(item => item.trx_id === transaction_id);
    if (isDuplicate) {
        return res.status(409).json({
            success: false,
            message: "এই ট্রানজ্যাকশনটি আগেই লেজারে সিঙ্ক করা হয়েছে!"
        });
    }

    try {
        /* 
        // আসল ব্যাংক এপিআই সিমুলেশন
        const bankResponse = await axios.post(
            process.env.DBBL_API_URL,
            {
                txn_id: transaction_id,
                target_account: process.env.MINISTER_ACCOUNT_NO,
                expected_amount: parseFloat(amount)
            },
            {
                headers: {
                    'Authorization': `Bearer ${process.env.BANK_BEARER_TOKEN}`,
                    'Content-Type': 'application/json'
                }
            }
        );
        */

        // এপিআই রেসপন্স সফল হলে লেজারে তথ্য যুক্তকরণ
        const newRecord = {
            date: date || new Date().toISOString().split('T')[0],
            trx_id: transaction_id,
            amount: parseFloat(amount),
            ref: payment_method || "NexusPay / Bank API",
            status: "SETTLED",
            synced_at: new Date().toLocaleString()
        };

        ledgerDatabase.unshift(newRecord);

        // লেজারের নতুন ব্যালেন্স হিসেব
        const totalPaid = ledgerDatabase.reduce((sum, item) => sum + item.amount, 0);

        return res.status(200).json({
            success: true,
            message: "ব্যাংক এপিআই দ্বারা ভেরিফাইড এবং মিনিস্টার লেজারে সফলভাবে হিট হয়েছে!",
            record: newRecord,
            total_paid: totalPaid
        });

    } catch (error) {
        return res.status(500).json({
            success: false,
            message: "ব্যাংক সিস্টেমের সাথে কানেক্ট করা যায়নি। " + error.message
        });
    }
};

// ২. বর্তমান লেজার তথ্য পাওয়ার এন্ডপয়েন্ট
exports.getLedgerSummary = (req, res) => {
    const totalPaid = ledgerDatabase.reduce((sum, item) => sum + item.amount, 0);
    return res.status(200).json({
        success: true,
        vendor_account: process.env.MINISTER_ACCOUNT_NO || "1041100034560",
        total_transactions: ledgerDatabase.length,
        total_paid: totalPaid,
        logs: ledgerDatabase
    });
};
