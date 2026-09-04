from app.main import placeholder_to_be_tested

def test_placeholder() -> None:
    resp = placeholder_to_be_tested()
    assert resp == "Hello world"