import parser


def main() -> None:
    """Driver code for maze generation and visualization"""
    unparsed = parser.read_configs()
    configs = parser.parse_configs(unparsed)
    print(configs)


if __name__ == "__main__":
    main()
