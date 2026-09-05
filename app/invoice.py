import bisect
from collections import defaultdict
class InvoiceProcessor:
    def __init__(self):
        self.invoice_states = {}
        self.failed_events = []
        self.valid_transitions = {
            ('NONE', 'CREATE') : 'DRAFT',
            ('DRAFT', 'FINALIZE') : 'OPEN',
            ('OPEN', 'PAY') : 'PAID',
            ('OPEN', 'VOID') : 'VOID'
        }
        self.history = defaultdict(list)

    def is_valid_event(self, from_state: str, event: str):
        return (from_state, event) in self.valid_transitions

    def get_next_state(self, from_state: str, event: str):
        return self.valid_transitions.get((from_state, event), "INVALID")

    def get_history_record(self, from_state: str, to_state: str, timestamp: int) -> dict:
        return {
            'FROM' : from_state,
            'TO' : to_state,
            'AT' : timestamp
        }

    def process_events(self, events: list[dict]):
        for event in events:
            event_id = event['event_id']
            invoice_id = event['invoice_id']
            action = event['action']
            timestamp = event.get('timestamp', 0)
            if invoice_id not in self.invoice_states and action == "CREATE":
                self.invoice_states[invoice_id] = "NONE"
            if self.is_valid_event(self.invoice_states.get(invoice_id, "INVALID"), action):
                next_state = self.get_next_state(self.invoice_states[invoice_id], action)
                self.history[invoice_id].append(self.get_history_record(self.invoice_states[invoice_id], next_state, timestamp))
                self.invoice_states[invoice_id] = next_state
            else:
                self.failed_events.append(event_id)

    def get_state_at(self, invoice_id: str, target_time: int) -> str | None:
        if invoice_id not in self.history:
            return None
        invoice_history = self.history[invoice_id]
        if target_time < invoice_history[0]['AT']:
            return None
        else:
            index = bisect.bisect_right(invoice_history, target_time, key=lambda item: item['AT'])
            return invoice_history[index-1]['TO']