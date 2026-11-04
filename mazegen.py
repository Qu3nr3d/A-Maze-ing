import random as rnd
from collections import deque


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
        def possible_move(position: tuple[int, int]) -> list[tuple[int, int]] :
            """Return a list of possible moves"""
            moves = []
            if position[0] != 0:
                moves.append((-1, 0))
            if position[0] != self._height:
                moves.append((1, 0))
            if position[1] != 0:
                moves.append((-1, 0))
            if position[1] != self._width:
                moves.append((1, 0))
            return moves

        visited = []
        if self._has_forty_two is True:
            visited = add_forty_two()
        curr_y, curr_x = (0, 0)
        rnd.seed(self._seed)
        while True:
            curr_y, curr_x = (rnd.randint(0, self._height),
                              rnd.randint(0, self._width))
            if (curr_y, curr_x) not in visited:
                break
        queue = deque()
        queue.append((curr_y, curr_x))
        while queue:
            for move in possible_move((curr_y, curr_x)):
                new_pos = (curr_y + move[0], curr_x + move[1])
                if new_pos not in visited:
                    queue.append(new_pos)
                    print(queue)
            new_pos = rnd.choice(queue)
            curr_x, curr_y = new_pos
            queue.remove(new_pos)
        return [1,2]#self._grid

    def solve_maze(self) -> list[str]:
        """method to return path from ENTRY to EXIT with BSF algorithm"""
