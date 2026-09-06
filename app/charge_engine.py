class ChargeEngine:
    def __init__(self):
        self.transaction_records = {}

    def process_charge(self, transaction: dict) -> dict:
        idempotency_key = transaction['idempotency_key']
        amount = transaction['amount']
        merchant = transaction['merchant']
        record_key = (merchant, idempotency_key)
        final_record = None
        if record_key in self.transaction_records:
            # Fetch the response from our stored records
            final_record = self.transaction_records[record_key]
            if final_record['status'] == "PROCESSING":
                return {"error": "CONFLICT - PLEASE RETRY LATER"}
            else:
                # Validate the payload
                return { "error" : "INVALID_PAYLOAD" } if final_record['amount_charged'] != amount else final_record
        else:
            self.transaction_records[record_key] = {
                'status' : 'PROCESSING',
                'amount_charged' : amount,
                'merchant' : merchant 
            }
            # Do some payment magic over here
            self.transaction_records[record_key]['status'] = 'SUCCESS'
            final_record = self.transaction_records[record_key]
        
        return final_record
