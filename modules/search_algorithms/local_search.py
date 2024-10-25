# modules/search_algorithms/local_search.py

import random
import math

# Existing local search algorithms

def hill_climbing(start, goal, grid, blocked_positions, grid_size):
    current = start
    path = [current]

    while current != goal:
        neighbors = get_neighbors(current, grid, blocked_positions, grid_size)
        if not neighbors:
            return None  # No path found
        next_node = min(neighbors, key=lambda n: heuristic(n, goal))
        if heuristic(next_node, goal) >= heuristic(current, goal):
            return path  # Local maximum reached
        current = next_node
        path.append(current)
    return path

def simulated_annealing(start, goal, grid, blocked_positions, grid_size):
    current = start
    path = [current]
    temperature = 1000
    cooling_rate = 0.99

    while current != goal and temperature > 0.1:
        neighbors = get_neighbors(current, grid, blocked_positions, grid_size)
        if not neighbors:
            return None  # No path found
        next_node = random.choice(neighbors)
        delta_e = heuristic(current, goal) - heuristic(next_node, goal)
        if delta_e > 0 or math.exp(delta_e / temperature) > random.random():
            current = next_node
            path.append(current)
        temperature *= cooling_rate
    if current == goal:
        return path
    else:
        return None  # Failed to find a path

def heuristic(a, b):
    # Using Manhattan distance as heuristic
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def get_neighbors(position, grid, blocked_positions, grid_size):
    x, y = position
    neighbors = []
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Left, Right, Up, Down

    for move in moves:
        nx, ny = x + move[0], y + move[1]
        if 0 <= nx < grid_size and 0 <= ny < grid_size:
            if grid[ny][nx] == 0 and (nx, ny) not in blocked_positions:
                neighbors.append((nx, ny))
    return neighbors

# Genetic Algorithm for 8-Queens problem

# Population parameters
POPULATION_SIZE = 100
MUTATION_RATE = 0.1

def generate_individual():
    """Generates an individual with random queen positions."""
    return [random.randint(0, 7) for _ in range(8)]

def fitness(individual):
    """Calculates the fitness score. Higher is better."""
    conflicts = 0
    for i in range(len(individual)):
        for j in range(i + 1, len(individual)):
            if individual[i] == individual[j] or abs(individual[i] - individual[j]) == abs(i - j):
                conflicts += 1
    return 28 - conflicts  # 28 is the maximum number of non-conflicting pairs

def crossover(parent1, parent2):
    """Performs crossover between two parents to create an offspring."""
    point = random.randint(0, 7)
    return parent1[:point] + parent2[point:]

def mutate(individual):
    """Mutates an individual randomly."""
    if random.random() < MUTATION_RATE:
        index = random.randint(0, 7)
        individual[index] = random.randint(0, 7)

def select_population(population):
    """Selects the population based on fitness."""
    population = sorted(population, key=lambda x: fitness(x), reverse=True)
    return population[:POPULATION_SIZE]
