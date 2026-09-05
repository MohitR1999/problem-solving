from app.pricing import calculate_bill, calculate_proration, BillingAccount

def test_calculate_bill():
    tiers = [
        {"up_to": 100,  "price": 0.10},  # Units 1 through 100
        {"up_to": 1000, "price": 0.05},  # Units 101 through 1000
        {"up_to": None, "price": 0.01}   # Units 1001 and beyond
    ]

    assert calculate_bill(50, tiers) == 5.0
    assert calculate_bill(150, tiers) == 12.5
    assert calculate_bill(1050, tiers) == 55.5

def test_calculate_proration():
    assert calculate_proration(30.0, 90.0, 30, 11) == 40.0

def test_billing_account_c1():
    account = BillingAccount(initial_balance=-15.0)
    amount_to_bill = account.apply_charge(40.0)
    assert amount_to_bill == 25.0
    assert account.balance == 0.0

def test_billing_account_c2():
    account = BillingAccount(initial_balance=-100.0)
    amount_to_bill = account.apply_charge(40.0)
    assert amount_to_bill == 0.0
    assert account.balance == -60.0

def test_billing_account_c3():
    account = BillingAccount(initial_balance=10.0)
    amount_to_bill = account.apply_charge(40.0)
    assert amount_to_bill == 50.0
    assert account.balance == 0.0