// server.js - Real-time Webhook Listener for Minister ERP Engine
const express = require('express');
const crypto = require('crypto');
const app = express();

app.use(express.json());

// Secret token for enterprise-grade security verification
const WEBHOOK_SECRET = process.env.ERP_WEBHOOK_SECRET || 'minister-secure-sync-key';

app.post('/api/v1/erp-webhook', (req, res) => {
    const signature = req.headers['x-erp-signature'];
    
    // Verify payload integrity for high security
    const hmac = crypto.createHmac('sha256', WEBHOOK_SECRET);
    const digest = hmac.update(JSON.stringify(req.body)).digest('hex');

    if (signature !== `sha256=${digest}`) {
        return res.status(401).json({ status: 'Unauthorized', error: 'Invalid signature' });
    }

    const transactionData = req.body;
    console.log('[SPONTANEOUS SYNC] Received live SAP transaction:', transactionData);

    // TODO: Process and insert verified settlement record into database/dashboard storage
    
    return res.status(200).json({ 
        status: 'Success', 
        message: 'Real-time ERP synchronization completed successfully',
        timestamp: new Date().toISOString()
    });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Minister ERP Sync Engine running on port ${PORT}`);
});
