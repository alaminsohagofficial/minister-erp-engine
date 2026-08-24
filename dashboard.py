import streamlit as st
import sqlite3
import pandas as pd
from app import execute_quantum_realtime_sync, initialize_production_database

st.set_page_config(page_title="Minister ERP Real-Time Dashboard", layout="wide")
st.title("⚡ Minister ERP & Logistics Live Control Center")

# ডাটাবেজ ইনিশিয়ালাইজ
initialize_production_database()

# লাইভ স্ট্যাটাস দেখার ফাংশন
def get_live_data():
    conn = sqlite3.connect('minister_main_system.db')
    bank_df = pd.read_sql_query("SELECT * FROM bank_accounts", conn)
    stock_df = pd.read_sql_query("SELECT * FROM warehouse_stock", conn)
    ledger_df = pd.read_sql_query("SELECT * FROM customer_ledger ORDER BY id DESC", conn)
    conn.close()
    return bank_df, stock_df, ledger_df

bank_df, stock_df, ledger_df = get_live_data()

# মেট্রিক কার্ড (উপরের অংশ)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🏦 DBBL Merchant Balance", f"৳ {bank_df.iloc[0]['balance']:,.2f}")
with col2:
    st.metric("📦 Minister AC Warehouse Stock", f"{stock_df.iloc[0]['stock']} Units")
with col3:
    latest_due = ledger_df.iloc[0]['current_balance'] if not ledger_df.empty else 0
    st.metric("👤 Dealer Closing Due", f"৳ {latest_due:,.2f}")

st.divider()

# সিমুলেশন কন্ট্রোল (বাটন চাপলেই ট্রানজেকশন হবে)
st.subheader("💳 Live Webhook Transaction Simulator")
c1, c2, c3 = st.columns(3)
with c1:
    cust_code = st.text_input("Customer Code", "DEAL002905")
with c2:
    pay_amount = st.number_input("Payment Amount (BDT)", value=135000.0, step=5000.0)
with c3:
    qty = st.number_input("AC Quantity Dispatched", value=2, min_value=1)

if st.button("🚀 Process Real-Time Payment & Dispatch Truck", type="primary"):
    payload = {
        "txn_id": f"RCT-{st.session_state.get('txn_cnt', 57650)}",
        "customer_code": cust_code,
        "amount": str(pay_amount),
        "product_code": "120001808",
        "quantity": qty
    }
    execute_quantum_realtime_sync(payload)
    st.success("✅ ট্রানজেকশন সফল! ব্যাংক ব্যালেন্স যোগ হয়েছে, গুদাম থেকে এসি কমেছে এবং ৩টি ডকুমেন্ট তৈরি হয়েছে।")
    st.rerun()

st.divider()

# লাইভ খতিয়ান টেবিল
st.subheader("📊 Customer Ledger / Statement (Live)")
st.dataframe(ledger_df, use_container_width=True)
