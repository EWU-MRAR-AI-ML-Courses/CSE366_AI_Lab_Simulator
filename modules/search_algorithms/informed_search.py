# modules/search_algorithms/informed_search.py

import heapq


def astar(start, goal, grid, blocked_positions, grid_size):
    open_set = []
    heapq.heappush(open_set, (0, start, [start]))
    g_scores = {start: 0}
    f_scores = {start: heuristic(start, goal)}

    while open_set:
        (_, current, path) = heapq.heappop(open_set)
        if current == goal:
            return path

        neighbors = get_neighbors(current, grid, blocked_positions, grid_size)
        for neighbor in neighbors:
            tentative_g_score = g_scores[current] + 1
            if neighbor in blocked_positions:
                continue
            if neighbor not in g_scores or tentative_g_score < g_scores[neighbor]:
                g_scores[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic(neighbor, goal)
                f_scores[neighbor] = f_score
                heapq.heappush(open_set, (f_score, neighbor, path + [neighbor]))
    return None


def heuristic(a, b):
    # Using Manhattan distance as heuristic
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def get_neighbors(position, grid, blocked_positions, grid_size):
    x, y = position
    neighbors = []
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Left, Right, Up, Down

    for move in moves:
        nx, ny = x + move[0], y + move[1]
        if 0 <= nx < grid_size and 0 <= ny < grid_size:
            if grid[ny][nx] == 0 and (nx, ny) not in blocked_positions:
                neighbors.append((nx, ny))
    return neighbors
