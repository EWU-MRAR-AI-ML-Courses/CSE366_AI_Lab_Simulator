# modules/environments/maze_environment.py

import random

class MazeEnvironment:
    def __init__(self, width, height):
        self.width = width  # Number of cells horizontally
        self.height = height  # Number of cells vertically
        self.grid = [[1 for _ in range(width)] for _ in range(height)]  # Initialize grid with walls
        self.visited = [[False for _ in range(width)] for _ in range(height)]
        self.generate_maze()
    
    def generate_maze(self):
        def carve_passages_from(cx, cy):
            directions = [('N', (0, -1)), ('S', (0, 1)), ('E', (1, 0)), ('W', (-1, 0))]
            random.shuffle(directions)
            self.visited[cy][cx] = True
            self.grid[cy][cx] = 0  # Mark as passage

            for direction, (dx, dy) in directions:
                nx, ny = cx + dx * 2, cy + dy * 2
                if 0 <= nx < self.width and 0 <= ny < self.height and not self.visited[ny][nx]:
                    self.grid[cy + dy][cx + dx] = 0  # Remove wall between cells
                    carve_passages_from(nx, ny)

        # Start maze generation from the top-left corner (1,1)
        carve_passages_from(1, 1)

        # Ensure entrance and exit
        self.grid[0][1] = 0  # Entrance
        self.grid[self.height - 1][self.width - 2] = 0  # Exit

    def get_grid(self):
        return self.grid
