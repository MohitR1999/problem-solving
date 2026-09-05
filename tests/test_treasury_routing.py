from app.treasury_routing import (
    get_route_payout, 
    get_route_payout_with_limit,
    PayoutRouter
)

def test_min_fee_route():
    amount = 1000  # $1,000.00
    rails = [
        {"name": "ACH", "fixed_fee": 1.00, "percent_fee": 0.0},
        {"name": "Wire", "fixed_fee": 15.00, "percent_fee": 0.0},
        {"name": "Instant", "fixed_fee": 0.50, "percent_fee": 0.01}
    ]
    resp = get_route_payout(amount, rails)
    assert resp == "ACH"

def test_payment_rail_with_limit():
    amount = 1000
    max_hours = 24
    rails = [
        {"name": "ACH", "fixed_fee": 1.00, "percent_fee": 0.0, "delivery_hours": 48},
        {"name": "Wire", "fixed_fee": 15.00, "percent_fee": 0.0, "delivery_hours": 24},
        {"name": "Instant", "fixed_fee": 0.50, "percent_fee": 0.01, "delivery_hours": 1}
    ]
    resp = get_route_payout_with_limit(amount, rails, max_hours)
    assert resp == "Instant"

def test_payout_router():
    rails = [
        {"name": "ACH", "fixed_fee": 1.00, "percent_fee": 0.0, "delivery_hours": 48, "daily_capacity": 500000},
        {"name": "Wire", "fixed_fee": 15.00, "percent_fee": 0.0, "delivery_hours": 24, "daily_capacity": 1000000},
        {"name": "Instant", "fixed_fee": 0.50, "percent_fee": 0.01, "delivery_hours": 1, "daily_capacity": 1000}
    ]
    router = PayoutRouter(rails)
    resp = router.route_payout(600, 24)
    assert resp == "Instant"
    resp = router.route_payout(500, 24)
    assert resp == "Wire"