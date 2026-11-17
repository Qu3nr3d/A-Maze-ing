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
        grid = labirynth.generate_maze()
        labirynth.solve_maze()
        labirynth.send_maze_to_file()
        app = visual.MazeRenderer(
            grid=grid,
            entry=labirynth.entry,
            exit=labirynth.exit,
            solution=labirynth.solution_str,
            regenerate=labirynth.regenerate
        )
        app.run()
    else:
        print("Usage: uv run python3 a_maze_ing.py config.txt")

if __name__ == "__main__":
    main()
