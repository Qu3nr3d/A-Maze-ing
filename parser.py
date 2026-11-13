import sys
from typing import TypedDict
from src.mazegen import MazeGenerator as mg  # type: ignore[import]


class Configs(TypedDict):
    WIDTH: int
    HEIGHT: int
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool
    SEED: str | None


def read_configs() -> dict[str, str]:
    """read config.txt file, exits in case of fail"""
    settings_dict: dict[str, str] = {}
    try:
        with open("config.txt") as config:
            config_lines = [line.strip() for line in config if line[0] != "#"]
            settings_dict = {(setting.split("=")[0]): (setting.split("=")[1])
                             for setting in config_lines}
    except IndexError as e:
        print(f"{e} No value assigned to setting")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"{e}")
        sys.exit(1)
    return settings_dict


def check_configs(
        settings: Configs) -> None:
    width = settings["WIDTH"]
    height = settings["HEIGHT"]
    entry = settings["ENTRY"]
    exit = settings["EXIT"]
    if not (0 <= entry[0] < height) or not (0 <= entry[1] <= width):
        print("Entry outside grid")
        raise ValueError
    if not (0 <= exit[0] < height) or not (0 <= exit[1] <= width):
        print("Exit outside grid")
        raise ValueError
    forbidden = mg().forty_two_symbol()
    if height > 7 and width > 5:
        if entry in forbidden:
            print("Entry inside forty_two_symbol")
            raise ValueError
        if exit in forbidden:
            print("Exit inside forty_two_symbol")
            raise ValueError


def parse_configs(settings_dict: dict[str, str])\
        -> Configs:
    try:
        width = int(settings_dict["WIDTH"])
        height = int(settings_dict["HEIGHT"])
        entry = (
            int(settings_dict["ENTRY"].split(",")[0]),
            int(settings_dict["ENTRY"].split(",")[1])
        )
        exit = (
            int(settings_dict["EXIT"].split(",")[1]),
            int(settings_dict["EXIT"].split(",")[0])
        )
        output_file = settings_dict["OUTPUT_FILE"]
        perfect = settings_dict["PERFECT"].capitalize() == "True"
        seed = settings_dict.get("SEED") or None
    except ValueError:
        print("Invalid filename")
        sys.exit(1)
    except KeyError as e:
        print(f"Invalid setting: {e}")
        sys.exit(1)

    if output_file == "":
        raise TypeError("OUTPUT_FILE cannot be empty")

    parsed_settings: Configs = {
        "WIDTH": width,
        "HEIGHT": height,
        "ENTRY": entry,
        "EXIT": exit,
        "OUTPUT_FILE": output_file,
        "PERFECT": perfect,
        "SEED": seed,
    }
    try:
        check_configs(parsed_settings)
    except ValueError:
        sys.exit(1)
    return parsed_settings
