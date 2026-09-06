from app.charge_engine import ChargeEngine

def test_charge_engine():
    engine = ChargeEngine()
    # 1. Initial Request (Network is good)
    assert engine.process_charge({
        "idempotency_key": "key_123", 
        "amount": 50, 
        "merchant": "merch_A"
    }) == {"status": "SUCCESS", "amount_charged": 50, "merchant": "merch_A"}

    # 2. Client retries because they dropped connection
    assert engine.process_charge({
        "idempotency_key": "key_123", 
        "amount": 50, 
        "merchant": "merch_A"
    }) == {"status": "SUCCESS", "amount_charged": 50, "merchant": "merch_A"}

    # 3. Completely new transaction
    assert engine.process_charge({
        "idempotency_key": "key_999", 
        "amount": 10, 
        "merchant": "merch_B"
    }) == {"status": "SUCCESS", "amount_charged": 10, "merchant": "merch_B"}

def test_charge_processing():
    # To test this in a synchronous Python script, we can manually 
    # jam a processing state into your cache to simulate a race condition:
    engine = ChargeEngine()

    # Simulate a request that is currently in-flight
    engine.transaction_records[("merch_A", "key_456")] = {"status": "PROCESSING"}

    # A retry hits your server while the first one is still running
    assert engine.process_charge({
        "idempotency_key": "key_456", 
        "amount": 50, 
        "merchant": "merch_A"
    }) == {"error": "CONFLICT - PLEASE RETRY LATER"}

def test_tamper_proofing():
    engine = ChargeEngine()

    # Initial Request
    engine.process_charge({"idempotency_key": "k1", "amount": 50, "merchant": "merch_A"}) 

    # Legitimate Retry
    assert engine.process_charge({"idempotency_key": "k1", "amount": 50, "merchant": "merch_A"}) == {"status": "SUCCESS", "amount_charged": 50, "merchant": "merch_A"}

    # Tampered Retry
    assert engine.process_charge({"idempotency_key": "k1", "amount": 5, "merchant": "merch_A"}) == {"error": "INVALID_PAYLOAD"}