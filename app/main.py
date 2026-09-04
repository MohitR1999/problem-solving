from collections import defaultdict, deque

def build_graph(transactions: list[str], target_user: str):
    graph = defaultdict(set)
    device_to_users = defaultdict(set)
    cc_to_users = defaultdict(set)
    user_to_score = defaultdict(int)
    all_users = set()
    for row in transactions:
        parts = [item.strip() for item in row.split(",")]
        user_id, device_id, cc_id = parts[0], parts[1], parts[2]
        device_to_users[device_id].add(user_id)
        cc_to_users[cc_id].add(user_id)
        all_users.add(user_id)
        if len(parts) >= 4:
            user_to_score[user_id] = int(parts[3])

        for user in device_to_users[device_id]:
            graph[user].add(user_id)
            graph[user_id].add(user)

        for user in cc_to_users[cc_id]:
            graph[user].add(user_id)
            graph[user_id].add(user)

    if target_user not in all_users:
        return set(), user_to_score

    visited = {target_user}
    queue = deque([target_user])
    while queue:
        curr = queue.popleft()
        for neighbor in graph[curr]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return visited, user_to_score

def identify_direct_links(transactions: list[str], target_user: str) -> list[str]:
    user_to_device = defaultdict(list)
    device_to_user = defaultdict(list)
    for row in transactions:
        user_id, device_id = [item.strip() for item in row.split(",")]
        user_to_device[user_id].append(device_id)
        device_to_user[device_id].append(user_id)

    result = []
    for device in user_to_device.get(target_user, []):
        for user in device_to_user.get(device, []):
            if user != target_user:
                result.append(user)

    return sorted(result)

def identify_fraud_ring_size(transactions: list[str], target_user: str) -> int:
    members, _ = build_graph(transactions, target_user)
    return len(members)

def identify_risk_score(transactions: list[str], target_user: str) -> str:
    ring_members, scores = build_graph(transactions, target_user)
    scores_to_consider = [scores[user] for user in ring_members if scores.get(user, 0) > 0]
    avg_score = sum(scores_to_consider) / len(scores_to_consider)
    return "true" if avg_score > 75 else "false"