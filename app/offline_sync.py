from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class SyncEvent:
    tx_id: str
    field: str
    value: Any
    timestamp: int
    event_id: Optional[str] = None
    depends_on: Optional[str] = None

class SyncEngine:
    def __init__(self, state: dict):
        self.state = state
        self.successful_events = set()
        self.failed_events = set()

    def _parse_event(self, raw: dict) -> SyncEvent:
        return SyncEvent(
            event_id=raw.get('event_id', None),
            tx_id=raw['tx_id'],
            field=raw['field'],
            value=raw['value'],
            timestamp=raw['timestamp'],
            depends_on=raw.get('depends_on', None)
        )

    def _is_dependency_valid(self, event: SyncEvent) -> bool:
        if not event.depends_on:
            return True

        return event.depends_on in self.successful_events

    def _is_timestamp_valid(self, event: SyncEvent) -> bool:
        tx_state = self.state.get(event.tx_id, {})
        field_state = tx_state.get(event.field, {})

        if not field_state:
            return True

        current_ts = field_state['timestamp']
        if event.timestamp == current_ts:
            return str(event.value) > str(field_state['value'])

        return event.timestamp > current_ts

    def _apply_mutation(self, event: SyncEvent):
        tx_state = self.state.setdefault(event.tx_id, {})
        tx_state[event.field] = {
            'value' : event.value,
            'timestamp' : event.timestamp
        }

    def apply_events(self, events: list[dict]):
        for event in events:
            event_id = event['tx_id']
            field = event['field']
            value = event['value']
            self.state.setdefault(event_id, {})[field] = value
        return self.state

    def process_batch(self, events: list[dict]) -> dict:
        for raw in events:
            try:
                event = self._parse_event(raw)
            except KeyError:
                continue

            if not self._is_dependency_valid(event):
                self.failed_events.add(event.event_id)
                continue

            if not self._is_timestamp_valid(event):
                self.failed_events.add(event.event_id)
                continue

            self._apply_mutation(event)
            self.successful_events.add(event.event_id)

        return self.state