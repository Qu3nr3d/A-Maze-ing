import sys


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


def parse_configs(settings_dict: dict[str, str])\
        -> dict[str, int | tuple[int, int] | str | bool]:
    parsed_settings = {k: v for k, v in settings_dict.items()}
    try:
        parsed_settings["WIDTH"] = int(parsed_settings["WIDTH"])
        parsed_settings["HEIGHT"] = int(parsed_settings["HEIGHT"])
        parsed_settings["ENTRY"] = (int((parsed_settings[
            "ENTRY"].split(",")[0])),
            int((parsed_settings["ENTRY"].split(","))[1]))
        parsed_settings["EXIT"] = (
            int((parsed_settings["EXIT"].split(","))[0]),
            int((parsed_settings["EXIT"].split(","))[1]))
        if parsed_settings["OUTPUT_FILE"] == "":
            raise ValueError
        if parsed_settings["PERFECT"].capitalize() != "True":
            parsed_settings["PERFECT"] = False
        else:
            parsed_settings["PERFECT"] = True
    except ValueError:
        print("Invalid filename")
        sys.exit(1)
    except KeyError as e:
        print(f"Invalid setting: {e}")
        sys.exit(1)
    return parsed_settings
