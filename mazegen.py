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
        if self._height <= 5 or self._height <=7:
            self._has_fort_two = False
        else:
            self._has_fort_two = True
            
    def generate_grid(self) -> list[list]:
        """method to genrate maze filled with only walls"""
        self.grid = [[15 for _ in range(self._width)]
                     for _ in range(self._height)]

    def generate_maze(self) -> list[list]:
        """method to generate maze by following Prims's algorithm"""


    def solve_maze(self) -> list[str]:
        """method to return path from ENTRY to EXIT with BSF algorithm"""
