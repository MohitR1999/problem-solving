class RateLimiter:
    def __init__(self):
        self.merchants = {}
        self.costs = {
            'GET /balance': 1,
            'POST /payout': 5,
        }

    def allow_request(self, merchant_id: str, timestamp: int) -> bool:
        current_window = timestamp // 10
        if merchant_id not in self.merchants or self.merchants[merchant_id]['window'] < current_window:
            self.merchants[merchant_id] = { 'window': current_window, 'count' : 0 }

        if self.merchants[merchant_id]['count'] < 5:
            self.merchants[merchant_id]['count'] += 1
            return True

        return False

    def allow_weighted_request(self, merchant_id: str, endpoint: str, timestamp: int) -> bool:
        if merchant_id in self.merchants and self.merchants[merchant_id]['penalty_until'] > timestamp:
            return False

        current_window = timestamp // 10
        if merchant_id not in self.merchants or self.merchants[merchant_id]['window'] < current_window:
            self.merchants[merchant_id] = { 
                'window' : current_window, 
                'count' : 0, 
                'tokens_left' : 10,
                'consecutive_rejects' : 0,
                'penalty_until' : 0,  
            }

        cost = self.costs.get(endpoint, 2)
        if self.merchants[merchant_id]['tokens_left'] - cost >= 0:
            self.merchants[merchant_id]['tokens_left'] -= cost
            self.merchants[merchant_id]['count'] += 1
            self.merchants[merchant_id]['consecutive_rejects'] = 0
            return True
        else:
            self.merchants[merchant_id]['consecutive_rejects'] += 1
            if (self.merchants[merchant_id]['consecutive_rejects'] == 3):
                self.merchants[merchant_id]['penalty_until'] = timestamp + 60
            return False