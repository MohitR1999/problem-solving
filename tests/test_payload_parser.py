from app.payload_parser_json import PayloadParser

def test_json_flattener():
    parser = PayloadParser()
    
    payload = {
        "merchant_id": "m_123",
        "active": True,
        "details": {
            "name": "Stripe Shop",
            "tax_id": None,  # Rule 4: Should be completely dropped
            "metadata": {}   # Rule 5: Empty dict should be dropped
        },
        "locations": [
            {"city": "San Francisco", "zip": 94103},
            {"city": "Seattle", "zip": 98104}
        ],
        "tags": [] # Rule 5: Empty list should be dropped
    }
    
    expected_output = {
        "merchant_id": "m_123",
        "active": True,
        "details.name": "Stripe Shop",
        "locations[0].city": "San Francisco",
        "locations[0].zip": 94103,
        "locations[1].city": "Seattle",
        "locations[1].zip": 98104
    }
    
    result = parser.flatten_payload(payload)
    
    assert result == expected_output, f"Failed!\nExpected: {expected_output}\nGot: {result}"
    print("All Deep JSON tests passed!")

# Run the tests
test_json_flattener()