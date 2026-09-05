from app.rate_limiter import RateLimiter

def test_rate_limiter():
    limiter = RateLimiter()
    assert limiter.allow_request("merch_A", 2) == True  # True (Count: 1)
    assert limiter.allow_request("merch_A", 3) == True  # True (Count: 2)
    assert limiter.allow_request("merch_B", 3) == True  # True (Count: 1 for merch_B)
    assert limiter.allow_request("merch_A", 4) == True  # True (Count: 3)
    assert limiter.allow_request("merch_A", 5) == True  # True (Count: 4)
    assert limiter.allow_request("merch_A", 8) == True  # True (Count: 5)
    assert limiter.allow_request("merch_A", 9) == False

def test_weighted_rate_limit():
    limiter = RateLimiter()
    # Window 0-9
    assert limiter.allow_weighted_request("merch_A", "POST /payout", 2) == True  # True (Remaining: 5)
    assert limiter.allow_weighted_request("merch_A", "POST /payout", 3) == True  # True (Remaining: 0)
    assert limiter.allow_weighted_request("merch_A", "GET /balance", 4) == False  # False (Cost 1, Remaining 0)

    # Window 10-19
    assert limiter.allow_weighted_request("merch_A", "POST /payout", 11) == True # True (Remaining: 5)

def test_penalty_box():
    limiter = RateLimiter()
    assert limiter.allow_weighted_request("merch_A", "POST /payout", 2) == True  # True (Remaining: 5)
    assert limiter.allow_weighted_request("merch_A", "POST /payout", 3) == True  # True (Remaining: 0)
    assert limiter.allow_weighted_request("merch_A", "POST /payout", 4) == False  # False (Rejection 1)
    assert limiter.allow_weighted_request("merch_A", "GET /balance", 5) == False  # False (Rejection 2)
    assert limiter.allow_weighted_request("merch_A", "GET /balance", 6) == False  # False (Rejection 3 - PENALTY BOX UNTIL t=66)

    # Normal window resets don't matter anymore
    assert limiter.allow_weighted_request("merch_A", "GET /balance", 15) == False # False (Blocked by penalty)
    assert limiter.allow_weighted_request("merch_A", "GET /balance", 65) == False # False (Blocked by penalty)

    # Penalty expires
    assert limiter.allow_weighted_request("merch_A", "GET /balance", 67) == True # True (Penalty lifted, fresh tokens)