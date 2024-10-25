# examples/main_8_queen.py

import sys
import os
import pygame
import random
import time
import argparse

# Add the parent directory to sys.path to import modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from modules.search_algorithms import local_search

# Constants for Pygame visualization
WINDOW_SIZE = 400
INFO_WIDTH = 200
TOTAL_WIDTH = WINDOW_SIZE + INFO_WIDTH
CELL_SIZE = WINDOW_SIZE // 8
LIGHT_GRAY = (211, 211, 211)
DARK_BLUE = (30, 144, 255)
PURPLE = (138, 43, 226)
WHITE = (255, 255, 255)
DARK_GRAY = (169, 169, 169)
FONT_COLOR = (50, 50, 50)

def draw_board(screen, font, individual):
    """Draws the chessboard and the queens."""
    for y in range(8):
        for x in range(8):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            color = LIGHT_GRAY if (x + y) % 2 == 0 else DARK_BLUE
            pygame.draw.rect(screen, color, rect)

            # Draw the queens
            if individual[x] == y:
                queen_text = f"Q{x + 1}"
                text_surface = font.render(queen_text, True, PURPLE)
                text_rect = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)

def draw_info_panel(screen, font, generation, individual, max_generations):
    """Draws the information panel showing the generation and queens' status."""
    panel_rect = pygame.Rect(WINDOW_SIZE, 0, INFO_WIDTH, WINDOW_SIZE)
    pygame.draw.rect(screen, DARK_GRAY, panel_rect)
    
    # Draw generation number
    generation_text = f"Generation: {generation}/{max_generations}"
    generation_surface = font.render(generation_text, True, WHITE)
    screen.blit(generation_surface, (WINDOW_SIZE + 10, 10))

    # Draw fitness score
    fitness_score = local_search.fitness(individual)
    fitness_text = f"Fitness: {fitness_score}/28"
    fitness_surface = font.render(fitness_text, True, WHITE)
    screen.blit(fitness_surface, (WINDOW_SIZE + 10, 40))

    # Draw queens' positions
    for i, pos in enumerate(individual):
        queen_text = f"Q{i + 1}: Row {pos + 1}"
        queen_surface = font.render(queen_text, True, WHITE)
        screen.blit(queen_surface, (WINDOW_SIZE + 10, 70 + i * 30))

def main():
    # Add argument parsing
    parser = argparse.ArgumentParser(description='8-Queens Genetic Algorithm Simulation')
    parser.add_argument('--max_generations', type=int, default=1000, help='Maximum number of generations')
    parser.add_argument('--delay', type=float, default=0.1, help='Delay between generations in seconds')
    args = parser.parse_args()

    MAX_GENERATIONS = args.max_generations
    DELAY = args.delay

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((TOTAL_WIDTH, WINDOW_SIZE))
    pygame.display.set_caption("8-Queens Genetic Algorithm")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    # Genetic Algorithm parameters
    population = [local_search.generate_individual() for _ in range(local_search.POPULATION_SIZE)]
    generation = 0
    running = True
    solution_found = False

    while running and generation < MAX_GENERATIONS:
        # Handle events to exit the simulation
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Select the best individuals
        population = local_search.select_population(population)

        # Check for a solution
        best_individual = population[0]
        if local_search.fitness(best_individual) == 28:
            print(f"Solution found in generation {generation}: {best_individual}")
            solution_found = True
            running = False  # Exit the loop when solution is found

        # Generate next generation
        next_generation = []
        while len(next_generation) < local_search.POPULATION_SIZE:
            parent1 = random.choice(population)
            parent2 = random.choice(population)
            child = local_search.crossover(parent1, parent2)
            local_search.mutate(child)
            next_generation.append(child)

        population = next_generation
        generation += 1

        # Draw the best individual (visualize the board and info panel)
        screen.fill(WHITE)
        draw_board(screen, font, best_individual)
        draw_info_panel(screen, font, generation, best_individual, MAX_GENERATIONS)
        pygame.display.flip()

        # Control animation speed
        clock.tick(10)  # Set to 10 FPS
        time.sleep(DELAY)  # Add a short delay (in seconds)

    # After the loop ends
    if solution_found:
        # Display the solution
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            screen.fill(WHITE)
            draw_board(screen, font, best_individual)
            draw_info_panel(screen, font, generation, best_individual, MAX_GENERATIONS)
            pygame.display.flip()
            clock.tick(10)
    else:
        # Display no solution message
        screen.fill(WHITE)
        font_large = pygame.font.Font(None, 36)
        text_surface = font_large.render("No solution found!", True, FONT_COLOR)
        text_rect = text_surface.get_rect(center=(TOTAL_WIDTH // 2, WINDOW_SIZE // 2))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()

        # Wait for user to exit
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
