class BillingAccount:
    def __init__(self, initial_balance: float):
        self.balance = initial_balance

    def apply_charge(self, charge_amount: float) -> float:
        tab = self.balance + charge_amount
        if tab >= 0:
            self.balance = 0.0
            return tab
        else:
            self.balance = tab
            return 0        

def calculate_bill(usage: int, tiers: list[dict]) -> float:
    bill = 0.0
    previous_limit = 0
    tiers.sort(key=lambda tier: (tier['up_to'] is None, tier['up_to']))
    for tier in tiers:
        if usage <= 0:
            break
        tier_limit = tier['up_to']
        if tier_limit is not None:
            tier_capacity = tier_limit - previous_limit
            used_amount = min(usage, tier_capacity)
            calculated_bill = used_amount * tier['price']
            bill += calculated_bill
            usage -= used_amount
            previous_limit = tier_limit
        else:
            calculated_bill = usage * tier['price']
            bill += calculated_bill
            usage -= usage
    return bill

def calculate_proration(old_price: float, new_price: float, days_in_month: int, day_of_upgrade: int) -> float:
    old_price_per_day = old_price / days_in_month
    new_price_per_day = new_price / days_in_month
    days_used = day_of_upgrade - 1
    days_left = days_in_month - days_used
    to_be_returned = old_price_per_day * days_left
    to_be_paid = new_price_per_day * days_left
    return to_be_paid - to_be_returned
