# modules/agents/robot_agent.py

from modules.search_algorithms import (
    dfs, bfs, ucs, astar, hill_climbing, simulated_annealing
)


class RobotAgent:
    def __init__(self, position, algorithm='astar'):
        self.position = position
        self.path = []
        self.tasks_completed = []
        self.path_traveled = [position]  # Keep track of the path traversed
        self.current_task = None
        self.algorithm = algorithm

    def move(self):
        if self.path:
            self.position = self.path.pop(0)
            self.path_traveled.append(self.position)

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
