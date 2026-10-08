const express = require('express');
const cors = require('cors');
const path = require('path');
require('dotenv').config();

const bankSyncController = require('./controllers/bankSyncController');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// এপিআই রাউটসমূহ
app.post('/api/sync-bank-transaction', bankSyncController.syncTransaction);
app.get('/api/ledger-summary', bankSyncController.getLedgerSummary);

app.listen(PORT, () => {
    console.log(`=================================`);
    console.log(`Minister ERP Engine Live on Port ${PORT}`);
    console.log(`=================================`);
});
