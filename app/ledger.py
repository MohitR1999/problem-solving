from collections import defaultdict

class Ledger:
    def __init__(self):
        self.accounts = defaultdict(int)
        self.transaction_status = defaultdict(str)

    def _handle_deposit(self, account: str, amount: int) -> str:
        self.accounts[account] += amount
        return "APPROVED"

    def _handle_pay(self, from_acc: str, to_acc: str, amount: int) -> str:
        if self.accounts[from_acc] - amount < 0:
            return "REJECTED"
        else:
            self.accounts[from_acc] -= amount
            self.accounts[to_acc] += amount
            return "APPROVED"

    def process(self, transactions: list) -> dict:
        for transaction in transactions:
            transaction_type = transaction['type']
            transaction_id = transaction['id']

            if transaction_id in self.transaction_status:
                continue

            if transaction_type == "PAY":
                from_account = transaction['from']
                to_account = transaction['to']
                _ = self.accounts[from_account]
                _ = self.accounts[to_account]
                amount = transaction['amount']
                status = self._handle_pay(from_account, to_account, amount)
                self.transaction_status[transaction_id] = status
            elif transaction_type == "DEPOSIT":
                account = transaction['account']
                amount = transaction['amount']
                status = self._handle_deposit(account, amount)
                self.transaction_status[transaction_id] = status
            else:
                pass

        return (dict(self.accounts), dict(self.transaction_status))
