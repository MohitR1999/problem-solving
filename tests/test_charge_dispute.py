from app.charge_dispute import FraudMonitor

def test_fraud_monitor():
    monitor = FraudMonitor()
    
    # 1. Normal charges (No state changes, returns None)
    assert monitor.process_event("CHARGE, ch_1, merch_A") is None
    assert monitor.process_event("CHARGE, ch_2, merch_A") is None
    assert monitor.process_event("CHARGE, ch_3, merch_A") is None
    assert monitor.process_event("CHARGE, ch_4, merch_A") is None
    
    # 2. First dispute. (1 dispute / 4 charges = 25%). 
    # Not enough to trigger Rule A (3 disputes) or Rule B (50% AND >=5 charges).
    assert monitor.process_event("DISPUTE, ch_1") is None
    
    # 3. Fifth charge arrives. (1 dispute / 5 charges = 20%). Still Healthy.
    assert monitor.process_event("CHARGE, ch_5, merch_A") is None
    
    # 4. Second dispute. (2 disputes / 5 charges = 40%). Still Healthy.
    assert monitor.process_event("DISPUTE, ch_2") is None
    
    # 5. Third dispute. (3 disputes). Triggers Rule A! State changes.
    assert monitor.process_event("DISPUTE, ch_3") == "merch_A FRAUDULENT"
    
    # 6. Fourth dispute. Already fraudulent. Should suppress output.
    assert monitor.process_event("DISPUTE, ch_4") is None
    
    # 7. Resolve one dispute. Back to 3 disputes. Still triggers Rule A. 
    assert monitor.process_event("RESOLVE, ch_1") is None
    
    # 8. Resolve another dispute. Now 2 disputes / 5 charges (40%). 
    # Drops below both Rule A and Rule B. State changes back to Healthy!
    assert monitor.process_event("RESOLVE, ch_2") == "merch_A HEALTHY"
    
    print("All Fraud Monitor tests passed!")
