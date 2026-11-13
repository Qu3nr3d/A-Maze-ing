import sys
from src.mazegen import MazeGenerator as mg


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

def check_configs(settings: dict[str, int | tuple[int, int] | str | bool])\
                    -> dict[str, int | tuple[int, int] | str | bool]:
        width: int = settings["WIDTH"]
        height: int = settings["HEIGHT"]
        entry: tuple[int, int] = settings["ENTRY"]
        exit: tuple[int, int] = settings["EXIT"]
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
        -> dict[str, int | tuple[int, int] | str | bool]:
    parsed_settings = {k: v for k, v in settings_dict.items()}
    try:
        parsed_settings["WIDTH"] = int(parsed_settings["WIDTH"])
        parsed_settings["HEIGHT"] = int(parsed_settings["HEIGHT"])
        parsed_settings["ENTRY"] = (
            int((parsed_settings["ENTRY"].split(",")[0])),
            int((parsed_settings["ENTRY"].split(","))[1])
            )
        parsed_settings["EXIT"] = (
            int((parsed_settings["EXIT"].split(","))[1]),
            int((parsed_settings["EXIT"].split(","))[0])
            )
        if parsed_settings["OUTPUT_FILE"] == "":
            raise TypeError
        if parsed_settings["PERFECT"].capitalize() != "True":
            parsed_settings["PERFECT"] = False
        else:
            parsed_settings["PERFECT"] = True
        try:
            if parsed_settings["SEED"] == '':
                parsed_settings["SEED"] = None
        except KeyError:
            parsed_settings["SEED"] = None
    except ValueError:
        print("Invalid filename")
        sys.exit(1)
    except KeyError as e:
        print(f"Invalid setting: {e}")
        sys.exit(1)
    try:
        check_configs(parsed_settings)
    except ValueError as e:
        sys.exit(1)
    return parsed_settings
