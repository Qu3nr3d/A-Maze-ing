import sys
from typing import TypedDict
from src.mazegen import mazegen as mg


class Configs(TypedDict):
    """Configuration settings for maze generation.

    defining grid dimensions, endpoints, and generation options."""
    WIDTH: int
    HEIGHT: int
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool
    SEED: str | None


def read_configs(filename: str) -> dict[str, str]:
    """read file of given name and returns it's content """
    settings_dict: dict[str, str] = {}
    try:
        with open(filename) as config:
            config_lines = [line.strip() for line in config if line[0] != "#"]
            for line in config_lines:
                if line.split("=")[0] not in ["WIDTH",
                                              "HEIGHT",
                                              "ENTRY",
                                              "EXIT",
                                              "OUTPUT_FILE",
                                              "PERFECT",
                                              "SEED"]:
                    raise ValueError(f"Invalid configuration: {line}")
            settings_dict = {(setting.split("=")[0]): (setting.split("=")[1])
                             for setting in config_lines
                             if len(setting.split("=")) == 2}
    except IndexError as e:
        print(f"{e}. No value assigned to setting")
        sys.exit(1)
    except (FileNotFoundError, ValueError) as e:
        print(f"{e}")
        sys.exit(1)
    return settings_dict


def check_configs(settings: Configs) -> None:
    """"""
    width = settings["WIDTH"]
    height = settings["HEIGHT"]
    entry = settings["ENTRY"]
    exit = settings["EXIT"]
    print(entry, exit)
    if width < 3 or height < 3:
        print("Invalid maze size")
        raise ValueError
    if not (0 <= entry[0] < height) or not (0 <= entry[1] < width):
        raise ValueError("Entry outside grid")
    if not (0 <= exit[0] < height) or not (0 <= exit[1] < width):
        raise ValueError("Exit outside grid")
    if entry == exit:
        raise ValueError("Entry and exit at the same position")
    forbidden = mg.MazeGenerator(settings).forty_two_symbol()
    if 5 < height < 500 and 7 < width < 500:
        if entry in forbidden:
            raise ValueError(f"Entry inside forty_two_symbol"
                             f"{entry[1],entry[0]}")
        elif exit in forbidden:
            raise ValueError("Exit inside forty_two_symbol")


def parse_configs(settings_dict: dict[str, str])\
        -> Configs:
    try:
        width = int(settings_dict["WIDTH"])
        height = int(settings_dict["HEIGHT"])
        entry = (
            int(settings_dict["ENTRY"].split(",")[1]),
            int(settings_dict["ENTRY"].split(",")[0])
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
    except ValueError as e:
        print(f"{e}")
        sys.exit(1)
    return parsed_settings
