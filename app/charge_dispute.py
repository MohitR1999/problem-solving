from collections import defaultdict

class FraudMonitor:
    def __init__(self):
        self.merchant_states = defaultdict(lambda: "HEALTHY")
        self.charges = defaultdict(str)
        self.merchant_data = defaultdict(lambda: defaultdict(int))

    def process_event(self, transaction: str):
        parts = [part.strip() for part in transaction.split(",")]
        event_type = parts[0]
        if event_type == "CHARGE":
            charge_id = parts[1]
            merchant_id = parts[2]
            self.merchant_data[merchant_id][event_type] += 1
            self.charges[charge_id] = merchant_id
        elif event_type == "DISPUTE":
            charge_id = parts[1]
            merchant_id = self.charges[charge_id]
            self.merchant_data[merchant_id][event_type] += 1
            self.disputes[charge_id] = merchant_id
        elif event_type == "RESOLVE":
            charge_id = parts[1]
            merchant_id = self.charges[charge_id]
            self.merchant_data[merchant_id]["DISPUTE"] -= 1
            del self.disputes[charge_id]

        active_disputes = self.merchant_data[merchant_id]["DISPUTE"]
        total_charges = self.merchant_data[merchant_id]["CHARGE"]

        current_state = self.merchant_states[merchant_id]
        new_state = current_state

        if (active_disputes >= 3) or total_charges >= 5 and (active_disputes / total_charges) >= 0.5:
            new_state = "FRAUDULENT"
        else:
            new_state = "HEALTHY"

        if current_state != new_state:
            self.merchant_states[merchant_id] = new_state
            return f"{merchant_id} {new_state}"
        return None

