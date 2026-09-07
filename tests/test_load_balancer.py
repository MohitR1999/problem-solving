from app.load_balancer import LoadBalancer

def test_load_balancer():
    # Initialize with 3 servers (Indexes: 0, 1, 2)
    lb = LoadBalancer(3)
    
    # All servers at 0. Tie-breaker picks index 0.
    assert lb.connect("conn_1") == 0
    
    # Server 0 has 1 conn. Servers 1 & 2 have 0. Tie-breaker picks index 1.
    assert lb.connect("conn_2") == 1
    
    # Server 0 & 1 have 1 conn. Server 2 has 0. Picks index 2.
    assert lb.connect("conn_3") == 2
    
    # All servers have 1 conn. Tie-breaker picks index 0.
    assert lb.connect("conn_4") == 0
    
    # Server loads are now: {0: 2, 1: 1, 2: 1}.
    
    # conn_2 disconnects from Server 1. 
    # Server loads are now: {0: 2, 1: 0, 2: 1}.
    lb.disconnect("conn_2")
    
    # Server 1 has the absolute minimum (0). Picks index 1.
    assert lb.connect("conn_5") == 1
    
    print("All Load Balancer Part 1 & 2 tests passed!")

def test_sticky_routing():
    lb = LoadBalancer(3)
    
    # New object (obj_A) -> Least load (0). 
    # obj_A is permanently sticky to Server 0.
    assert lb.connect("conn_1", "obj_A") == 0
    
    # New object (obj_B) -> Least load (1). 
    # obj_B is permanently sticky to Server 1.
    assert lb.connect("conn_2", "obj_B") == 1
    
    # obj_A returns! Ignores load, routes stickily to Server 0.
    assert lb.connect("conn_3", "obj_A") == 0
    
    # Server loads are now: {0: 2, 1: 1, 2: 0}
    
    # New object (obj_C) -> Least load (2). 
    # obj_C is permanently sticky to Server 2.
    assert lb.connect("conn_4", "obj_C") == 2
    
    print("All Load Balancer Part 3 tests passed!")
