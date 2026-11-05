import random as rnd


class MazeGenerator:
    """This class provides methods to generate maze based on given configs"""
    def __init__(self, configs: dict[str, int | tuple[int, int] | str | bool]):
        """Saves configurations as attributes"""
        self._width: int = configs["WIDTH"]
        self._height: int = configs["HEIGHT"]
        self._entry: tuple[int, int] = configs["ENTRY"]
        self._exit: tuple[int, int] = configs["EXIT"]
        self._output_file: str = configs["OUTPUT_FILE"]
        self._is_perfect: bool = configs["PERFECT"]
        self._seed = configs["SEED"]
        if self._height <= 5 or self._height <= 7:
            self._has_forty_two = False
        else:
            self._has_forty_two = True

    def generate_maze(self) -> list[list]:
        """method to generate maze by following Prims's algorithm"""
        self._grid = [[15 for _ in range(self._width)]
                      for _ in range(self._height)]
        N, E, S, W = 1, 2, 4, 8
        directions = {
            'N': (-1, 0, N, S),
            'S': (1, 0, S, N),
            'E': (0, 1, E, W),
            'W': (0, -1, W, E)
                    }

        def add_forty_two() -> list[tuple[int, int]]:
            """restricted '42' symbol area is saved to list of positions"""
            x, y = (self._width // 2, self._height // 2)
            return [
                (y - 2, x - 3), (y - 1, x - 3), (y, x - 3),
                (y, x - 2), (y, x - 1), (y + 1, x - 1), (y + 2, x - 1),
                (y - 2, x + 1), (y - 2, x + 2), (y - 2, x + 3), (y - 1, x + 3),
                (y, x + 3), (y, x + 2), (y, x + 1), (y + 1, x + 1),
                (y + 2, x + 1), (y + 2, x + 2), (y + 2, x + 3)
                    ]

        def valid_moves(y: int, x: int) -> list[tuple[tuple[int, int]], int] :
            """Return a list of possible moves"""
            moves = []
            for key, (dy, dx, dir_from, dir_to) in directions.items():
                ny, nx = y + dy, x + dx
                if 0 <= ny < self._height and 0 <= nx < self._width:
                    if (ny, nx) not in visited:
                        moves.append(((y, x), (ny, nx), dir_from, dir_to))
            return moves

        visited = set()
        if self._has_forty_two is True:
            visited = set(add_forty_two())
        curr_y, curr_x = (0, 0)
        rnd.seed(self._seed)
        while True:
            curr_y, curr_x = (rnd.randint(0, self._height - 1),
                              rnd.randint(0, self._width - 1))
            if (curr_y, curr_x) not in visited:
                break
        queue = valid_moves(curr_y, curr_x)
        visited.add((curr_y, curr_x))
        while queue:
            move = rnd.choice(queue)
            queue.remove(move)
            (curr_y, curr_x), (new_y, new_x), dir_from, dir_to = move
            if (new_y, new_x) not in visited:
                visited.add((new_y, new_y))
                self._grid[curr_y][curr_x] -= dir_from
                self._grid[new_y][new_x] -= dir_to
            new_moves = valid_moves(new_y, new_x)
            queue.extend(new_moves)
        return self._grid

    def solve_maze(self) -> list[str]:
        """method to return path from ENTRY to EXIT with BSF algorithm"""
