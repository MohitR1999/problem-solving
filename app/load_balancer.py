from collections import defaultdict
class LoadBalancer:
    def __init__(self, servers: int):
        self.server_mappings = [0 for _ in range(servers)]
        self.state = defaultdict()
        self.object_id_to_server_id = defaultdict()

    def connect(self, connection_id: str, object_id: str = "") -> int:
        if object_id and object_id in self.object_id_to_server_id:
            target_server = self.object_id_to_server_id[object_id]
        else:
            min_load = float('inf')
            min_index = float('inf')
            for index, load in enumerate(self.server_mappings):
                if load < min_load:
                    min_load = load
                    min_index = index
            target_server = min_index
            self.object_id_to_server_id[object_id] = target_server

        self.server_mappings[target_server] += 1
        self.state[connection_id] = target_server
        return target_server

    def disconnect(self, connection_id: str) -> None:
        target_server = self.state.get(connection_id, None)
        if target_server is not None:
            self.server_mappings[target_server] -= 1
            del self.state[connection_id]

