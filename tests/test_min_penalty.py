from app.minimum_penalty import StoreManager

def test_penalty_log():
    manager = StoreManager()
    log = "BEGIN Y Y N N END"
    # Parsed array: ["Y", "Y", "N", "N"]

    # Store never opens. 
    # Open penalty: 0. Closed penalty: two 'Y's missed. Total: 2
    assert manager.compute_penalty(log, 0) == 2
    # Expected: 2

    # Store closes at index 2 (open for Y, Y. closed for N, N).
    # Open penalty: 0 (no 'N's while open). Closed penalty: 0 (no 'Y's while closed). Total: 0
    assert manager.compute_penalty(log, 2) == 0
    # Expected: 0

    # Store open all day (closes at index 4).
    # Open penalty: two 'N's while open. Closed penalty: 0. Total: 2
    assert manager.compute_penalty(log, 4) == 2
    # Expected: 2

def test_minimum_penalty():
    manager = StoreManager()
    # Parsed: ["Y", "Y", "N", "N"]
    # Penalties for each possible closing time:
    # Close at 0: 2 (Missed two Ys)
    # Close at 1: 1 (Missed one Y)
    # Close at 2: 0 (Perfect!)
    # Close at 3: 1 (Open for one N)
    # Close at 4: 2 (Open for two Ns)
    assert manager.find_best_closing_time("BEGIN Y Y N N END") == 2 
    # Expected: 2

    # Parsed: ["N", "N", "N"]
    # Penalties:
    # Close at 0: 0 (Perfect, never open)
    # Close at 1: 1
    # Close at 2: 2
    # Close at 3: 3
    assert manager.find_best_closing_time("BEGIN N N N END") == 0
    # Expected: 0