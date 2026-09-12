def master_reconciliation_check(pool_a, pool_b):
    total_verified = pool_a + pool_b
    sap_target = 35189545.00
    discrepancy = total_verified - sap_target
    return {
        'total_verified_pool': total_verified,
        'sap_s4hana_allocation': sap_target,
        'discrepancy': discrepancy,
        'status': 'Balanced' if discrepancy == 0 else 'Override Required'
    }
