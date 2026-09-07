from collections import defaultdict
class AlertManager:
    def __init__(self):
        self.event_records = defaultdict(lambda: defaultdict(lambda: {
            'total_requests' : 0,
            'total_errors' : 0,
        }))

        self.service_states = defaultdict(lambda: "HEALTHY")

        self.all_services = set()

    def record_event(self, timestamp: int, service: str, is_error: bool):
        self.all_services.add(service)
        current_window = timestamp // 60
        stats = self.event_records[service][current_window]
        stats['total_requests'] += 1
        if is_error:
            stats['total_errors'] += 1

    def get_window_stats(self, window_id: int, service: str) -> dict:
        return self.event_records.get(service, {}).get(window_id, { 'total_requests' : 0, 'total_errors' : 0 })

    def evaluate_window(self, window_id: int) -> list[str]:
        results = []
        for service in self.all_services:
            stats = self.event_records[service].get(window_id, { 'total_requests' : 0, 'total_errors' : 0 })
            reqs = stats['total_requests']
            errs = stats['total_errors']
            is_breaching = False
            if reqs > 10 and (errs / reqs) >= 0.5:
                is_breaching = True

            current_state = self.service_states[service]
            if current_state == "HEALTHY" and is_breaching:
                self.service_states[service] = "ALERTING"
                results.append(f"{service} ALERT")

            elif current_state == "ALERTING" and not is_breaching:
                self.service_states[service] = "HEALTHY"
                results.append(f"{service} RESOLVED")

        return sorted(results)


