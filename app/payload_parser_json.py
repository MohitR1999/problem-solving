from typing import Any
class PayloadParser:
    def __init__(self):
        pass

    def flatten_payload(self, payload: dict) -> dict:
        result = {}
        def flatten_helper(payload: Any, key: str, result: dict):
            if payload is None or payload == {} or payload == []:
                pass
            elif isinstance(payload, int) or isinstance(payload, str) or isinstance(payload, float) or isinstance(payload, bool):
                result[key] = payload
            elif isinstance(payload, dict):
                for property_name in payload:
                    flatten_helper(payload[property_name], f"{key}.{property_name}" if key else property_name, result)
            else:
                for index, item in enumerate(payload):
                    flatten_helper(item, f"{key}[{index}]", result)
        flatten_helper(payload, "", result)
        return result