from app.offline_sync import SyncEngine

def test_sync_c1():
    initial_state = {
        "tx_123": {"category": "Food", "note": "Lunch"},
        "tx_456": {"category": "Travel", "note": "Flight"}
    }
    events = [
        {"tx_id": "tx_123", "field": "category", "value": "Entertainment", "timestamp": 105},
        {"tx_id": "tx_456", "field": "note", "value": "Business Flight", "timestamp": 110},
        {"tx_id": "tx_789", "field": "category", "value": "Office Supplies", "timestamp": 115} # New transaction
    ]
    engine = SyncEngine(initial_state)
    response = engine.apply_events(events)
    assert response == {
        "tx_123": {"category": "Entertainment", "note": "Lunch"},
        "tx_456": {"category": "Travel", "note": "Business Flight"},
        "tx_789": {"category": "Office Supplies"}
    }

def test_timestamp_resolution_c1():
    initial_state = {
        "tx_123": {
            "category": {"value": "Food", "timestamp": 100},
            "note": {"value": "Lunch", "timestamp": 100}
        },
        "tx_456": {
            "category": {"value": "Travel", "timestamp": 100}
        }
    }

    events = [
        # 1. Server has category at t=100. Event is t=105. ACCEPT.
        {"tx_id": "tx_123", "field": "category", "value": "Entertainment", "timestamp": 105},
    
        # 2. Server has note at t=100. Event is t=90 (Stale!). REJECT.
        {"tx_id": "tx_123", "field": "note", "value": "Breakfast", "timestamp": 90},

        # 3. Server doesn't have a note for tx_456 yet. ACCEPT.
        {"tx_id": "tx_456", "field": "note", "value": "Flight", "timestamp": 95}
    ]

    engine = SyncEngine(initial_state)
    resp = engine.process_batch(events)
    assert resp == {
        "tx_123": {
            "category": {"value": "Entertainment", "timestamp": 105},
            "note": {"value": "Lunch", "timestamp": 100} # Untouched
        },
        "tx_456": {
            "category": {"value": "Travel", "timestamp": 100},
            "note": {"value": "Flight", "timestamp": 95} # Newly added
        }
    }

def test_cascade_events_c1():
    initial_state = {
        "tx_123": {
            "category": {"value": "Food", "timestamp": 100}
        }
    }

    events = [
        # Event 1: REJECTED (Timestamp 90 is older than server's 100)
        {"event_id": "e1", "tx_id": "tx_123", "field": "category", "value": "Entertainment", "timestamp": 90},

        # Event 2: REJECTED (Depends on e1, which failed. Note is NOT updated despite valid timestamp 110)
        {"event_id": "e2", "depends_on": "e1", "tx_id": "tx_123", "field": "note", "value": "Movie", "timestamp": 110},

        # Event 3: ACCEPTED (New transaction, no dependencies)
        {"event_id": "e3", "tx_id": "tx_456", "field": "category", "value": "Travel", "timestamp": 105},

        # Event 4: ACCEPTED (Depends on e3, which succeeded. Timestamp 106 is valid)
        {"event_id": "e4", "depends_on": "e3", "tx_id": "tx_456", "field": "note", "value": "Train", "timestamp": 106}        
    ]

    engine = SyncEngine(initial_state)
    resp = engine.process_batch(events)
    assert resp == {
        "tx_123": {
            "category": {"value": "Food", "timestamp": 100} # Untouched
        },
        "tx_456": {
            "category": {"value": "Travel", "timestamp": 105},
            "note": {"value": "Train", "timestamp": 106}
        }
    }

def test_deep_cascade_bug():
    initial_state = {
        "tx_1": {
            "field1": {"value": "initial", "timestamp": 100}
        }
    }
    
    events = [
        # Event 1: FAILS (Timestamp 90 is older than server's 100)
        {"event_id": "e1", "tx_id": "tx_1", "field": "field1", "value": "new_1", "timestamp": 90},
        
        # Event 2: DEPENDS ON e1. Should fail.
        {"event_id": "e2", "depends_on": "e1", "tx_id": "tx_1", "field": "field2", "value": "new_2", "timestamp": 110},
        
        # Event 3: DEPENDS ON e2. Should ALSO fail because e2 failed.
        {"event_id": "e3", "depends_on": "e2", "tx_id": "tx_1", "field": "field3", "value": "new_3", "timestamp": 120},
    ]
    
    engine = SyncEngine(initial_state)
    response = engine.process_batch(events)
    
    # In your original code, e3 executes! response['tx_1'] will contain 'field3'.
    # We assert that ONLY 'field1' should exist, proving e3 was correctly aborted.
    assert list(response["tx_1"].keys()) == ["field1"], \
        f"Bug caught! Expected only field1, but got {list(response['tx_1'].keys())}"