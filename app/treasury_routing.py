class PayoutRouter:
    def __init__(self, rails: list[dict]):
        self.rails = rails

    def get_fee(self, amount: int, fixed_fee: int, percent_fee: float) -> float:
        return fixed_fee + amount * percent_fee

    def get_route_payout(self, amount: int, rails: list[dict]) -> str:
        min_fee = float('inf')
        final_route = None
        for rail in rails:
            fixed_fee = rail['fixed_fee']
            percent_fee = rail['percent_fee']
            fee = self.get_fee(amount, fixed_fee, percent_fee)
            if fee < min_fee:
                min_fee = fee
                final_route = rail
        return final_route

    def route_payout(self, amount: float, max_hours: int):
        available_routes = [
            r for r in self.rails 
            if r['daily_capacity'] >= amount and r['delivery_hours'] <= max_hours
        ]
        if not available_routes:
            raise ValueError("No eligible routing rails available")

        chosen_rail = self.get_route_payout(amount, available_routes)
        chosen_rail['daily_capacity'] -= amount
        return chosen_rail['name']


def get_fee(amount: int, fixed_fee: int, percent_fee: float) -> float:
    return fixed_fee + amount * percent_fee

def get_route_payout(amount: int, rails: list[dict]) -> str:
    min_fee = float('inf')
    final_route = None
    for rail in rails:
        name = rail['name']
        fixed_fee = rail['fixed_fee']
        percent_fee = rail['percent_fee']
        fee = get_fee(amount, fixed_fee, percent_fee)
        if fee < min_fee:
            min_fee = fee
            final_route = name
    return final_route

def get_route_payout_with_limit(amount: int, rails: list[dict], time_limit: int) -> str:
    eligible_routes = [r for r in rails if r['delivery_hours'] <= time_limit]
    if not eligible_routes:
        raise ValueError("No eligible routing rails available")
    return get_route_payout(amount, eligible_routes)