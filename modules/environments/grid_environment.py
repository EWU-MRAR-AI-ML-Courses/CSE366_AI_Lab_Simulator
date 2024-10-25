# modules/environments/grid_environment.py

import random


class GridEnvironment:
    def __init__(self, grid_size, room_start, room_end, door_position):
        self.grid_size = grid_size
        self.room_start = room_start
        self.room_end = room_end
        self.door_position = door_position

        self.grid, self.obstacles = self.create_environment()

    def create_environment(self):
        grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        obstacles = set()

        # Build walls
        for x in range(self.room_start[0], self.room_end[0] + 1):
            for y in range(self.room_start[1], self.room_end[1] + 1):
                if (x == self.room_start[0] or x == self.room_end[0] or
                        y == self.room_start[1] or y == self.room_end[1]):
                    if (x, y) != self.door_position:  # Leave the door open
                        obstacles.add((x, y))
                        grid[y][x] = 1  # Mark as obstacle

        return grid, obstacles

    def generate_tasks(self, num_tasks, start_pos, task_positions=None):
        tasks = {}
        i = 1
        if task_positions is not None:
            # Use provided task positions
            for position in task_positions:
                if (0 <= position[0] < self.grid_size and 0 <= position[1] < self.grid_size and
                        position not in self.obstacles and
                        position != start_pos and
                        self.grid[position[1]][position[0]] == 0):
                    task_name = f'Task {i}'
                    tasks[task_name] = {'position': position, 'completed': False}
                    i += 1
                else:
                    print(f"Invalid task position {position}; it's either an obstacle or the start position.")
        else:
            # Generate random tasks
            while len(tasks) < num_tasks:
                x = random.randint(0, self.grid_size - 1)
                y = random.randint(0, self.grid_size - 1)
                position = (x, y)
                if (position not in self.obstacles and
                        position != start_pos and
                        self.grid[y][x] == 0):
                    task_name = f'Task {i}'
                    tasks[task_name] = {'position': position, 'completed': False}
                    i += 1
        return tasks
