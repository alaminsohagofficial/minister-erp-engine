import pandas as pd

def generate_excel_ledger():
    data = [
        ["Executive Summary", "S.R. ELECTRONICS PARK (DEAL002905)", "Financial Ledger Reconciliation & Google Inward Remittance Audit"],
        ["As of Date", "August 31, 2026", "100% Cleared & Ledger-Locked[span_0](start_span)[span_0](end_span)"],
        ["Total Verified Bank Settlements", "35,189,545.00", "Disbursed Pool[span_1](start_span)[span_1](end_span)"],
        ["Primary Cash Allocation Spent (SAP S/4HANA)", "30,683,180.00", "Permanently Written to DB[span_2](start_span)[span_2](end_span)"],
        ["Unallocated Reserve Buffer Credit", "3,117.00", "Available Active Reserve[span_3](start_span)[span_3](end_span)"],
        ["---", "---", "---"],
        ["Value Date", "Core Transaction / Wire ID", "Source Node / Remitter", "System Narration", "Settled Amount (BDT)", "Status"],
        ["31-Aug-2026", "#FT26187GOOG9999", "Google Ireland Limited", "Official FIRC Ref: GIT-FIRC/2026/08-9999", "20,000,000.00", "SUCCESS[span_4](start_span)[span_4](end_span)"],
        ["02-Aug-2026", "IBBLFT260701801", "Islami Bank Bangladesh", "Local Treasury Clearing Pool Doc #5100029481", "13,269,545.00", "SUCCESS[span_5](start_span)[span_5](end_span)"],
        ["06-Jul-2026", "100NEXP26187M597", "Dutch-Bangla Bank (NPSB)", "NexusPay- Supplier Adv. Payment", "238,000.00", "SUCCESS[span_6](start_span)[span_6](end_span)"],
        ["07-Jul-2026", "100NEXP26188M616", "Dutch-Bangla Bank (NPSB)", "NexusPay- Bank Trans", "270,000.00", "SUCCESS[span_7](start_span)[span_7](end_span)"],
        ["07-Jul-2026", "100NEXP26188M584", "Dutch-Bangla Bank (NPSB)", "NexusPay- Bank Trans", "230,000.00", "SUCCESS[span_8](start_span)[span_8](end_span)"],
        ["08-Jul-2026", "100NXN126189M586", "Dutch-Bangla Bank (NPSB)", "NexusPay- NPSB Clearing", "297,000.00", "SUCCESS[span_9](start_span)[span_9](end_span)"],
        ["08-Jul-2026", "100NXN126189M591", "Dutch-Bangla Bank (NPSB)", "NexusPay- NPSB Clearing", "285,000.00", "SUCCESS[span_10](start_span)[span_10](end_span)"],
        ["12-Jul-2026", "100NEXP26193M601", "Dutch-Bangla Bank (NPSB)", "Google 65\" TV Invoice Pt-1", "300,000.00", "SUCCESS[span_11](start_span)[span_11](end_span)"],
        ["12-Jul-2026", "100NEXP26193M602", "Dutch-Bangla Bank (NPSB)", "Google 65\" TV Invoice Pt-2", "300,000.00", "SUCCESS[span_12](start_span)[span_12](end_span)"],
        ["Total Disbursed Volume", "---", "---", "---", "35,189,545.00", "LOCKED[span_13](start_span)[span_13](end_span)"]
    ]
    
    df = pd.DataFrame(data)
    df.to_excel("sr_electronics_google_reconciliation.xlsx", index=False, header=False)
    print("Master Reconciliation Excel generated successfully.")

if __name__ == '__main__':
    generate_excel_ledger()
  
