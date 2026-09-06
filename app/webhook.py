import heapq

class WebhookDispatcher:
    def __init__(self):
        self.scheduled_webhooks = []
        self.events = {}

    def schedule_webhook(self, event_id: str, merchant_id: str, payload: dict, timestamp: int):
        heapq.heappush(self.scheduled_webhooks, (timestamp, event_id, merchant_id, payload))
        self.events[event_id] = { 'merchant_id' : merchant_id, 'payload' : payload, 'failed': 0, 'cancelled' : False }

    def get_pending_webhooks(self, current_time: int) -> list[str]:
        res = []
        while self.scheduled_webhooks and self.scheduled_webhooks[0][0] <= current_time:
            elem = heapq.heappop(self.scheduled_webhooks)
            event_id = elem[1]
            if self.events[event_id]['cancelled']:
                continue
            res.append(event_id)
        return res

    def report_failure(self, event_id: str, current_time: int):
        if event_id in self.events:
            event = self.events[event_id]
            failed_times = event['failed']
            if failed_times < 5:
                delay = 10 * (2 ** (failed_times))
                self.events[event_id]['failed'] += 1
                next_retry_timestamp = current_time + delay
                heapq.heappush(self.scheduled_webhooks, (next_retry_timestamp, event_id, event['merchant_id'], event['payload']))

    def cancel_webhook(self, event_id: str):
        if event_id in self.events:
            self.events[event_id]['cancelled'] = True