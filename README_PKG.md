*This project has been created as part of the 42 curriculum by jziental, kgirczyc*
# MazeGenerator Package

## Description

### Overview
The class is responsible for generating, solving, and exporting 2D grid-based mazes. It accepts a Configs dictionary (or uses defaults) defining dimensions, entry/exit coordinates, output file path, perfect/imperfect mode, and seed for reproducible pseudo-randomness.

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

### Key Methods & Workflow

#### __init\__(configs)

Stores settings and checks if dimensions exceed
5×7 to determine if the centered "42" pattern fits (_has_forty_two).

#### forty_two_symbol() -> set[tuple[int, int]]

Computes coordinate offsets relative to the grid center for the cells forming the "42" logo. These cells are marked pre-visited so no passages carve through them.

#### generate_maze() -> list[list[int]]

Base Spanning Tree (Prim's Algorithm): Starts from a random cell outside the "42" symbol and expands a frontier queue to carve walls until all accessible cells are visited.
Imperfect Mazes (_is_perfect=False): Iterates over all dead ends (cells with exactly 3 walls: values 7, 11, 13, 14).
 ##### Uses helper functions:
###### is_3x3_open: Checks whether internal walls of a
3 × 3 subgrid would all be absent.
###### scan_area: Evaluates all overlapping
3 × 3 candidate bounding boxes around the candidate wall opening.
##### open_wall:
Carves an extra opening if it respects grid boundaries, avoids the "42" symbol, and doesn't create a 3 × 3 open area.

#### solve_maze() -> list[tuple[int, int, str]]

Uses Breadth-First Search (**BFS**) with a queue and parent tracking dictionary to find the shortest path from _entry to _exit.
Returns steps as [(y, x, 'N'|'E'|'S'|'W'), ...].

#### send_maze_to_file() -> None

Formats the grid into hexadecimal rows (0 to f), followed by an empty line, entry x,y, exit x,y, and the path directions string.

#### Coordinate Conventions:
 Notice that inside the algorithms, tuples are handled as (y, x) (row, col), but send_maze_to_file() flips them to x,y (entry[1], entry[0]) to match standard Cartesian coordinates required by the subject.
