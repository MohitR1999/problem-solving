from collections import defaultdict
class TransactionParser:
    def __init__(self):
        pass

    def parse_and_aggregate(self, csv_data: str) -> dict:
        lines = [l.strip() for l in csv_data.split("\n") if l][1:]
        records = defaultdict(float)
        for line in lines:
            data_parts = line.split(",")
            if len(data_parts) < 3:
                continue
            name = data_parts[0].strip()
            email = data_parts[1].strip()
            amount_str = data_parts[2]
            try:
                amount = float(amount_str)
                records[email] += amount
            except ValueError:
                print(f"Invalid values detected: name {name}, email: {email}, amount: {amount_str}, skipping")
                continue
        return dict(records)
