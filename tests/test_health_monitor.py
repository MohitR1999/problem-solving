from app.health_monitor import AlertManager

def test_part_1():
    manager = AlertManager()
    # --- WINDOW 0 (t=0 to t=59) ---
    # Service A: 3 requests, 2 errors
    manager.record_event(10, "Service_A", is_error=True)
    manager.record_event(15, "Service_A", is_error=True)
    manager.record_event(59, "Service_A", is_error=False)

    # Service B: 1 request, 1 error
    manager.record_event(5, "Service_B", is_error=True)

    # --- WINDOW 1 (t=60 to t=119) ---
    # Service A: 2 requests, 0 errors
    manager.record_event(60, "Service_A", is_error=False)
    manager.record_event(119, "Service_A", is_error=False)

    # --- ASSERTS ---
    
    # Check Window 0
    stats_a_0 = manager.get_window_stats(0, "Service_A")
    assert stats_a_0['total_requests'] == 3, f"A Win0 Total failed: {stats_a_0}"
    assert stats_a_0['total_errors'] == 2, f"A Win0 Errors failed: {stats_a_0}"
    
    stats_b_0 = manager.get_window_stats(0, "Service_B")
    assert stats_b_0['total_requests'] == 1, f"B Win0 Total failed: {stats_b_0}"
    assert stats_b_0['total_errors'] == 1, f"B Win0 Errors failed: {stats_b_0}"

    # Check Window 1
    stats_a_1 = manager.get_window_stats(1, "Service_A")
    assert stats_a_1['total_requests'] == 2, f"A Win1 Total failed: {stats_a_1}"
    assert stats_a_1['total_errors'] == 0, f"A Win1 Errors failed: {stats_a_1}"

    # Check Empty State (Service B had no traffic in Window 1)
    stats_b_1 = manager.get_window_stats(1, "Service_B")
    assert stats_b_1['total_requests'] == 0, f"B Win1 Total failed: {stats_b_1}"
    assert stats_b_1['total_errors'] == 0, f"B Win1 Errors failed: {stats_b_1}"

    print("All Part 1 tests passed!")

def test_part_2():
    manager = AlertManager()

    # --- WINDOW 0 (t=0 to 59) ---
    # Service A: 12 requests, 8 errors -> BREACH (>10 reqs, 66% error rate)
    for i in range(12):
        manager.record_event(timestamp=10, service="Service_A", is_error=(i < 8))

    # Service B: 5 requests, 5 errors -> NO BREACH (reqs <= 10)
    for _ in range(5):
        manager.record_event(timestamp=20, service="Service_B", is_error=True)

    res_0 = manager.evaluate_window(0)
    assert sorted(res_0) == ["Service_A ALERT"], f"Window 0 failed: {res_0}"

    # --- WINDOW 1 (t=60 to 119) ---
    # Service A: 20 requests, 20 errors -> BREACH, but already ALERTING (Suppressed!)
    for _ in range(20):
        manager.record_event(timestamp=70, service="Service_A", is_error=True)

    # Service B: 12 requests, 6 errors -> BREACH (>10 reqs, 50% error rate) -> ALERT
    for i in range(12):
        manager.record_event(timestamp=80, service="Service_B", is_error=(i < 6))

    res_1 = manager.evaluate_window(1)
    assert sorted(res_1) == ["Service_B ALERT"], f"Window 1 failed: {res_1}"

    # --- WINDOW 2 (t=120 to 179) ---
    # Service A: 100 requests, 1 error -> RECOVERS (Error rate < 50%) -> RESOLVED
    for i in range(100):
        manager.record_event(timestamp=130, service="Service_A", is_error=(i == 0))

    # Service B: 0 traffic in Window 2! -> RECOVERS (reqs <= 10) -> RESOLVED
    # (Notice: no record_event called for Service B in Window 2!)

    res_2 = manager.evaluate_window(2)
    assert sorted(res_2) == ["Service_A RESOLVED", "Service_B RESOLVED"], f"Window 2 failed: {res_2}"

    print("All Part 2 tests passed!")

test_part_2()
