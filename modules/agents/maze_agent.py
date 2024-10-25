# modules/agents/maze_agent.py

from modules.search_algorithms.uninformed_search import dfs, bfs, ucs
from modules.search_algorithms.informed_search import astar

class MazeAgent:
    def __init__(self, start_position, goal_position, algorithm='dfs'):
        self.position = start_position
        self.goal_position = goal_position
        self.algorithm = algorithm
        self.path = []
        self.path_traveled = []

    def find_path(self, grid):
        blocked_positions = set()
        grid_size = len(grid)
        if self.algorithm == 'dfs':
            self.path = dfs(self.position, self.goal_position, grid, blocked_positions, grid_size)
        elif self.algorithm == 'bfs':
            self.path = bfs(self.position, self.goal_position, grid, blocked_positions, grid_size)
        elif self.algorithm == 'ucs':
            self.path = ucs(self.position, self.goal_position, grid, blocked_positions, grid_size)
        elif self.algorithm == 'astar':
            self.path = astar(self.position, self.goal_position, grid, blocked_positions, grid_size)
        else:
            raise ValueError(f"Unknown algorithm: {self.algorithm}")

    def move(self):
        if self.path:
            next_position = self.path.pop(0)
            self.position = next_position
            self.path_traveled.append(self.position)
