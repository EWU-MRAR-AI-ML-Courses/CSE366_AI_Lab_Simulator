# modules/agents/robot_agent.py

from modules.search_algorithms.uninformed_search import bfs
from modules.search_algorithms.informed_search import astar

class RobotAgent:
    def __init__(self, start_position, tasks, algorithm='astar', nearest_task=False):
        self.position = start_position
        self.tasks = tasks.copy()  # Original list of tasks
        self.algorithm = algorithm
        self.nearest_task = nearest_task  # Determines behavior
        self.path = []
        self.path_traveled = []
        self.completed_tasks = []
        self.current_task_index = 0  # For task order-based behavior
        self.grid = None  # Will be set when find_initial_path is called
        self.current_task = None

    def find_initial_path(self, grid):
        self.grid = grid
        if self.nearest_task:
            # Start by finding a path to the nearest task
            self.find_path_to_nearest_task()
        else:
            # Start by finding a path to the first task in order
            if self.current_task_index < len(self.tasks):
                self.current_task = self.tasks[self.current_task_index]
                self.find_path_to_current_task()

    def find_path_to_current_task(self):
        blocked_positions = set()
        grid_size = len(self.grid)
        if self.algorithm == 'dfs':
            from modules.search_algorithms.uninformed_search import dfs
            self.path = dfs(self.position, self.current_task, self.grid, blocked_positions, grid_size)
        elif self.algorithm == 'bfs':
            self.path = bfs(self.position, self.current_task, self.grid, blocked_positions, grid_size)
        elif self.algorithm == 'ucs':
            from modules.search_algorithms.uninformed_search import ucs
            self.path = ucs(self.position, self.current_task, self.grid, blocked_positions, grid_size)
        elif self.algorithm == 'astar':
            self.path = astar(self.position, self.current_task, self.grid, blocked_positions, grid_size)
        else:
            raise ValueError(f"Unknown algorithm: {self.algorithm}")

    def find_path_to_nearest_task(self):
        if not self.tasks:
            return False  # No tasks left

        # Calculate distances to uncompleted tasks
        task_distances = []
        for task in self.tasks:
            if task not in self.completed_tasks:
                distance = self.manhattan_distance(self.position, task)
                task_distances.append((distance, task))

        if not task_distances:
            return False  # All tasks completed

        # Find the nearest task
        task_distances.sort()
        self.current_task = task_distances[0][1]

        # Plan path to the nearest task
        self.find_path_to_current_task()

    def move(self):
        if self.path:
            next_position = self.path.pop(0)
            self.position = next_position
            self.path_traveled.append(self.position)
            # Check if reached the current task
            if self.position == self.current_task:
                self.completed_tasks.append(self.current_task)
                self.path = []
                # Decide next action
                if self.nearest_task:
                    # Find path to the next nearest task
                    if len(self.completed_tasks) < len(self.tasks):
                        self.find_path_to_nearest_task()
                else:
                    # Move to the next task in order
                    self.current_task_index += 1
                    if self.current_task_index < len(self.tasks):
                        self.current_task = self.tasks[self.current_task_index]
                        self.find_path_to_current_task()
        else:
            # No path, agent is idle or tasks are completed
            pass

    def manhattan_distance(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        return abs(x1 - x2) + abs(y1 - y2)
