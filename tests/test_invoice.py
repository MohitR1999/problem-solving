from app.invoice import InvoiceProcessor

def test_invoice_processor():
    processor = InvoiceProcessor()
    events = [
        # Valid: None -> DRAFT
        {"event_id": "e1", "invoice_id": "inv_1", "action": "CREATE"},

        # Valid: DRAFT -> OPEN
        {"event_id": "e2", "invoice_id": "inv_1", "action": "FINALIZE"},

        # Invalid: Cannot transition from None -> OPEN. inv_2 doesn't exist yet!
        {"event_id": "e3", "invoice_id": "inv_2", "action": "FINALIZE"},

        # Valid: OPEN -> PAID
        {"event_id": "e4", "invoice_id": "inv_1", "action": "PAY"},

        # Invalid: inv_1 is already PAID. Cannot transition PAID -> VOID.
        {"event_id": "e5", "invoice_id": "inv_1", "action": "VOID"},
    ]
    processor.process_events(events)
    assert processor.invoice_states == {"inv_1": "PAID"}
    assert processor.failed_events == ["e3", "e5"]

def test_invoice_processor_timeline():
    processor = InvoiceProcessor()
    events = [
        {"event_id": "e1", "invoice_id": "inv_1", "action": "CREATE", "timestamp": 100},
        {"event_id": "e2", "invoice_id": "inv_1", "action": "FINALIZE", "timestamp": 150},
        {"event_id": "e3", "invoice_id": "inv_1", "action": "PAY", "timestamp": 200},
    ]
    processor.process_events(events)

    assert processor.get_state_at("inv_1", 50) == None  # Returns None (didn't exist yet)
    assert processor.get_state_at("inv_1", 120) == "DRAFT" # Returns "DRAFT"
    assert processor.get_state_at("inv_1", 150) == "OPEN" # Returns "OPEN" (inclusive of timestamp)
    assert processor.get_state_at("inv_1", 999) == "PAID" # Returns "PAID"