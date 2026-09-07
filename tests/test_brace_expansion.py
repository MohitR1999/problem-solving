from app.brace_expansion import RouteParser

def test_brace_expansion():
    parser = RouteParser()
    
    # Example 1: Standard expansion
    res_1 = parser.expand_pattern("{a,b}c{d,e}f")
    assert res_1 == ["acdf", "acef", "bcdf", "bcef"], f"Failed 1: {res_1}"
    
    # Example 2: No braces at all
    res_2 = parser.expand_pattern("stripe")
    assert res_2 == ["stripe"], f"Failed 2: {res_2}"
    
    # Example 3: Real-world routing example
    res_3 = parser.expand_pattern("api/{v1,v2}/users")
    assert res_3 == ["api/v1/users", "api/v2/users"], f"Failed 3: {res_3}"

    # Example 4: Sorting is required!
    res_4 = parser.expand_pattern("{c,a,b}")
    assert res_4 == ["a", "b", "c"], f"Failed 4: {res_4}"

    print("All Brace Expansion Part 1 tests passed!")

# Run the tests
test_brace_expansion()