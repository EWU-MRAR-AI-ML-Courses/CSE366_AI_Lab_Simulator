# modules/simulations/search_simulation.py

import pygame
from pygame.locals import RESIZABLE
from collections import deque
import sys
import os

# Add the parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)

from modules.agents.robot_agent import RobotAgent
from modules.environments.grid_environment import GridEnvironment
from modules.utils.constants import (
    PANEL_WIDTH, WHITE, GRAY, GREEN, BLUE, PURPLE, BLACK, YELLOW, BROWN, LIGHT_GRAY
)

from .simulation_base import SimulationBase


class SearchSimulation(SimulationBase):
    def __init__(self, screen, grid_size=16, algorithm='astar', task_positions=None):
        super().__init__(screen)
        self.grid_size = grid_size
        self.algorithm = algorithm
        self.task_positions = task_positions

        # Initialize simulation variables
        self.mouse_grid_pos = None

        # Initialize fonts
        self.font_size = 20
        self.font_small = pygame.font.SysFont(None, self.font_size)
        self.font_medium = pygame.font.SysFont(None, int(self.font_size * 1.2))
        self.font_large = pygame.font.SysFont(None, int(self.font_size * 1.5))

        # Start button
        self.update_start_button()

        # Initialize environment and robot
        self.initialize_environment()

        # Initialize robot
        self.robot = RobotAgent(self.start_pos, algorithm=self.algorithm)

        # Set animation_started to False so the robot waits for the Start button
        self.animation_started = False

        # Calculate initial path (but don't start moving yet)
        self.calculate_initial_path()

    def initialize_environment(self):
        # Define room and door positions
        room_start = (4, 4)
        room_end = (self.grid_size - 5, self.grid_size - 5)
        door_position = (self.grid_size // 2, room_start[1])  # Door at the top wall

        # Create grid and obstacles
        env = GridEnvironment(self.grid_size, room_start, room_end, door_position)
        self.grid = env.grid
        self.obstacles = env.obstacles

        # Starting position
        self.start_pos = (self.grid_size // 2, self.grid_size // 2)

        # Generate tasks
        if self.task_positions is not None:
            num_tasks = len(self.task_positions)
        else:
            num_tasks = 3  # Default number of tasks

        self.tasks = env.generate_tasks(num_tasks, self.start_pos, self.task_positions)
        self.task_order = deque(self.tasks.keys())

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

    def calculate_initial_path(self):
        if self.task_order:
            self.robot.current_task = self.task_order[0]  # Do not pop yet
            current_task = self.tasks[self.robot.current_task]

            # Block uncompleted tasks (excluding current task)
            blocked_positions = set(
                task_info['position'] for task_name, task_info in self.tasks.items()
                if not task_info['completed'] and task_name != self.robot.current_task
            )

            self.robot.path = self.robot.find_path(
                self.robot.position, current_task['position'], self.grid, blocked_positions, self.grid_size
            )

            if self.robot.path is None:
                print(f"No path found to {self.robot.current_task} using {self.algorithm.upper()}")
                self.quit()
        else:
            self.robot.path = []
            self.robot.current_task = None

    def reset_simulation(self):
        # Initialize environment
        self.initialize_environment()

        # Initialize robot
        self.robot = RobotAgent(self.start_pos, algorithm=self.algorithm)

        # Reset animation state
        self.animation_started = True  # Start the animation immediately upon reset

        # Calculate initial path
        self.calculate_initial_path()

        # Pop the first task now that simulation is starting
        if self.task_order:
            self.task_order.popleft()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.is_clicked(event.pos):
                    # Reset and restart the simulation
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

        # Update start button position on resize
        self.update_start_button()

        # Update robot
        self.update_robot()

    def draw(self):
        self.screen.fill(WHITE)
        self.draw_environment()
        pygame.display.flip()

    def draw_environment(self):
        CELL_SIZE = self.cell_size
        MARGIN = self.margin

        # Draw grid
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                rect = pygame.Rect(
                    x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE - MARGIN, CELL_SIZE - MARGIN
                )
                # Draw obstacles
                if self.grid[y][x] == 1:
                    pygame.draw.rect(self.screen, BROWN, rect)
                else:
                    pygame.draw.rect(self.screen, GRAY, rect)

        # Draw tasks
        for task_name, task_info in self.tasks.items():
            x, y = task_info['position']
            rect = pygame.Rect(
                x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE - MARGIN, CELL_SIZE - MARGIN
            )
            color = GREEN if task_info['completed'] else PURPLE
            pygame.draw.rect(self.screen, color, rect)

            # Label the task with its number
            task_number = ''.join(filter(str.isdigit, task_name))
            number_text = self.font_small.render(task_number, True, BLACK)
            number_rect = number_text.get_rect(center=rect.center)
            self.screen.blit(number_text, number_rect)

        # Draw the path traversed by the robot
        for pos in self.robot.path_traveled:
            x, y = pos
            rect = pygame.Rect(
                x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE - MARGIN, CELL_SIZE - MARGIN
            )
            pygame.draw.rect(self.screen, YELLOW, rect)

        # Draw right panel background
        panel_rect = pygame.Rect(self.grid_size * CELL_SIZE, 0, PANEL_WIDTH, self.screen.get_height())
        pygame.draw.rect(self.screen, WHITE, panel_rect)

        # Draw UI elements on the right panel
        self.draw_ui(panel_rect.x + 20, 20)

        # Draw Start button
        self.start_button.draw(self.screen)

        # Draw robot
        self.draw_robot()

    def draw_ui(self, panel_x, y_offset):
        # Display Robot Status
        status_text = self.font_medium.render("Robot Status", True, BLACK)
        self.screen.blit(status_text, (panel_x, y_offset))
        y_offset += int(self.font_size * 1.5)

        position_text = self.font_small.render(f"Position: {self.robot.position}", True, BLACK)
        self.screen.blit(position_text, (panel_x, y_offset))
        y_offset += int(self.font_size)

        if self.robot.current_task and self.animation_started:
            task_text = self.font_small.render(f"Moving to {self.robot.current_task}", True, BLACK)
        elif not self.animation_started:
            task_text = self.font_small.render("Press Start to Begin", True, BLACK)
        else:
            task_text = self.font_small.render("No more tasks", True, BLACK)
        self.screen.blit(task_text, (panel_x, y_offset))
        y_offset += int(self.font_size * 1.5)

        # Display Mouse Grid Position
        if self.mouse_grid_pos is not None:
            mouse_pos_text = self.font_small.render(f"Cursor Position: {self.mouse_grid_pos}", True, BLACK)
            self.screen.blit(mouse_pos_text, (panel_x, y_offset))
            y_offset += int(self.font_size * 1.5)
        else:
            y_offset += int(self.font_size * 1.5)

        # Display Task Status
        task_status_text = self.font_medium.render("Task Status", True, BLACK)
        self.screen.blit(task_status_text, (panel_x, y_offset))
        y_offset += int(self.font_size * 1.5)

        for task_name in self.tasks.keys():
            status = "Completed" if self.tasks[task_name]['completed'] else "Pending"
            text = self.font_small.render(f"{task_name}: {status}", True, BLACK)
            self.screen.blit(text, (panel_x, y_offset))
            y_offset += int(self.font_size)

    def update_robot(self):
        if self.animation_started:
            # Move the robot
            self.robot.move()

            # Check if task is completed
            if self.robot.current_task and self.robot.position == self.tasks[self.robot.current_task]['position']:
                self.tasks[self.robot.current_task]['completed'] = True
                self.robot.tasks_completed.append(self.robot.current_task)
                if self.task_order:
                    self.robot.current_task = self.task_order.popleft()
                    current_task = self.tasks[self.robot.current_task]

                    # Block uncompleted tasks (excluding current task)
                    blocked_positions = set(
                        task_info['position'] for task_name, task_info in self.tasks.items()
                        if not task_info['completed'] and task_name != self.robot.current_task
                    )

                    self.robot.path = self.robot.find_path(
                        self.robot.position, current_task['position'], self.grid, blocked_positions, self.grid_size
                    )
                    if self.robot.path is None:
                        print(f"No path found to {self.robot.current_task} using {self.algorithm.upper()}")
                        self.quit()
                else:
                    self.robot.path = []
                    self.robot.current_task = None

            # Stop animation if no path remains
            if not self.robot.path and not self.robot.current_task:
                self.animation_started = False

    def draw_robot(self):
        # Draw robot on top of the path
        CELL_SIZE = self.cell_size
        MARGIN = self.margin
        x, y = self.robot.position
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
