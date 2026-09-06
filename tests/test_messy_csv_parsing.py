from app.messy_csv_parsing import TransactionParser

def test_csv_parser():
    parser = TransactionParser()
    csv_data = """
    name,email,amount
    Alice, alice@stripe.com, 50.00
    Bob, bob@stripe.com, 10.00
    Alice, alice@stripe.com, 25.50
    Charlie, charlie@stripe.com, N/A
    InvalidRowNoCommas
    David, david@stripe.com, 100.oo
    , ghost@stripe.com, 5.00
    """

    assert parser.parse_and_aggregate(csv_data) == {
       "alice@stripe.com": 75.50,
       "bob@stripe.com": 10.00,
       "ghost@stripe.com": 5.00
    }