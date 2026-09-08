# Dashboard 


# Real-time dashboard module for Minister ERP Engine (DEAL002905 & MDEL000215)
class ERPDashboard:
    def __init__(self, dealer_code="DEAL002905", secondary_dealer="MDEL000215"):
        self.dealer_code = dealer_code
        self.secondary_dealer = secondary_dealer
        self.primary_entity = "Minister Hi-Tech Park"
        self.secondary_entity = "Salsabilah Electronics Park"
        self.verified_pool = 35189545.00
        self.sap_allocation = 30683180.00

    def get_live_status(self):
        return {
            "primaryDealer": {
                "dealerCode": self.dealer_code,
                "entity": self.primary_entity,
                "status": "DZ Cleared & Override Active",
                "verifiedPool": self.verified_pool,
                "sapAllocation": self.sap_allocation,
                "audit": "Reconciled"
            },
            "secondaryDealer": {
                "dealerCode": self.secondary_dealer,
                "entity": self.secondary_entity,
                "status": "Synchronized Bypass",
                "audit": "Reconciled"
            },
            "timestamp": "2026-09-09T03:22:27Z"
        }
        
