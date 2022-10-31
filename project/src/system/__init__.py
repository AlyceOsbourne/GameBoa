from .config import *
from .system_paths import *
from .gb_logger import *
from . import data_distributor

data_distributor.subscribe(data_distributor.SystemEvents.Log, logger.debug)
data_distributor.subscribe(data_distributor.SystemEvents.ExceptionRaised, logger.exception)
data_distributor.subscribe(
    data_distributor.SystemEvents.SettingsUpdated,
    lambda:
        stream_handler.setLevel(
            "DEBUG"
            if get_value("developer", "debug logging")
            else "INFO")
        or data_distributor.broadcast(
            data_distributor.SystemEvents.Log,
            "Debug logging set to {}".format(
                get_value("developer", "debug logging"))),
    data_distributor.Priority.CRITICAL
)



__all__ = ["data_distributor", 'system_paths', 'config', 'gb_logger']
