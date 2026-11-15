import sys
import parser
from src.mazegen import mazegen as mg
import src.visual.visual as visual


def main() -> None:
    """Driver code for maze generation and visualization"""
    if len(sys.argv) == 2:
        try:
            unparsed = parser.read_configs(sys.argv[1])
        except FileNotFoundError as e:
            print(f"{e}")
        configs = parser.parse_configs(unparsed)
        labirynth = mg.MazeGenerator(configs)
        labirynth.generate_maze()
        labirynth.solve_maze()
        labirynth.send_maze_to_file()


if __name__ == "__main__":
    main()
