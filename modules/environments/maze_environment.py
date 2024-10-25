# modules/environments/maze_environment.py

import random

class MazeEnvironment:
    def __init__(self, width, height, complexity=0.75, density=0.75):
        self.width = width  # Number of cells horizontally
        self.height = height  # Number of cells vertically
        self.grid = [[1 for _ in range(width)] for _ in range(height)]  # Initialize grid with walls
        self.visited = [[False for _ in range(width)] for _ in range(height)]
        self.complexity = complexity
        self.density = density
        self.generate_maze()
        self.add_additional_paths()
        
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

    def add_additional_paths(self):
        # Adjust complexity and density relative to maze size
        complexity = int(self.complexity * (5 * (self.width + self.height)))
        density = int(self.density * ((self.width // 2) * (self.height // 2)))

        for i in range(density):
            x = random.randrange(1, self.width - 1, 2)
            y = random.randrange(1, self.height - 1, 2)
            self.grid[y][x] = 0
            for j in range(complexity):
                neighbors = []
                if x > 1:
                    neighbors.append((x - 2, y))
                if x < self.width - 2:
                    neighbors.append((x + 2, y))
                if y > 1:
                    neighbors.append((x, y - 2))
                if y < self.height - 2:
                    neighbors.append((x, y + 2))
                if neighbors:
                    nx, ny = random.choice(neighbors)
                    if self.grid[ny][nx] == 1:
                        self.grid[ny][nx] = 0
                        self.grid[ny + (y - ny) // 2][nx + (x - nx) // 2] = 0
                        x, y = nx, ny

    def get_grid(self):
        return self.grid
