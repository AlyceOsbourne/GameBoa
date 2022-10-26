import configparser
import pathlib

from src.system import EventHandler, SystemEvents

config_parser = configparser.ConfigParser()

root_path = pathlib.Path(__file__).parent.parent.parent.absolute()

local_path = root_path / 'local'
local_path.mkdir(exist_ok=True)

config_folder_path = local_path / "config"
config_folder_path.mkdir(exist_ok=True)
config_path = config_folder_path / "gameboa.config"

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
    'developer': {}
}

@EventHandler.subscriber(SystemEvents.LoadSettings)
def load_config():
    config_parser.read_dict({
        section: {
            key: value[0]
            for key, value in defaults[section].items()
        }
        for section in defaults
    })
    config_parser.read(config_path)
    for path in config_parser['paths'].values():
        path = pathlib.Path(path)
        path.mkdir(exist_ok=True)
    config_parser.write(open(config_path, 'w'))

def get_value(section, key):
    if section not in config_parser:
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

@EventHandler.subscriber(SystemEvents.SaveSettings)
def save_config():
    config_parser.write(open(config_path, 'w'))

load_config()


