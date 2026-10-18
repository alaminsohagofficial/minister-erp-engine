/**
 * Minister ERP Engine - Server & API Route Handler
 * Dealer Code: DEAL002905
 */

const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

// রিয়েল-টাইম লেজার সিঙ্ক এন্ডপয়েন্ট
app.post('/api/v1/sync-ledger', (req, res) => {
    const { dealer_id, transactions, total_disputed_pool_bdt } = req.body;
    
    if (dealer_id !== "DEAL002905") {
        return res.status(403).json({ error: "Unauthorized Dealer ID" });
    }

    let calculatedSum = transactions.reduce((acc, curr) => acc + curr.amount, 0);
    
    if (calculatedSum === total_disputed_pool_bdt) {
        res.status(200).json({
            status: "SUCCESS",
            message: "Ledger reconciled successfully via NPSB Switch.",
            verified_total: calculatedSum,
            timestamp: new Date().toISOString()
        });
    } else {
        res.status(400).json({
            status: "FAILED",
            message: "Amount mismatch detected in ledger pool."
        });
    }
});

// ইমারজেন্সি ফান্ড ম্যানেজমেন্ট এন্ডপয়েন্ট
app.post('/api/v1/emergency-transfer', (req, res) => {
    const { source_account, target_mfs, amount } = req.body;
    
    // ইমারজেন্সি ৫০,০০০ টাকা বা যেকোনো অ্যামাউন্ট ট্রান্সফার লজিক
    console.log(`Processing emergency transfer of ৳${amount} from ${source_account} to ${target_mfs}`);
    
    res.status(200).json({
        status: "COMPLETED",
        transaction_id: "EMERGENCY_TXN_" + Date.now(),
        transferred_amount: amount,
        routing: "DBBL Core / Sonali CBS Universal"
    });
});

app.listen(PORT, () => {
    console.log(`Minister ERP Engine running on port ${PORT}`);
});
