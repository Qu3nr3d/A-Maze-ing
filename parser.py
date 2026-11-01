import sys


def read_configs() -> dict[str, str]:
    """read config.txt file, exits in case of fail"""
    settings_dict: dict[str, str] = {}
    try:
        with open("config.txt") as config:
            all_lines = [config.readline().strip() for line in config]
            config_lines = [line for line in all_lines if line[0] != "#"]
            settings_dict = {setting.split("=")[0]: setting.split("=")[1]
                             for setting in config_lines}
    except IndexError as e:
        print(f"{e} No value assigned to setting")
    except FileNotFoundError as e:
        print(f"{e}")
    return settings_dict


def parse_configs(settings_dict: dict[str, str])\
        -> dict[str, int | tuple[int, int] | str | bool]:
    parsed_settings = {k: v for k, v in settings_dict.items()}
    try:
        parsed_settings["WIDTH"] = int(parsed_settings["WIDTH"])
        parsed_settings["HEIGHT"] = int(parsed_settings["HEIGHT"])
        parsed_settings["ENTRY"] = (int((parsed_settings["ENTRY"].split(",")[0])),
                                  int((parsed_settings["ENTRY"].split(","))[1]))
        parsed_settings["EXIT"] = (int((parsed_settings["EXIT"].split(","))[0]),
                                  int((parsed_settings["EXIT"].split(","))[1]))
        if parsed_settings["OUTPUT_FILE"] == "":
            raise ValueError
        parsed_settings["PERFECT"] = bool(parsed_settings["PERFECT"])
    except ValueError:
        print("Invalid filename")
        sys.exit(1)
    return parsed_settings
