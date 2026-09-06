from collections import defaultdict
import heapq
class ShippingRouter:
    def __init__(self, raw_routes: str):
        self.graph = defaultdict(lambda: defaultdict(int))
        routes = raw_routes.split(":")
        for route in routes:
            parts = route.split(",")
            source = parts[0]
            dest = parts[1]
            cost = int(parts[3])
            if dest not in self.graph[source]:
                self.graph[source][dest] = cost
            else:
                self.graph[source][dest] = min(self.graph[source][dest], cost)

    def get_direct_cost(self, source: str, dest: str) -> int:
        return self.graph.get(source, {}).get(dest, None)

    def get_cheapest_route(self, source: str, dest: str) -> int:
        distances = { source : 0 }
        priority_queue = [(0, source)]
        predecessors = {}
        while priority_queue:
            current_distance, node = heapq.heappop(priority_queue)

            if node == dest:
                path = []
                current = dest
                while current is not None:
                    path.append(current)
                    current = predecessors.get(current)
                path.reverse()
                return {
                    'cost' : current_distance,
                    'path': path
                }
            
            if current_distance > distances.get(node, float('inf')):
                continue

            for neighbor, cost in self.graph.get(node, {}).items():
                 dist = current_distance + cost
                 if dist < distances.get(neighbor, float('inf')):
                     distances[neighbor] = dist
                     predecessors[neighbor] = node
                     heapq.heappush(priority_queue, (dist, neighbor))

        return None


