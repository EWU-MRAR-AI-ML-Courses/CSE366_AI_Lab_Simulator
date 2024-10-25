# modules/agents/robot_agent.py

from modules.search_algorithms.uninformed_search import dfs, bfs, ucs
from modules.search_algorithms.informed_search import astar
from modules.search_algorithms.local_search import hill_climbing, simulated_annealing
import time

class RobotAgent:
    def __init__(self, position, algorithm='astar'):
        self.position = position
        self.algorithm = algorithm
        self.path = []
        self.path_traveled = []
        self.current_task = None
        self.tasks_completed = []

    def find_path(self, start, goal, grid, blocked_positions, grid_size):
        if self.algorithm == 'dfs':
            return dfs(start, goal, grid, blocked_positions, grid_size)
        elif self.algorithm == 'bfs':
            return bfs(start, goal, grid, blocked_positions, grid_size)
        elif self.algorithm == 'ucs':
            return ucs(start, goal, grid, blocked_positions, grid_size)
        elif self.algorithm == 'astar':
            return astar(start, goal, grid, blocked_positions, grid_size)
        elif self.algorithm == 'hill_climbing':
            return hill_climbing(start, goal, grid, blocked_positions, grid_size)
        elif self.algorithm == 'simulated_annealing':
            return simulated_annealing(start, goal, grid, blocked_positions, grid_size)
        else:
            raise ValueError(f"Unknown algorithm: {self.algorithm}")

    def move(self):
        if self.path:
            next_position = self.path.pop(0)
            self.position = next_position
            self.path_traveled.append(self.position)
