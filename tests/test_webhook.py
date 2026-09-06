from app.webhook import WebhookDispatcher

def test_webhook_dispatcher_c1():
    dispatcher = WebhookDispatcher()

    # Schedule three events
    dispatcher.schedule_webhook("evt_1", "merch_A", {"status": "paid"}, 100)
    dispatcher.schedule_webhook("evt_2", "merch_B", {"status": "failed"}, 150)
    dispatcher.schedule_webhook("evt_3", "merch_A", {"status": "refunded"}, 120)

    # Time moves to 130
    ready = dispatcher.get_pending_webhooks(130)
    assert ready == ["evt_1", "evt_3"] 
    # Expected: ["evt_1", "evt_3"] (Order doesn't strictly matter, but chronological is best)

    # Call it again at the same time
    ready_again = dispatcher.get_pending_webhooks(130)
    assert ready_again == []
    # Expected: [] (The previous call popped them off the queue)

def test_exponential_backoff_c1():
    dispatcher = WebhookDispatcher()
    dispatcher.schedule_webhook("evt_1", "merch_A", {"status": "paid"}, 100)

    # Pops evt_1 at t=100
    dispatcher.get_pending_webhooks(100) 

    # Worker thread fails to deliver, reports failure.
    # evt_1 has failed 1 time. It should be rescheduled for 100 + 10 = 110.
    dispatcher.report_failure("evt_1", 100)

    # Check at 105: Empty
    assert dispatcher.get_pending_webhooks(105) == []

    # Check at 110: Ready for first retry
    assert dispatcher.get_pending_webhooks(110) == ["evt_1"]

def test_cancel_webhook():
    dispatcher = WebhookDispatcher()
    dispatcher.schedule_webhook("evt_1", "merch_A", {"status": "paid"}, 100)
    dispatcher.schedule_webhook("evt_2", "merch_A", {"status": "refunded"}, 120)

    # Cancel evt_1 instantly in O(1) time
    dispatcher.cancel_webhook("evt_1")

    # Time moves to 130. evt_1 should NOT be returned.
    assert dispatcher.get_pending_webhooks(130) == ["evt_2"]