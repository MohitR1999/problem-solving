from app.ledger import Ledger

def test_transaction_part_1():
    transactions = [
        {"id": "tx_1", "type": "DEPOSIT", "account": "alice", "amount": 100},
        {"id": "tx_2", "type": "PAY", "from": "alice", "to": "bob", "amount": 30},
        {"id": "tx_3", "type": "PAY", "from": "bob", "to": "charlie", "amount": 10}
    ]
    ledger = Ledger()
    res, _ = ledger.process(transactions)
    assert res == {"alice": 70, "bob": 20, "charlie": 10}

def test_transactions_part_2():
    transactions = [
        {"id": "tx_1", "type": "DEPOSIT", "account": "alice", "amount": 100},
        {"id": "tx_2", "type": "PAY", "from": "alice", "to": "bob", "amount": 30},
        # The app lost connection and retries tx_2, plus a new transaction
        {"id": "tx_2", "type": "PAY", "from": "alice", "to": "bob", "amount": 30}, 
        {"id": "tx_4", "type": "PAY", "from": "bob", "to": "charlie", "amount": 5}
    ]
    ledger = Ledger()
    res, _ = ledger.process(transactions)
    assert res == {"alice": 70, "bob": 25, "charlie": 5}

def test_transactions_part_3():
    transactions = [
        {"id": "tx_1", "type": "DEPOSIT", "account": "alice", "amount": 20},
        {"id": "tx_2", "type": "PAY", "from": "alice", "to": "bob", "amount": 50}, # Rejects: Alice only has 20
        {"id": "tx_3", "type": "DEPOSIT", "account": "alice", "amount": 100},      # Alice now has 120
        {"id": "tx_2", "type": "PAY", "from": "alice", "to": "bob", "amount": 50}  # Retry of tx_2. Still rejects.
    ]
    ledger = Ledger()
    res = ledger.process(transactions)
    assert res == (
        {"alice": 120, "bob": 0}, 
        {"tx_1": "APPROVED", "tx_2": "REJECTED", "tx_3": "APPROVED"}
    )
