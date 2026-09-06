from app.multi_currency_ledger import SettlementEngine

import math

def test_settlement_engine():
    engine = SettlementEngine()
    
    # The exchange rates matrix provided by the system
    rates = {
        "USD_EUR": 0.90,  # $1 USD = €0.90 EUR
        "EUR_USD": 1.10,  # €1 EUR = $1.10 USD
        "USD_JPY": 150.0  # $1 USD = ¥150 JPY
    }

    # --- Test Case 1: Standard USD Transaction ---
    # Amount: 100.0
    # Percentage Fee: 2.90
    # Fixed Fee: 0.30
    # Expected Net: 96.80
    engine.process_transaction("merchant_A", 100.0, "USD", rates)
    balances_A = engine.get_balances("merchant_A")
    
    assert "USD" in balances_A, "USD balance missing for merchant_A"
    assert math.isclose(balances_A["USD"], 96.80, rel_tol=1e-5), f"Expected 96.80, got {balances_A['USD']}"

    # --- Test Case 2: Foreign Currency Transaction (EUR) ---
    # Amount: 50.0
    # Percentage Fee: 1.45 EUR
    # Fixed Fee: 0.30 USD * 0.90 = 0.27 EUR
    # Expected Net: 48.28 EUR
    engine.process_transaction("merchant_A", 50.0, "EUR", rates)
    balances_A = engine.get_balances("merchant_A")
    
    assert "EUR" in balances_A, "EUR balance missing for merchant_A"
    assert math.isclose(balances_A["EUR"], 48.28, rel_tol=1e-5), f"Expected 48.28, got {balances_A['EUR']}"

    # --- Test Case 3: Zero-Decimal Currency (JPY) ---
    # Amount: 10000.0
    # Percentage Fee: 290.0 JPY
    # Fixed Fee: 0.30 USD * 150.0 = 45.0 JPY
    # Expected Net: 9665.0 JPY
    engine.process_transaction("merchant_B", 10000.0, "JPY", rates)
    balances_B = engine.get_balances("merchant_B")
    
    assert "JPY" in balances_B, "JPY balance missing for merchant_B"
    assert math.isclose(balances_B["JPY"], 9665.0, rel_tol=1e-5), f"Expected 9665.0, got {balances_B['JPY']}"

    # --- Test Case 4: Settlement and State Clearing ---
    # merchant_A currently has: 96.80 USD and 48.28 EUR.
    # We settle to USD. 
    # EUR conversion: 48.28 EUR * 1.10 = 53.108 USD
    # Total payout = 96.80 + 53.108 = 149.908 USD
    payout = engine.settle("merchant_A", "USD", rates)
    
    assert math.isclose(payout, 149.908, rel_tol=1e-5), f"Expected payout 149.908, got {payout}"
    
    # Verify the ledger was wiped clean
    cleared_balances = engine.get_balances("merchant_A")
    assert len(cleared_balances) == 0, f"Ledger not cleared for merchant_A after settlement! Found: {cleared_balances}"
    
    print("All tests passed! You are ready for Stripe.")

# Run the tests
# test_settlement_engine()
