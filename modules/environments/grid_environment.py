# modules/environments/grid_environment.py

import random


class GridEnvironment:
    def __init__(self, grid_size, room_start, room_end, door_position):
        self.grid_size = grid_size
        self.room_start = room_start
        self.room_end = room_end
        self.door_position = door_position
        self.grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
        self.obstacles = set()
        self.create_environment()

    def create_environment(self):
        # Build walls
        for x in range(self.room_start[0], self.room_end[0] + 1):
            for y in range(self.room_start[1], self.room_end[1] + 1):
                if (x == self.room_start[0] or x == self.room_end[0] or
                    y == self.room_start[1] or y == self.room_end[1]):
                    if (x, y) != self.door_position:  # Leave the door open
                        self.obstacles.add((x, y))
                        self.grid[y][x] = 1  # Mark as obstacle

    def generate_tasks(self, num_tasks, start_pos, task_positions=None):
        tasks = {}
        available_positions = set((x, y) for x in range(self.grid_size) for y in range(self.grid_size))
        available_positions -= self.obstacles
        available_positions.discard(start_pos)

        if task_positions is not None:
            for i, pos in enumerate(task_positions):
                if pos in available_positions:
                    tasks[f"Task {i + 1}"] = {'position': pos, 'completed': False}
                    available_positions.discard(pos)
                else:
                    raise ValueError(f"Invalid task position: {pos}")
        else:
            for i in range(num_tasks):
                pos = random.choice(list(available_positions))
                tasks[f"Task {i + 1}"] = {'position': pos, 'completed': False}
                available_positions.discard(pos)

        return tasks
