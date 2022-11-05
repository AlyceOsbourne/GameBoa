import configparser
import pathlib
import sys

if hasattr(sys, "_MEIPASS"):
    user_path = pathlib.Path.home() / "GameBoa"
    user_path.mkdir(exist_ok=True)
else:
    user_path = pathlib.Path(pathlib.Path.cwd()) / "local"
    user_path.mkdir(exist_ok=True)


defaults = {
    "paths": {
        "roms": (user_path / "roms", str),
        "saves": (user_path / "saves", str),
        "save states": (user_path / "save_states", str),
        "game configs": (user_path / "game_configs", str),
        "patch files": (user_path / "patches", str),
        "logs": (user_path / "logs", str),
    },
    "video": {},
    "sound": {},
    "input": {},
    "developer": {
        "debug": (False, bool),
        "debug logging": (False, bool),
    },
}

_config_parser = configparser.ConfigParser()


def load_config():
    defaults_ = {section: {key: value[0] for key, value in options.items()} for section, options in defaults.items()}
    _config_parser.read_dict(defaults_)
    _config_parser.read(user_path / "gameboa.config")
    for section in _config_parser.sections():
        if section not in defaults:
            _config_parser.remove_section(section)
        else:
            for key in _config_parser[section]:
                if key not in defaults_[section]:
                    _config_parser[section].pop(key)
    save_config()
    for path in _config_parser["paths"].values():
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def get_value(section, key):
    if section not in _config_parser.sections():
        raise KeyError(f"No section {section} in config")
    if key not in _config_parser[section]:
        raise KeyError(f"No key {key} in section {section}")
    opt_type = option_type(section, key)
    if opt_type == str:
        return _config_parser[section][key]
    elif opt_type == int:
        return _config_parser[section].getint(key)
    elif opt_type == float:
        return _config_parser[section].getfloat(key)
    elif opt_type == bool:
        return _config_parser[section].getboolean(key)
    raise TypeError(f"Unknown option type {opt_type}")


def set_value(section, key, value):
    if section not in _config_parser:
        raise KeyError(f"No section {section} in config")
    if key not in _config_parser[section]:
        raise KeyError(f"No key {key} in section {section}")
    if type(value) != defaults[section][key][1]:
        raise TypeError(f"Value {value} is not of type {defaults[section][key][1]}")
    _config_parser[section][key] = str(value)


def sections():
    return _config_parser.sections()


def section_options(section):
    return _config_parser[section].keys()


def option_type(section, key):
    return defaults[section][key][1]


def save_config():
    _config_parser.write(open(user_path / "gameboa.config", "w"))


def reset_to_defaults():
    for section, options in defaults.items():
        for key, value in options.items():
            _config_parser[section][key] = str(value[0])


__all__ = [
    "load_config",
    "get_value",
    "set_value",
    "save_config",
    "sections",
    "section_options",
    "option_type",
]
