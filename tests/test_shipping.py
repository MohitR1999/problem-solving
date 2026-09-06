from app.shipping import ShippingRouter

def test_direct_route():
    # Notice that there are two direct routes from US to UK (UPS for 5, DHL for 4)
    routes = "US,UK,UPS,5:US,CA,FedEx,3:CA,UK,DHL,7:US,UK,DHL,4"
    router = ShippingRouter(routes)

    # Should find the cheapest direct route
    assert router.get_direct_cost("US", "UK") == 4

    # Exists, but only one option
    assert router.get_direct_cost("US", "CA") == 3

    # No direct route exists from UK to US (routes are one-way!)
    assert router.get_direct_cost("UK", "US") == None

def test_cheapest_route():
    routes = "US,CA,FedEx,3:CA,UK,DHL,7:US,UK,UPS,15:UK,FR,DHL,2"
    router = ShippingRouter(routes)

    # Direct route US -> UK is 15. 
    # But US -> CA (3) + CA -> UK (7) = 10. 
    # 10 is cheaper than 15!
    assert router.get_cheapest_route("US", "UK")['cost'] == 10

    # Multi-hop: US -> CA (3) + CA -> UK (7) + UK -> FR (2) = 12
    assert router.get_cheapest_route("US", "FR")['cost'] == 12

    assert router.get_cheapest_route("FR", "US") == None

def test_cheapest_route_with_path():
    routes = "US,CA,FedEx,3:CA,UK,DHL,7:US,UK,UPS,15"
    router = ShippingRouter(routes)

    assert router.get_cheapest_route("US", "UK") =={"cost": 10, "path": ["US", "CA", "UK"]}