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

## Usage

### Running the Simulation
Navigate to the examples directory and run main.py:

```
cd examples
python main.py
```
This will launch the robot task simulation with default settings.

### Command-Line Arguments
==========================

You can customize the simulation by providing command-line arguments:

* `--algorithm`: Specify the search algorithm to use.
	+ Options: `dfs`, `bfs`, `ucs`, `astar`, `hill_climbing`, `simulated_annealing`
	+ Default: `astar`
* `--grid_size`: Set the size of the grid.
	+ Default: `16`
* `--task_positions`: Provide a list of task positions.
	+ Format: `"[(x1,y1),(x2,y2),..."]"`
	+ Default: Randomly generated positions

#### Example Usage:

```
python main.py --algorithm bfs --grid_size 20 --task_positions "[(2,3),(5,5),(10,10)]"
```
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
│   │   └── robot_agent.py
│   ├── environments/
│   │   ├── __init__.py
│   │   └── grid_environment.py
│   ├── search_algorithms/
│   │   ├── __init__.py
│   │   ├── uninformed_search.py
│   │   ├── informed_search.py
│   │   └── local_search.py
│   ├── csp_algorithms/
│   │   ├── __init__.py
│   │   └── csp_solver.py
│   ├── adversarial_search/
│   │   ├── __init__.py
│   │   └── minimax.py
│   ├── reinforcement_learning/
│   │   ├── __init__.py
│   │   └── q_learning.py
│   ├── simulations/
│   │   ├── __init__.py
│   │   ├── simulation_base.py
│   │   ├── search_simulation.py
│   │   ├── csp_simulation.py
│   │   ├── adversarial_simulation.py
│   │   └── rl_simulation.py
│   └── utils/
│       ├── __init__.py
│       └── constants.py
└── examples/
    ├── __init__.py
    └── main.py
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
### Running with Default Settings
```
python main.py
```

### Using BFS Algorithm
```
python main.py --algorithm bfs
```
### Setting a Custom Grid Size
```
python main.py --grid_size 20
```
### Specifying Task Positions
```
python main.py --task_positions "[(3,3),(5,5),(7,7)]"
```
### Combining Arguments
```
python main.py --algorithm ucs --grid_size 25 --task_positions "[(2,2),(4,4),(6,6)]"
```

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

