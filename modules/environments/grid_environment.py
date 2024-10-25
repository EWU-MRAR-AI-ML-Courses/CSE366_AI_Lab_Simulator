# modules/environments/grid_environment.py

import random

class GridEnvironment:
    def __init__(self, size, num_tasks=5):
        self.size = size
        self.num_tasks = num_tasks
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.obstacles = []
        self.tasks = []
        self.start_position = (0, 0)
        self.generate_environment()

    def generate_environment(self):
        # Place obstacles randomly
        num_obstacles = int(self.size * self.size * 0.2)  # 20% of the grid cells
        while len(self.obstacles) < num_obstacles:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if self.grid[y][x] == 0 and (x, y) != self.start_position:
                self.grid[y][x] = 1
                self.obstacles.append((x, y))

        # Place tasks randomly
        while len(self.tasks) < self.num_tasks:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if self.grid[y][x] == 0 and (x, y) != self.start_position and (x, y) not in self.tasks:
                self.tasks.append((x, y))

    def get_grid(self):
        return self.grid

    def get_tasks(self):
        return self.tasks

    def get_start_position(self):
        return self.start_position
