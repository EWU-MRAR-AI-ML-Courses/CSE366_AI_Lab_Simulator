# examples/main_robot_nearest.py

import sys
import os

# Add the parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import pygame
import argparse
from modules.simulations.search_simulation import SearchSimulation
from modules.utils.constants import DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT

def main():
    parser = argparse.ArgumentParser(description='Robot Task Simulation (Nearest Task First)')
    parser.add_argument('--algorithm', type=str, default='astar',
                        choices=['dfs', 'bfs', 'ucs', 'astar'],
                        help='Search algorithm to use (default: astar)')
    parser.add_argument('--grid_size', type=int, default=16, help='Size of the grid (default: 16)')
    parser.add_argument('--num_tasks', type=int, default=5, help='Number of tasks (default: 5)')
    args = parser.parse_args()

    algorithm = args.algorithm
    grid_size = args.grid_size
    num_tasks = args.num_tasks

    pygame.init()
    screen = pygame.display.set_mode((DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Robot Task Simulation (Nearest Task First)")

    sim = SearchSimulation(screen, algorithm=algorithm, grid_size=grid_size, num_tasks=num_tasks, nearest_task=True)
    sim.run()

if __name__ == "__main__":
    main()
