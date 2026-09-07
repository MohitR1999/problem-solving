from app.fraud_detection import FraudEngine

def test_fraud_engine():
    engine = FraudEngine()
    
    # Transaction 1: $5,000 at t=0 (Approved: 1 tx, $5k total)
    assert engine.process_transaction(0, "acct_1", 5000) == True
    
    # Transaction 2: $4,000 at t=100 (Approved: 2 tx, $9k total)
    assert engine.process_transaction(100, "acct_1", 4000) == True
    
    # Transaction 3: $2,000 at t=200 (REJECTED: Would exceed $10k limit)
    assert engine.process_transaction(200, "acct_1", 2000) == False
    
    # Transaction 4: $500 at t=300 (Approved: 3 tx, $9.5k total)
    assert engine.process_transaction(300, "acct_1", 500) == True
    
    # Transaction 5: $100 at t=400 (REJECTED: Would exceed 3 tx limit)
    assert engine.process_transaction(400, "acct_1", 100) == False
    
    # --- The Sliding Window Shifts ---
    # Fast forward to t=86401 (1 second past 24 hours after t=0).
    # The first transaction (t=0, $5,000) expires and drops out of the window!
    # The window now only contains t=100 ($4k) and t=300 ($500).
    
    # Transaction 6: $5,000 at t=86401 (Approved: 3 tx, $9.5k total in window)
    assert engine.process_transaction(86401, "acct_1", 5000) == True
    
    print("All Fraud Engine Part 1 tests passed!")

def test_fraud_engine_part_2():
    engine = FraudEngine()
    
    # Tx 1: Card 1 (Approved: 1 tx, $100, 1 distinct card)
    assert engine.process_transaction(0, "acct_1", 100, "card_1") == True
    
    # Tx 2: Card 2 (Approved: 2 tx, $200, 2 distinct cards)
    assert engine.process_transaction(100, "acct_1", 100, "card_2") == True
    
    # Tx 3: Card 1 again (Approved: 3 tx, $300, STILL 2 distinct cards)
    assert engine.process_transaction(200, "acct_1", 100, "card_1") == True
    
    # --- The Sliding Window Shifts ---
    # Fast forward to t=86401. Tx 1 (using card_1) expires.
    # The window now contains Tx 2 (card_2) and Tx 3 (card_1). 
    # Notice that card_1 is STILL active in the window because of Tx 3!
    
    # Tx 4: Card 3 (REJECTED: Approving would mean 3 distinct cards in window)
    assert engine.process_transaction(86401, "acct_1", 100, "card_3") == False
    
    # Fast forward to t=86501. Tx 2 (using card_2) expires.
    # The window now ONLY contains Tx 3 (card_1).
    
    # Tx 5: Card 3 (Approved: 2 tx, $200, 2 distinct cards [card_1, card_3])
    assert engine.process_transaction(86501, "acct_1", 100, "card_3") == True

    print("All Fraud Engine Part 2 tests passed!")

# Run the tests
test_fraud_engine_part_2()
