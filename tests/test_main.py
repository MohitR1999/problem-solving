from app.main import identify_direct_links, identify_fraud_ring_size, identify_risk_score

def test_direct_links_c1() -> None:
    transactions = [
        "Alice,D1",
        "Bob,D1",
        "Charlie,D2",
        "David,D3",
        "Eve,D1"
    ]
    target_user = "Alice"
    response = identify_direct_links(transactions, target_user)
    assert response == ["Bob", "Eve"]

def test_direct_links_c2() -> None:
    transactions = [
        "Alice,D1",
        "Bob,D2",
        "Charlie,D2",
        "David,D3",
        "Eve,D1"
    ]
    target_user = "Charlie"
    response = identify_direct_links(transactions, target_user)
    assert response == ["Bob"]

def test_direct_links_c3() -> None:
    transactions = [
        "Alice,D1",
        "Bob,D2",
        "Charlie,D3",
        "David,D4",
        "Eve,D5"
    ]
    target_user = "Eve"
    response = identify_direct_links(transactions, target_user)
    assert response == []

def test_fraud_ring_size_c1() -> None:
    transactions = [
        "Alice,D1,CC1",
        "Bob,D1,CC2",
        "Charlie,D2,CC2",
        "David,D3,CC3",
        "Eve,D3,CC4"
    ]
    target_user = "Alice"
    response = identify_fraud_ring_size(transactions, target_user)
    assert response == 3

def test_risk_score_c1() -> None:
    transactions = [
        "Alice,D1,CC1,90",
        "Bob,D1,CC2,0",
        "Charlie,D2,CC2,80"
    ]
    target_user = "Alice"
    response = identify_risk_score(transactions, target_user)
    assert response == "true"