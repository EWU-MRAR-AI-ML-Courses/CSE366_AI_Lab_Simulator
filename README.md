# CSE366 AI Lab Simulator

CSE366 AI Lab Simulator is a comprehensive Python library designed for the **CSE 366 Artificial Intelligence Lab** course. It provides simulation tools for various AI concepts, including search algorithms, local search, constraint satisfaction problems (CSP), adversarial search, and reinforcement learning. This library is intended to aid in teaching and understanding AI algorithms through visual simulations.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the Simulation](#running-the-simulation)
  - [Command-Line Arguments](#command-line-arguments)
- [Directory Structure](#directory-structure)
- [Examples](#examples)
- [Future Extensions](#future-extensions)
- [License](#license)
- [Contact](#contact)

---

## Features

- **Search Algorithms**: Implementations of DFS, BFS, UCS, A*, Hill Climbing, and Simulated Annealing.
- **Robot Movement Simulation**: Visualize robot movement in a grid environment while performing tasks.
- **Extensible Framework**: Designed to be extended for CSP, adversarial tasks, and reinforcement learning simulations.
- **User-Friendly Interface**: Interact with simulations through a graphical interface built with Pygame.
- **Customization**: Easily modify grid size, task positions, and algorithms via command-line arguments.

---

## Installation

### Prerequisites

- **Python 3.6 or higher**
- **Pygame library**

### Steps

1. **Clone the Repository**

   ```
   git clone https://github.com/your_username/CSE366_AI_Lab_Simulator.git
   cd CSE366_AI_Lab_Simulator
   ```

2. **Install Dependencies**

Install the required Python packages using **pip**:

```
pip install -r requirements.txt
```
*Note: Ensure that you have the latest version of pip installed.*

---

## Directory Structure
The project is organized as follows:

```
CSE366_AI_Lab_Simulator/
├── README.md
├── LICENSE
├── requirements.txt
├── modules/
│   ├── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── robot_agent.py
│   │   └── maze_agent.py
│   ├── environments/
│   │   ├── __init__.py
│   │   ├── grid_environment.py
│   │   └── maze_environment.py
│   ├── search_algorithms/
│   │   ├── __init__.py
│   │   ├── uninformed_search.py
│   │   ├── informed_search.py
│   │   └── local_search.py
│   ├── simulations/
│   │   ├── __init__.py
│   │   ├── simulation_base.py
│   │   ├── search_simulation.py
│   │   └── maze_simulation.py
│   └── utils/
│       ├── __init__.py
│       └── constants.py
└── examples/
    ├── __init__.py
    ├── main.py
    ├── main_8_queen.py
    └── main_maze_solver.py

```

The simulator's codebase is organized into the following directories:

* **modules/**: Contains all the core modules of the simulator.
* **agents/**: Agent classes like `RobotAgent`.
* **environments/**: Environment classes like `GridEnvironment`.
* **search_algorithms/**: Implementations of various search algorithms.
* **simulations/**: Simulation classes for different AI problems.
* **utils/**: Utility modules and constants.
* **examples/**: Contains example scripts demonstrating how to use the library.
---

## Examples

---
## Robot Task Simulator

### Running Task Order-Based Simulation
To run the task order-based simulation:

```
cd examples
python main.py --grid_size 16 --num_tasks 5 --algorithm astar
```

### Running Nearest Task First Simulation
To run the nearest task first simulation:

```
cd examples
python main_robot_nearest.py --grid_size 16 --num_tasks 5 --algorithm astar
```

### Command-Line Arguments
* --algorithm: Specify the search algorithm (dfs, bfs, ucs, or astar).
* --grid_size: Set the size of the grid (default is 16).
* --num_tasks: Set the number of tasks in the environment (default is 5).

### Example Usage
Run a simulation with BFS, a grid size of 20, and 10 tasks:

```
python main.py --algorithm bfs --grid_size 20 --num_tasks 10
```

Run the nearest task simulation with A*, a grid size of 25, and 8 tasks:

```
python main_robot_nearest.py --algorithm astar --grid_size 25 --num_tasks 8
```

---
## Running the Maze Solver Simulation

### Run the Simulation

Navigate to the examples directory and run:

```
cd examples
python main_maze_solver.py
```

### Select Algorithm

```
python main_maze_solver.py --algorithm bfs
```

### Set Maze Dimensions

```
python main_maze_solver.py --maze_width 31 --maze_height 31
```

### Adjust Complexity and Density

```
python main_maze_solver.py --complexity 0.9 --density 0.9
```

### Example Usage

```
python main_maze_solver.py --algorithm astar --maze_width 25 --maze_height 25 --complexity 0.8 --density 0.8
```

### Interacting with the Simulation
* Start Button: Click to begin the simulation. The agent will start moving along the path found.
* Reset Button: Click to generate a new maze and reset the agent.
* Observe the Path Length: The UI panel displays the length of the path found.
* Compare Algorithms: Run the simulation with different algorithms to see how they perform.

---
## Future Extensions
The simulator is designed to be extensible and will include the following modules in future updates:

* Constraint Satisfaction Problems (CSP) Simulation
* Adversarial Search Simulation
* Reinforcement Learning Simulation

These modules will provide practical implementations and visualizations to help students understand advanced AI concepts.

## License
 GPL-3.0 license

## Contact

**Name**: Md Rifat Ahmmad Rashid  
**Position**: Associate Professor  
**Department**: Computer Science and Engineering (CSE)  
**Institution**: East West University, Bangladesh  
**E-mail**: rifat.rashid@ewubd.edu  

