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

    def generate(self) -> list[list]:
        self.grid = [[16 for _ in range(self._width)]
                     for _ in range(self._height)]
