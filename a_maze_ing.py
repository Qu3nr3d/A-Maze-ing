import parser
import mazegen


def main() -> None:
    """Driver code for maze generation and visualization"""
    unparsed = parser.read_configs()
    configs = parser.parse_configs(unparsed)
    print(configs)
    labirynth = mazegen.MazeGenerator(configs)
    maze = labirynth.generate_perfect_maze()
    for line in maze:
        print("".join(format(char, "x") for char in line))
    labirynth.send_maze_to_file()

if __name__ == "__main__":
    main()
