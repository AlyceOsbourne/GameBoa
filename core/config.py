import configparser
import pathlib
import re

DEFAULTS = {
    # developer_options
    "developer_options": {
        "debug mode": "False",
        "enable indev features": "False"
    },
}

dtype_patterns = {
    bool: re.compile(r"^(true|false)$", re.IGNORECASE),
    int: re.compile(r"^-?\d+$"),
    float: re.compile(r"^-?\d+\.\d+$")
}


class _Config:
    """A class to handle the configuration file."""

    def __init__(self):
        self.config_parser = configparser.ConfigParser()
        self.config_file = pathlib.Path("../config.ini")
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)
        # check structure matches defaults
        self._set_defaults()

    def _set_defaults(self) -> None:
        """Sets default values for the configuration file."""
        for section, options in DEFAULTS.items():
            if section not in self.config.sections():
                self.config.add_section(section)
            for option, value in options.items():
                if option not in self.config.options(section):
                    self.config.set(section, option, value)
        for section in self.config.sections():
            if section not in DEFAULTS:
                self.config.remove_section(section)
            else:
                for option in self.config.options(section):
                    if option not in DEFAULTS[section]:
                        self.config.remove_option(section, option)





    def save(self) -> None:
        """Saves the configuration file."""
        with open(self.config_file, "w") as file:
            self.config.write(file)

    def get(self, section: str, option: str) -> str:
        """Gets a value from the configuration file."""
        return self.config.get(section, option)

    def set(self, section: str, option: str, value: str) -> None:
        """Sets a value in the configuration file."""
        self.config.set(section, option, value)

    def sections(self) -> list:
        """Gets all sections in the configuration file."""
        return self.config.sections()

    def options(self, section: str) -> list:
        """Gets all options in a section in the configuration file."""
        return self.config.options(section)

    def get_value_as_dtype(self, section: str, option: str):
        """Gets a value from the configuration file and auto casts it."""
        value = self.get(section, option)
        for dtype, pattern in dtype_patterns.items():
            if pattern.match(value):
                return dtype(value)
        return value

    def get_boolean(self, section: str, option: str) -> bool:
        """Gets a boolean value from the configuration file."""
        return self.config.getboolean(section, option)




# regex patterns to match values to their types



config = _Config()
config.save()
