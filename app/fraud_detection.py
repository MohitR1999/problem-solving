from collections import deque, defaultdict
class FraudEngine:
    def __init__(self):
        self.history = defaultdict(deque)
        self.window_spend = defaultdict(int)
        self.card_frequency = defaultdict(lambda: defaultdict(int))

    def process_transaction(self, timestamp: int, account_id: str, amount: int, card_id: str = "") -> bool:
        account_history = self.history[account_id]
        cutoff = timestamp - 86400
        while account_history and account_history[0][0] <= cutoff:
            expired_tx = account_history.popleft()
            card_id_to_be_removed = expired_tx[2]
            self.card_frequency[account_id][card_id_to_be_removed] -= 1
            self.window_spend[account_id] -= expired_tx[1]

            if self.card_frequency[account_id][card_id_to_be_removed] == 0:
                del self.card_frequency[account_id][card_id_to_be_removed]

        current_tx_count = len(account_history)
        current_tx_total_spend = self.window_spend[account_id]
        current_total_unique_cards = len(self.card_frequency[account_id])

        if current_tx_count >= 3:
            return False

        if current_tx_total_spend + amount > 10_000:
            return False    

        if self.card_frequency[account_id].get(card_id, 0) == 0:
            if current_total_unique_cards + 1 > 2:
                return False

        account_history.append((timestamp, amount, card_id))
        self.window_spend[account_id] += amount
        if card_id:
            self.card_frequency[account_id][card_id] += 1

        print(self.card_frequency)
        return True





