from .config import *
from .system_paths import *
from .gb_logger import *
from . import bus


bus.subscribe(bus.SystemEvents.Log, logger.debug)
bus.subscribe(bus.SystemEvents.ExceptionRaised, logger.exception)
bus.subscribe(
    bus.SystemEvents.SettingsUpdated,
    lambda:
        stream_handler.setLevel(
            "DEBUG"
            if get_value("developer", "debug logging")
            else "INFO")
        or bus.broadcast(
            bus.SystemEvents.Log,
            "Debug logging set to {}".format(
                get_value("developer", "debug logging"))),
    bus.Priority.CRITICAL
)




__all__ = ["bus", 'system_paths', 'config', 'gb_logger']
