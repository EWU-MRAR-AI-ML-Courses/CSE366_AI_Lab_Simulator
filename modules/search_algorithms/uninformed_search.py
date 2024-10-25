# modules/search_algorithms/uninformed_search.py

from collections import deque
import heapq


def dfs(start, goal, grid, blocked_positions, grid_size):
    stack = [(start, [start])]
    visited = set()

    while stack:
        (vertex, path) = stack.pop()
        if vertex not in visited:
            if vertex in blocked_positions:
                continue
            visited.add(vertex)
            if vertex == goal:
                return path
            neighbors = get_neighbors(vertex, grid, blocked_positions, grid_size)
            for neighbor in neighbors:
                stack.append((neighbor, path + [neighbor]))
    return None


def bfs(start, goal, grid, blocked_positions, grid_size):
    queue = deque([(start, [start])])
    visited = set([start])

    while queue:
        (vertex, path) = queue.popleft()
        if vertex == goal:
            return path
        neighbors = get_neighbors(vertex, grid, blocked_positions, grid_size)
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return None


def ucs(start, goal, grid, blocked_positions, grid_size):
    queue = [(0, start, [start])]
    visited = set()

    while queue:
        (cost, vertex, path) = heapq.heappop(queue)
        if vertex not in visited:
            if vertex in blocked_positions:
                continue
            visited.add(vertex)
            if vertex == goal:
                return path
            neighbors = get_neighbors(vertex, grid, blocked_positions, grid_size)
            for neighbor in neighbors:
                heapq.heappush(queue, (cost + 1, neighbor, path + [neighbor]))
    return None


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
