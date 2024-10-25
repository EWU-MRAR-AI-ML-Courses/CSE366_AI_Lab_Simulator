# modules/simulations/maze_simulation.py

import pygame
import sys
import os

# Add the parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)

from modules.simulations.simulation_base import SimulationBase
from modules.environments.maze_environment import MazeEnvironment
from modules.agents.maze_agent import MazeAgent
from modules.utils.constants import (
    DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT, WHITE, BLACK, BLUE, GREEN, RED,
    PANEL_WIDTH, LIGHT_GRAY, BLACK, GRAY
)

class MazeSimulation(SimulationBase):
    def __init__(self, screen, algorithm='dfs', maze_width=21, maze_height=21):
        super().__init__(screen)
        self.algorithm = algorithm
        self.maze_width = maze_width
        self.maze_height = maze_height

        # Initialize fonts
        self.font_size = 20
        self.font_small = pygame.font.SysFont(None, self.font_size)
        self.font_medium = pygame.font.SysFont(None, int(self.font_size * 1.2))
        self.font_large = pygame.font.SysFont(None, int(self.font_size * 1.5))

        # Initialize clock for controlling animation speed
        self.clock = pygame.time.Clock()

        # Start button
        self.update_start_button()

        # Generate maze
        self.maze_env = MazeEnvironment(self.maze_width, self.maze_height)
        self.grid = self.maze_env.get_grid()

        # Set cell size
        self.cell_size = min((DEFAULT_WINDOW_WIDTH - PANEL_WIDTH) // self.maze_width, DEFAULT_WINDOW_HEIGHT // self.maze_height)
        self.margin = 1

        # Set start and goal positions
        self.start_pos = (1, 0)
        self.goal_pos = (self.maze_width - 2, self.maze_height - 1)

        # Initialize agent
        self.agent = MazeAgent(self.start_pos, self.goal_pos, algorithm=self.algorithm)
        self.animation_started = False

        # Variables for UI
        self.mouse_grid_pos = None

    def update_start_button(self):
        window_width, window_height = self.screen.get_size()
        # Position the start button at the bottom right corner
        button_width = 100
        button_height = 40
        margin = 10  # Margin from the edges
        button_x = window_width - PANEL_WIDTH - button_width - margin
        button_y = window_height - button_height - margin
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        self.start_button = Button(button_rect, LIGHT_GRAY, "Start", BLACK, self.font_medium)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.is_clicked(event.pos):
                    self.animation_started = True
                    # Find path when start button is clicked
                    self.agent.find_path(self.grid)
                    if not self.agent.path:
                        print(f"No path found using {self.algorithm.upper()}")
                        self.quit()

            # Exit on pressing ESC key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()

            # Capture mouse motion to update grid position under cursor
            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                # Check if mouse is over the grid area
                if mouse_x < self.maze_width * self.cell_size and mouse_y < self.maze_height * self.cell_size:
                    grid_x = mouse_x // self.cell_size
                    grid_y = mouse_y // self.cell_size
                    self.mouse_grid_pos = (int(grid_x), int(grid_y))
                else:
                    self.mouse_grid_pos = None  # Reset if mouse is outside the grid

    def update(self):
        # Handle window resize
        window_width, window_height = self.screen.get_size()
        grid_width = window_width - PANEL_WIDTH
        grid_height = window_height
        self.cell_size = min(grid_width // self.maze_width, grid_height // self.maze_height)
        self.margin = 1

        # Update fonts based on cell_size
        self.font_size = int(self.cell_size // 2)
        self.font_small = pygame.font.SysFont(None, self.font_size)
        self.font_medium = pygame.font.SysFont(None, int(self.font_size * 1.2))
        self.font_large = pygame.font.SysFont(None, int(self.font_size * 1.5))

        self.start_button.font = self.font_medium

        # Update start button position on resize
        self.update_start_button()

        if self.animation_started:
            self.agent.move()
            # Stop the simulation when the agent reaches the goal
            if self.agent.position == self.goal_pos:
                self.animation_started = False

    def draw(self):
        self.screen.fill(WHITE)
        self.draw_environment()
        pygame.display.flip()

    def draw_environment(self):
        CELL_SIZE = self.cell_size
        MARGIN = self.margin

        # Draw the maze grid
        for y in range(self.maze_height):
            for x in range(self.maze_width):
                rect = pygame.Rect(
                    x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE - MARGIN, CELL_SIZE - MARGIN
                )
                if self.grid[y][x] == 1:
                    pygame.draw.rect(self.screen, BLACK, rect)
                else:
                    pygame.draw.rect(self.screen, GRAY, rect)

        # Draw the goal
        gx, gy = self.goal_pos
        rect = pygame.Rect(
            gx * CELL_SIZE, gy * CELL_SIZE, CELL_SIZE - MARGIN, CELL_SIZE - MARGIN
        )
        pygame.draw.rect(self.screen, RED, rect)

        # Draw the path traveled
        for pos in self.agent.path_traveled:
            x, y = pos
            rect = pygame.Rect(
                x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE - MARGIN, CELL_SIZE - MARGIN
            )
            pygame.draw.rect(self.screen, GREEN, rect)

        # Draw right panel background
        panel_rect = pygame.Rect(self.maze_width * CELL_SIZE, 0, PANEL_WIDTH, self.screen.get_height())
        pygame.draw.rect(self.screen, WHITE, panel_rect)

        # Draw UI elements on the right panel
        self.draw_ui(panel_rect.x + 20, 20)

        # Draw Start button
        self.start_button.draw(self.screen)

        # Draw the agent
        self.draw_agent()

    def draw_ui(self, panel_x, y_offset):
        # Display Agent Status
        status_text = self.font_medium.render("Agent Status", True, BLACK)
        self.screen.blit(status_text, (panel_x, y_offset))
        y_offset += int(self.font_size * 1.5)

        position_text = self.font_small.render(f"Position: {self.agent.position}", True, BLACK)
        self.screen.blit(position_text, (panel_x, y_offset))
        y_offset += int(self.font_size)

        if self.animation_started:
            status_text = self.font_small.render("Status: Moving", True, BLACK)
        else:
            status_text = self.font_small.render("Status: Idle", True, BLACK)
        self.screen.blit(status_text, (panel_x, y_offset))
        y_offset += int(self.font_size * 1.5)

        # Display Mouse Grid Position
        if self.mouse_grid_pos is not None:
            mouse_pos_text = self.font_small.render(f"Cursor Position: {self.mouse_grid_pos}", True, BLACK)
            self.screen.blit(mouse_pos_text, (panel_x, y_offset))
            y_offset += int(self.font_size * 1.5)
        else:
            y_offset += int(self.font_size * 1.5)

    def draw_agent(self):
        # Draw agent on top of the maze
        CELL_SIZE = self.cell_size
        MARGIN = self.margin
        x, y = self.agent.position
        rect = pygame.Rect(
            x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE - MARGIN, CELL_SIZE - MARGIN
        )
        pygame.draw.rect(self.screen, BLUE, rect)

    def run(self):
        """Main loop of the simulation."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(5)  # Set to 5 FPS to slow down the animation

    def quit(self):
        """Exit the simulation."""
        self.running = False

class Button:
    def __init__(self, rect, color, text, text_color, font):
        self.rect = rect
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = font

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
