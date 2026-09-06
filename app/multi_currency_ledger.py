from collections import defaultdict
class SettlementEngine:
    def __init__(self):
        self.ledger = defaultdict(lambda: defaultdict(float))

    def get_balances(self, merchant_id: str) -> dict:
        return self.ledger.get(merchant_id, {})

    def process_transaction(self, merchant_id: str, amount: float, currency: str, exchange_rates: dict):
        fixed_fee = 0.30 if currency == "USD" else exchange_rates[f"USD_{currency}"] * 0.30
        percentage_fee = (2.9 / 100) * amount
        self.ledger[merchant_id][currency] += amount - fixed_fee - percentage_fee

    def settle(self, merchant_id: str, base_currency: str, exchange_rates: dict) -> float:
        merchant_record = self.ledger.pop(merchant_id, {})
        final_payout = 0.0
        for target_currency, amount in merchant_record.items():
            if target_currency == base_currency:
                final_payout += amount
            else:
                final_payout += amount * exchange_rates.get(f"{target_currency}_{base_currency}", 1.0)
        return final_payout