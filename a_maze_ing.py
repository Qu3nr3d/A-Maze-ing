import parser
from src.mazegen import mazegen as mg


def main() -> None:
    """Driver code for maze generation and visualization"""
    unparsed = parser.read_configs()
    configs = parser.parse_configs(unparsed)
    labirynth = mg.MazeGenerator(configs)
    labirynth.generate_maze()
    labirynth.solve_maze()
    labirynth.send_maze_to_file()


if __name__ == "__main__":
    main()
