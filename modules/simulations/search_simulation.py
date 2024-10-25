# modules/simulations/search_simulation.py

import pygame
import sys
import os

# Add the parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)

from modules.simulations.simulation_base import SimulationBase
from modules.environments.grid_environment import GridEnvironment
from modules.agents.robot_agent import RobotAgent
from modules.utils.constants import (
    DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT, WHITE, BLACK, BLUE, GREEN, RED,
    PANEL_WIDTH, LIGHT_GRAY, GRAY
)

class SearchSimulation(SimulationBase):
    def __init__(self, screen, algorithm='astar', grid_size=16, num_tasks=5, nearest_task=False):
        super().__init__(screen)
        self.algorithm = algorithm
        self.grid_size = grid_size
        self.num_tasks = num_tasks
        self.nearest_task = nearest_task  # New parameter

        # Initialize fonts
        self.font_size = 20
        self.font_small = pygame.font.SysFont(None, self.font_size)
        self.font_medium = pygame.font.SysFont(None, int(self.font_size * 1.2))
        self.font_large = pygame.font.SysFont(None, int(self.font_size * 1.5))

        # Initialize clock for controlling animation speed
        self.clock = pygame.time.Clock()

        # Start and Reset buttons
        self.update_buttons()

        # Generate environment and agent
        self.reset_simulation()

        # Variables for UI
        self.mouse_grid_pos = None

    def update_buttons(self):
        window_width, window_height = self.screen.get_size()
        # Position the start button
        button_width = 100
        button_height = 40
        margin = 10  # Margin from the edges
        button_x = window_width - PANEL_WIDTH - button_width - margin
        button_y = window_height - button_height - margin
        self.start_button = Button(pygame.Rect(button_x, button_y, button_width, button_height),
                                   LIGHT_GRAY, "Start", BLACK, self.font_medium)

        # Position the reset button
        reset_button_x = button_x
        reset_button_y = button_y - button_height - margin
        self.reset_button = Button(pygame.Rect(reset_button_x, reset_button_y, button_width, button_height),
                                   LIGHT_GRAY, "Reset", BLACK, self.font_medium)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.is_clicked(event.pos):
                    self.animation_started = True
                    # Find initial path when start button is clicked
                    self.agent.find_initial_path(self.grid)
                    if not self.agent.path:
                        print(f"No path found using {self.algorithm.upper()}")
                        self.animation_started = False
                    else:
                        self.path_length = len(self.agent.path_traveled) + len(self.agent.path)
                elif self.reset_button.is_clicked(event.pos):
                    self.reset_simulation()

            # Exit on pressing ESC key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()

            # Capture mouse motion to update grid position under cursor
            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                # Check if mouse is over the grid area
                if mouse_x < self.grid_size * self.cell_size and mouse_y < self.grid_size * self.cell_size:
                    grid_x = mouse_x // self.cell_size
                    grid_y = mouse_y // self.cell_size
                    self.mouse_grid_pos = (int(grid_x), int(grid_y))
                else:
                    self.mouse_grid_pos = None  # Reset if mouse is outside the grid

    def reset_simulation(self):
        # Generate new environment and reset agent
        self.env = GridEnvironment(self.grid_size, num_tasks=self.num_tasks)
        self.grid = self.env.get_grid()
        self.tasks = self.env.get_tasks()
        # Keep a copy of all tasks and assign numbers
        self.all_tasks = self.tasks.copy()
        self.task_numbers = {task: i + 1 for i, task in enumerate(self.all_tasks)}
        # Set cell size
        self.cell_size = min((DEFAULT_WINDOW_WIDTH - PANEL_WIDTH) // self.grid_size,
                             DEFAULT_WINDOW_HEIGHT // self.grid_size)
        self.margin = 1
        # Set start position
        self.start_pos = self.env.get_start_position()
        # Initialize agent
        self.agent = RobotAgent(self.start_pos, self.tasks.copy(), algorithm=self.algorithm,
                                nearest_task=self.nearest_task)
        self.animation_started = False
        self.agent.path_traveled = []
        self.agent.path = []
        self.agent.completed_tasks = []
        self.path_length = None

    def update(self):
        # Handle window resize
        window_width, window_height = self.screen.get_size()
        grid_width = window_width - PANEL_WIDTH
        grid_height = window_height
        self.cell_size = min(grid_width // self.grid_size, grid_height // self.grid_size)
        self.margin = 1

        # Update fonts based on cell_size
        self.font_size = int(self.cell_size // 2)
        self.font_small = pygame.font.SysFont(None, self.font_size)
        self.font_medium = pygame.font.SysFont(None, int(self.font_size * 1.2))
        self.font_large = pygame.font.SysFont(None, int(self.font_size * 1.5))

        self.start_button.font = self.font_medium
        self.reset_button.font = self.font_medium

        # Update button positions on resize
        self.update_buttons()

        if self.animation_started:
            self.agent.move()
            # Update path length
            self.path_length = len(self.agent.path_traveled) + len(self.agent.path)
            # Stop the simulation when all tasks are completed
            if len(self.agent.completed_tasks) == len(self.tasks):
                self.animation_started = False

    def draw(self):
        self.screen.fill(WHITE)
        self.draw_environment()
        pygame.display.flip()

    def draw_environment(self):
        CELL_SIZE = self.cell_size
        MARGIN = self.margin

        # Draw the grid
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                rect = pygame.Rect(
                    x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE - MARGIN, CELL_SIZE - MARGIN
                )
                if self.grid[y][x] == 1:
                    pygame.draw.rect(self.screen, BLACK, rect)
                else:
                    pygame.draw.rect(self.screen, GRAY, rect)

        # Draw all tasks (both completed and uncompleted)
        for task in self.all_tasks:
            tx, ty = task
            rect = pygame.Rect(
                tx * CELL_SIZE, ty * CELL_SIZE, CELL_SIZE - MARGIN, CELL_SIZE - MARGIN
            )
            if task in self.agent.completed_tasks:
                pygame.draw.rect(self.screen, GREEN, rect)
            else:
                pygame.draw.rect(self.screen, RED, rect)
            # Draw task number
            task_number = self.task_numbers[task]
            text_surface = self.font_small.render(str(task_number), True, BLACK)
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)

        # Draw right panel background
        panel_rect = pygame.Rect(self.grid_size * CELL_SIZE, 0, PANEL_WIDTH, self.screen.get_height())
        pygame.draw.rect(self.screen, WHITE, panel_rect)

        # Draw UI elements on the right panel
        self.draw_ui(panel_rect.x + 20, 20)

        # Draw Start and Reset buttons
        self.start_button.draw(self.screen)
        self.reset_button.draw(self.screen)

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

        # Display Path Length
        if self.path_length is not None:
            path_length_text = self.font_small.render(f"Path Length: {self.path_length}", True, BLACK)
            self.screen.blit(path_length_text, (panel_x, y_offset))
            y_offset += int(self.font_size)

        # Display Algorithm Used
        algorithm_text = self.font_small.render(f"Algorithm: {self.algorithm.upper()}", True, BLACK)
        self.screen.blit(algorithm_text, (panel_x, y_offset))
        y_offset += int(self.font_size)

        # Display Tasks Remaining
        tasks_remaining = len(self.tasks) - len(self.agent.completed_tasks)
        tasks_remaining_text = self.font_small.render(f"Tasks Remaining: {tasks_remaining}", True, BLACK)
        self.screen.blit(tasks_remaining_text, (panel_x, y_offset))
        y_offset += int(self.font_size)

        # Display Mouse Grid Position
        if self.mouse_grid_pos is not None:
            mouse_pos_text = self.font_small.render(f"Cursor Position: {self.mouse_grid_pos}", True, BLACK)
            self.screen.blit(mouse_pos_text, (panel_x, y_offset))
            y_offset += int(self.font_size)
        else:
            y_offset += int(self.font_size)

    def draw_agent(self):
        # Draw agent on top of the grid
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
