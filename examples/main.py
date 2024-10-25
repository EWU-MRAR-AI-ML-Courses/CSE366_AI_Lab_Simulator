# examples/main.py

import sys
import os

# Add the parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import pygame
from pygame.locals import RESIZABLE
from modules.utils.constants import DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT
from modules.simulations.search_simulation import SearchSimulation

import argparse
import ast


def main():
    parser = argparse.ArgumentParser(description='Robot Task Simulation')
    parser.add_argument('--algorithm', type=str, default='astar',
                        choices=['dfs', 'bfs', 'ucs', 'astar', 'hill_climbing', 'simulated_annealing'],
                        help='Search algorithm to use (default: astar)')
    parser.add_argument('--grid_size', type=int, default=16,
                        help='Size of the grid (default: 16)')
    parser.add_argument('--task_positions', type=str, default=None,
                        help='List of task positions in the format "[(x1,y1),(x2,y2),...]". If not provided, tasks are placed randomly.')

    args = parser.parse_args()

    algorithm = args.algorithm
    grid_size = args.grid_size
    task_positions = args.task_positions

    # Parse task_positions if provided
    if task_positions is not None:
        try:
            task_positions = ast.literal_eval(task_positions)
            if not isinstance(task_positions, list):
                raise ValueError
            # Ensure all positions are tuples of integers
            for pos in task_positions:
                if not (isinstance(pos, tuple) and len(pos) == 2 and
                        isinstance(pos[0], int) and isinstance(pos[1], int)):
                    raise ValueError
        except:
            print("Invalid task_positions format. Please provide a list of tuples, e.g., '[(1,1),(3,4),(5,5)]'")
            return
    else:
        task_positions = None  # Use random tasks if not specified

    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT), RESIZABLE)
    pygame.display.set_caption("Robot Task Simulation with Task Labels")

    # Run the search simulation
    sim = SearchSimulation(screen, algorithm=algorithm, grid_size=grid_size, task_positions=task_positions)
    sim.run()

if __name__ == "__main__":
    main()
