# examples/main_maze_solver.py

import sys
import os

# Add the parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import pygame
import argparse
from modules.simulations.maze_simulation import MazeSimulation
from modules.utils.constants import DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT

def main():
    parser = argparse.ArgumentParser(description='Maze Solver Simulation')
    parser.add_argument('--algorithm', type=str, default='dfs',
                        choices=['dfs', 'bfs', 'ucs', 'astar'],
                        help='Search algorithm to use (default: dfs)')
    parser.add_argument('--maze_width', type=int, default=21, help='Width of the maze (odd number, default: 21)')
    parser.add_argument('--maze_height', type=int, default=21, help='Height of the maze (odd number, default: 21)')
    parser.add_argument('--complexity', type=float, default=0.75,
                        help='Maze complexity (0.0 to 1.0, default: 0.75)')
    parser.add_argument('--density', type=float, default=0.75,
                        help='Maze density (0.0 to 1.0, default: 0.75)')
    args = parser.parse_args()

    algorithm = args.algorithm
    maze_width = args.maze_width
    maze_height = args.maze_height

    # Ensure maze dimensions are odd numbers
    if maze_width % 2 == 0:
        maze_width += 1
    if maze_height % 2 == 0:
        maze_height += 1

    pygame.init()
    screen = pygame.display.set_mode((DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Maze Solver Simulation")

    sim = MazeSimulation(screen, algorithm=algorithm, maze_width=maze_width, maze_height=maze_height,
                         complexity=args.complexity, density=args.density)
    sim.run()

if __name__ == "__main__":
    main()
