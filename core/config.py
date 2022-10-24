from pathlib import Path
from re import compile, IGNORECASE
from configparser import ConfigParser

DEFAULTS = {
    "developer_options": {"debug mode": "False", "enable indev features": "False"},
}

data_type_patterns = {
    int: compile(r"^-?\d+$"),
    float: compile(r"^-?\d+\.\d+$"),
    bool: compile(r"^(true|false)$", IGNORECASE),
}


class ConfigManager:
    """Manages the configuration file."""

    def __init__(self):
        self.config_manager = ConfigParser()
        self.config_file = Path("config.ini")
        self.config_manager.read(self.config_file)

        self._set_defaults()
        self.save()

    def _set_defaults(self) -> None:
        """Sets default values for the configuration file."""
        for (section, option) in DEFAULTS.items():
            if section not in self.config_manager.sections():
                self.config_manager.add_section(section)

            for (option, value) in option.items():
                if option not in self.config_manager.options(section):
                    self.config_manager.set(section, option, value)

        for section in self.config_manager.sections():
            if section not in DEFAULTS:
                self.config_manager.remove_section(section)
            else:
                for option in self.config_manager.options(section):
                    if option not in DEFAULTS[section]:
                        self.config_manager.remove_option(section, option)

    def save(self) -> None:
        """Saves the configuration file."""
        with open(self.config_file, "w") as file:
            self.config_manager.write(file)

    def get(self, section: str, option: str) -> str:
        """Gets a value from the configuration file."""
        return self.config_manager.get(section, option)

    def set(self, section: str, option: str, value: str) -> None:
        """Sets a value in the configuration file."""
        self.config_manager.set(section, option, value)

    def sections(self) -> list:
        """Gets all sections in the configuration file."""
        return self.config_manager.sections()

    def options(self, section: str) -> list:
        """Gets all options in a section in the configuration file."""
        return self.config_manager.options(section)

    def get_value_as_type(self, section: str, option: str) -> str | int | float | bool:
        """Gets a value from the configuration file and autocasts it."""
        value = self.get(section, option)

        for (data_type, pattern) in data_type_patterns.items():
            if pattern.match(value):
                return data_type(value)

        return value

    def get_boolean(self, section: str, option: str) -> bool:
        """Gets a boolean value from the configuration file."""
        return self.config_manager.getboolean(section, option)
