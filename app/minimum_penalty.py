class StoreManager:
    def __init__(self):
        pass

    def _parse_logs(self, log: str) -> list[str]:
        return log.split(" ")[1:-1]

    def compute_penalty(self, log: str, closing_time: int) -> int:
        parsed_logs = self._parse_logs(log)
        total_penalty = 0
        for index, shop_state in enumerate(parsed_logs):
            if shop_state == "Y" and index >= closing_time:
                total_penalty += 1
            elif shop_state == "N" and index < closing_time:
                total_penalty += 1
            else:
                pass
        return total_penalty

    def find_best_closing_time(self, log_string: str) -> int:
        parsed_logs = self._parse_logs(log_string)
        min_penalty = sum([1 for status in parsed_logs if status == "Y"])
        penalty = min_penalty
        best_time = 0
        for i, shop_status in enumerate(parsed_logs):
            penalty += -1 if shop_status == "Y" else 1
            if penalty < min_penalty:
                min_penalty = penalty
                best_time = i + 1
        print(best_time, min_penalty)
        return best_time