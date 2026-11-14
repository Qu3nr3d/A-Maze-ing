*This project has been created as part of the 42 curriculum by jziental, kgirczyc*

# A-Maze-ing

## Description

### Project Goal
The goal of this project is to create a Python maze generator that reads its
parameters from a configuration file, generates a valid maze, saves it using
the required hexadecimal wall format, and displays it visually. The program
must support reproducible generation through a seed, define an entry and an
exit, and provide a solution path between them.

### Project Overview
The application is launched with a configuration file and produces a maze
whose cells are represented by four possible walls: north, east, south, and
west. It supports both perfect mazes, which have a single path between cells,
and non-perfect mazes with loops suitable for a Pac-Man-like board. The
generated maze is written to the configured output file, including the entry,
exit, and shortest path, and is also rendered graphically with MLX. The maze
generator is implemented as a reusable `MazeGenerator` class in the
standalone `mazegen` package.

## Instructions

### Installation
Requires uv to be installed.
```zsh
make install
```
This runs uv sync, which creates a virtual environment and installs all required dependencies.
### Execution
```zsh
make run
```
Runs the program with the default config.txt. Equivalent to:
```zsh
python3 a_maze_ing.py
```

## Configuration File

### Complete Structure
```text
config.txt
# Every setting has to be in one line with it's value
# Maze width (number of cells):
WIDTH=3
# Maze height
HEIGHT=3
# Entry coordinates (x,y):
ENTRY=0,0
# Exit coordinates (x,y)
EXIT=2,2
# Output filename
OUTPUT_FILE=maze.txt
# Is the maze perfect?
PERFECT=False
# If SEED setting is invalid/empty seed is set to None
# meaning randomness is based on system time
SEED=
```
### Format
configuration file can contain any number of lines starting with '#' and will be ommited. Other lines have to be valid.

## Maze Generation Algorithm

### Chosen Algorithm
We've decided to use Prim's algorithm which finds the minimum spanning tree on given graph
### Rationale
Minimum spanning tree is a subgraph of a given graph with a minimum number of edges needed to connect all nodes. Because of that it guarantes that maze will be perfect - not a single node shall be conected twice with any of it's neighbours and thus won't create any loop.
## Code Reusability

### Reusable Code
In this project we implemented the maze generation as a unique class (‘MazeGenerator‘) inside
a standalone module that can be imported in a future project.

### How to Reuse It
#### Instantiate
`MazeGenerator` accepts one configuration dictionary. All keys are required when
passing a custom configuration:
```Python
import mazegen

maze = mazegen.MazeGenerator()
```

The supported configuration keys are:
- `WIDTH` and `HEIGHT`: maze dimensions as integers.
- `ENTRY` and `EXIT`: entry and exit coordinates as `(row, column)` tuples.
- `OUTPUT_FILE`: name of the file to which the maze is written.
- `PERFECT`: boolean indicating whether to generate a perfect maze.
- `SEED`: string used to seed generation, or `None` for a time-based seed.

For example:
```python
maze = mazegen.MazeGenerator({
    "WIDTH": 15,
    "HEIGHT": 20,
    "ENTRY": (0, 0),
    "EXIT": (14, 19),
    "OUTPUT_FILE": "labyrinth.txt",
    "PERFECT": True,
    "SEED": "42",
})
```

#### Generate and solve
Call `generate_maze()` first. It returns the maze grid as a list of lists of
integers, where each integer encodes the walls of one cell. Then call
`solve_maze()` to calculate the shortest route from `ENTRY` to `EXIT`. The
solution is returned as a list of `(row, column, direction)` tuples.

```Python
grid = maze.generate_maze()
path = maze.solve_maze()
```

#### Save the maze
After generating and solving the maze, call `send_maze_to_file()` to save the
grid, entry and exit coordinates, and solution path to `OUTPUT_FILE`.

```Python
maze.send_maze_to_file()
```

## Team and Project Management

### Team Roles
| team member | responsibilities |
|--|--|
| jziental | backend (algorithms) + Makefile + README|
| kgirczyc | frontend (visualization with MLX) + uv tool (pyproject.toml with command)|

### Initial Planning
At the beginning of the project, we divided the work according to our strengths. One person focused on the maze-generation algorithm, configuration handling, the Makefile and documentation, while the other focused on the graphical interface and project setup.

### Planning Evolution
The original plan remained mostly unchanged because the initial division of responsibilities and technical choices worked well. During development, we made only small adjustments while integrating the generator with the visualizer, improving configuration validation, and testing the complete application.

### What Worked Well
The clear division of responsibilities helped us work in parallel and make steady progress. Keeping the maze generator modular made it easier to test and reuse, while regular integration allowed us to connect it with the visualizer without major problems.

### What Could Be Improved
Although the project progressed smoothly, we could have planned integration testing earlier and documented the public API in more detail from the start. We could also have added more automated tests for invalid configuration values and edge cases, which would make future changes safer and reduce the need for manual checks.

### Tools Used
We used Python for the implementation, MLX for visualization, and `uv` for project and dependency management. The Makefile provided convenient commands for installation, execution, debugging, cleaning and linting. We used Git for version control and AI tools as an additional aid for understanding concepts, checking implementation ideas and finding bugs.

## Advanced Features

### Display Options
**Key bindings**\
ESC: exit program
R: regenerate maze\
C: change color of the walls
S: switch on/off path showing

## Resources

### References
[Subject](https://cdn.intra.42.fr/pdf/pdf/224851/en.subject.pdf)\
[Prims's algorithm](https://en.wikipedia.org/wiki/Prim%27s_algorithm)\
[A-maze-ing website with visualization](https://amazeing.app/learn?algorithm=Prims)
### AI Usage
AI was used to understand Prim's algorithm , to debug the imperfect maze generation logic, and to learn MLX library usage for graphical rendering.
