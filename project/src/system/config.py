import configparser
import pathlib
from __paths__ import local_path, config_folder_path, config_path

config_parser = configparser.ConfigParser()

defaults = {
    "paths" : {
        'roms' : (local_path / "roms", str),
        'saves' : (local_path / "saves", str),
        'save states': (local_path / "save_states", str),
        'game configs': (config_folder_path / "game_configs", str),
        'patch files': (local_path / "patches", str),
    },
    "video" : {},
    "sound": {},
    'input': {},
    'developer': {
        'debug': (False, bool),
    }
}


def load_config():
    defaults_ = {
    section: {
        key: value[0]
        for key, value in options.items()

    }
    for section, options in defaults.items()
}
    config_parser.read_dict(defaults_)
    config_parser.read(config_path)
    save_config()

    for path in config_parser['paths'].values():
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)

def get_value(section, key):
    if section not in config_parser.sections():
        raise KeyError(f'No section {section} in config')
    if key not in config_parser[section]:
        raise KeyError(f'No key {key} in section {section}')
    opt_type = option_type(section, key)
    if opt_type == str:
        return config_parser[section][key]
    elif opt_type == int:
        return config_parser[section].getint(key)
    elif opt_type == float:
        return config_parser[section].getfloat(key)
    elif opt_type == bool:
        return config_parser[section].getboolean(key)
    else:
        raise TypeError(f'Unknown option type {opt_type}')

def set_value(section, key, value):
    if section not in config_parser:
        raise KeyError(f'No section {section} in config')
    if key not in config_parser[section]:
        raise KeyError(f'No key {key} in section {section}')
    if type(value) != defaults[section][key][1]:
        raise TypeError(f'Value {value} is not of type {defaults[section][key][1]}')
    config_parser[section][key] = str(value)

def sections():
    return config_parser.sections()

def section_options(section):
    return config_parser[section].keys()

def option_type(section, key):
    return defaults[section][key][1]

def save_config():
    config_parser.write(open(config_path, 'w'))

load_config()

