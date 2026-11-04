import random


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

    def generate_grid(self) -> list[list]:
        """method to genrate maze filled with only walls"""
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

        visited = []
        if self._has_forty_two is True:
            visited = add_forty_two()
        random.seed(self._seed)
        print(random.randint(0, 17))
        return self._grid


    def generate_maze(self) -> list[list]:
        """method to generate maze by following Prims's algorithm"""

    def solve_maze(self) -> list[str]:
        """method to return path from ENTRY to EXIT with BSF algorithm"""
