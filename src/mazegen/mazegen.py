import random as rnd
from collections import deque


class MazeGenerator:
    """This class provides methods to generate maze based on given configs"""
    def __init__(self, configs: dict[str, int | tuple[int, int] | str | bool] =
                 {"WIDTH": 10, "HEIGHT": 10, "ENTRY": (0,0), "EXIT": (9,9),
                  "OUTPUT_FILE": "maze.txt", "PERFECT": True,
                   "SEED": "42"}) -> None:
        """Saves configurations as attributes"""
        self._width: int = configs["WIDTH"]
        self._height: int = configs["HEIGHT"]
        self._entry: tuple[int, int] = configs["ENTRY"]
        self._exit: tuple[int, int] = configs["EXIT"]
        self._output_file: str = configs["OUTPUT_FILE"]
        self._is_perfect: bool = configs["PERFECT"]
        self._seed = configs["SEED"]
        print(self._entry, self._exit)
        if self._height <= 5 or self._width <= 7:
            self._has_forty_two = False
        else:
            self._has_forty_two = True

    def forty_two_symbol(self) -> list[tuple[int, int]]:
        """Returns restricted '42' symbol area as a list of positions"""
        x, y = self._width // 2, self._height // 2
        points = set([
            (y - 2, x - 3), (y - 1, x - 3), (y, x - 3),
            (y, x - 2), (y, x - 1), (y + 1, x - 1), (y + 2, x - 1),
            (y - 2, x + 1), (y - 2, x + 2), (y - 2, x + 3), (y - 1, x + 3),
            (y, x + 3), (y, x + 2), (y, x + 1), (y + 1, x + 1),
            (y + 2, x + 1), (y + 2, x + 2), (y + 2, x + 3)
                    ])
        return points

    def generate_maze(self) -> list[list]:
        """method to generate maze by following Prims's algorithm"""
        self._grid = [[15 for _ in range(self._width)]
                      for _ in range(self._height)]
        N, E, S, W = 1, 2, 4, 8
        directions = {
            'N': (-1, 0, N, S),
            'E': (0, 1, E, W),
            'S': (1, 0, S, N),
            'W': (0, -1, W, E)
                    }


        def valid_dirs(y: int, x: int) -> list[tuple[tuple[int, int]], int] :
            """Return a list of possible wall openings"""
            moves = []
            for key, (dy, dx, dir_from, dir_to) in directions.items():
                ny, nx = y + dy, x + dx
                if 0 <= ny < self._height and 0 <= nx < self._width:
                    if (ny, nx) not in visited:
                        moves.append(((y, x), (ny, nx), dir_from, dir_to))
            return moves

        visited = set()
        if self._has_forty_two is True:
            visited.update(self.forty_two_symbol())
        curr_y, curr_x = (0, 0)
        rnd.seed(self._seed)
        while True:
            curr_y, curr_x = (rnd.randint(0, self._height - 1),
                              rnd.randint(0, self._width - 1))
            if (curr_y, curr_x) not in visited:
                break
        queue = valid_dirs(curr_y, curr_x)
        visited.add((curr_y, curr_x))
        while queue:
            move = rnd.choice(queue)
            queue.remove(move)
            (curr_y, curr_x), (new_y, new_x), dir_from, dir_to = move
            if (new_y, new_x) not in visited:
                visited.add((new_y, new_x))
                self._grid[curr_y][curr_x] -= dir_from
                self._grid[new_y][new_x] -= dir_to
                new_moves = valid_dirs(new_y, new_x)
                queue.extend(new_moves)
        if self._is_perfect:
            return self._grid
        else:
            def is_3x3_open(r, c, opened_y, opened_x, opened_dir):
                """Is 3x3 block open after this wall opening?"""
                for row in range(r, r + 3):
                    for col in range(c, c + 2):
                        already_open = (opened_dir == 'E'
                                        and row == opened_y and col == opened_x)
                        if not already_open and self._grid[row][col] & E:
                            return False
                for row in range(r, r + 2):
                    for col in range(c, c + 3):
                        already_open = (opened_dir == 'S'
                                        and row == opened_y and col == opened_x)
                        if not already_open and self._grid[row][col] & S:
                            return False
                return True

            def scan_area(dead_end: tuple[int, int], open_dir: str) -> bool:
                """Check if area after opening wall will be smaller than 3x3"""
                y, x = dead_end
                dy, dx = directions[open_dir][:2]
                ny, nx = y + dy, x + dx
                r_min = max(0, max(y, ny) - 2)
                r_max = min(self._height - 3, min(y, ny))
                c_min = max(0, max(x, nx) - 2)
                c_max = min(self._width - 3,  min(x, nx))
                for r in range(r_min, r_max + 1):
                    for c in range(c_min, c_max + 1):
                        if is_3x3_open(r, c, y, x, open_dir):
                            return False   # this direction would create a 3x3
                return True

            def open_wall(dead_end: tuple[int, int]) -> list[list]:
                """Returns an updated grid with opened dead end on given pos"""
                y, x = dead_end
                for direction, (dy, dx,
                                dir_from, dir_to) in directions.items():
                    ny, nx = y + dy, x + dx
                    if not (0 <= ny < self._height and 0 <= nx < self._width):
                        continue
                    if (y, x) not in restricted or (ny, nx) not in restricted:
                        continue
                    if not self._grid[y][x] & dir_from:
                        continue
                    if scan_area((y, x), direction):
                        self._grid[y][x] -= dir_from
                        self._grid[ny][nx] -= dir_to
                        return

            restricted = self.forty_two_symbol()
            for y, row in enumerate(self._grid):
                for x, wall in enumerate(row):
                    if wall in [N + E + S, E + S + W, N + E + W, N + S + W]:
                        open_wall((y, x))
            return self._grid
            #find dead end
            #check if not in 42 symbol
            #scan if area won't be open 3x3

    def solve_maze(self) -> list[tuple[int, int, str]]:
        """Return the shortest path from ENTRY to EXIT using BFS."""
        directions = [
            (-1, 0, 'N', 1),
            (0, 1, 'E', 2),
            (1, 0, 'S', 4),
            (0, -1, 'W', 8)
                    ]

        def valid_moves(y: int, x: int) -> list[tuple[int, int],
                                                tuple[int, int], str] :
            """Return a list of possible moves"""
            moves = []
            for (dy, dx, dir_to, wall_idx) in directions:
                ny, nx = y + dy, x + dx
                if 0 <= ny < self._height and 0 <= nx < self._width:
                    if (ny, nx) not in visited and\
                        not (self._grid[y][x] & wall_idx):
                            moves.append(((y, x), (ny, nx), dir_to))
            return moves

        visited = set()
        curr_y, curr_x = self._entry
        visited.add((curr_y, curr_x))
        queue = deque()
        for new_move in valid_moves(curr_y, curr_x):
            queue.append(new_move)
            visited.add(new_move[1])
        self._path = {}
        goal = self._exit
        while queue:
            move = queue.popleft()
            (curr_y, curr_x), (new_y, new_x), dir_to = move
            self._path.update({(new_y, new_x):(curr_y, curr_x, dir_to)})
            visited.add((new_y, new_x))
            if (new_y, new_x) == goal:
                self._path.update({(new_y, new_x):(curr_y, curr_x, dir_to)})
                shortest_route = []
                while (new_y, new_x) != self._entry:
                    parent_y, parent_x, dir_to = self._path[(new_y, new_x)]
                    shortest_route.append((new_y, new_x, dir_to))
                    new_y, new_x = parent_y, parent_x
                self._path.clear()
                shortest_route.reverse()
                self._path = shortest_route
                break
            for new_move in valid_moves(new_y, new_x):
                queue.append(new_move)
                visited.add(new_move[1])
        return self._path

    def send_maze_to_file(self) -> None:
        with open(f"{self._output_file}", "w") as file:
            formated_grid = [[f"{num:x}" for num in line]
                              for line in self._grid]
            for line in formated_grid:
                for char in line:
                    file.write(char)
                file.write("\n")
            file.write(f"\n{self._entry[1]},{self._entry[0]}\n"
                       f"{self._exit[1]},{self._exit[0]}\n")
            try:
                for move in self._path:
                    file.write(move[2])
                file.write("\n")
            except AttributeError as e:
                print(f"{e} (solve_maze() not called)")
            except IndexError as e:
                print(f"{e} (entry = exit)")
