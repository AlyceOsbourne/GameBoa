import configparser
import pathlib

# default values
DEFAULTS = {
    # developer_options
    "developer_options": {
        "debug_mode": "False"
    },
}


class Config:
    """A class to handle the configuration file."""

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            setattr(cls, "instance", super().__new__(cls))
        return getattr(cls, "instance")

    def __init__(self, config_file: pathlib.Path):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)
        self._set_defaults()

    def _set_defaults(self) -> None:
        """Sets default values for the configuration file."""
        for section, options in DEFAULTS.items():
            if not self.config.has_section(section):
                self.config.add_section(section)
            for option, value in options.items():
                if not self.config.has_option(section, option):
                    self.config.set(section, option, value)

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

    def get_as_type(self, section, option):
        """Gets the type of a value in the configuration file."""
        value = self.get(section, option)
        match value:
            case "True":
                return True
            case "False":
                return False
            case value.isdigit():
                if "." in value:
                    return float(value)
                return int(value)
            case _:
                return value


if __name__ == "__main__":
    config = Config(pathlib.Path("config.ini"))
    config.save()
