from enum import auto
from .config import * ; load_config()
from .system_paths import *
from .gb_logger import *
from .bus import *


class LogEvent(Event):
    LogError = auto()
    LogWarning = auto()
    LogCritical = auto()
    LogInfo = auto()
    LogDebug = auto()
    LogToggleOutput = auto()


class SystemEvents(Event):
    Quit = auto()
    ExceptionRaised = auto()
    SettingsUpdated = auto()


class GuiEvents(Event):
    Update = auto()
    OpenAboutDialog = auto()
    UpdateRomLibrary = auto()
    OpenLoadRomDialog = auto()
    LoadRomFromLibrary = auto()
    OpenSettingsDialog = auto()
    RequestMemoryStatus = auto()
    DeleteRomFromLibrary = auto()
    RequestRegistryStatus = auto()


class ComponentEvents(Event):
    RomLoaded = auto()
    RomUnloaded = auto()

    HeaderLoaded = auto()
    RequestReset = auto()

    RequestOpCode = auto()
    RequestDecode = auto()
    RequestExecute = auto()

    RequestMemoryRead = auto()
    RequestMemoryWrite = auto()

    RequestRegisterRead = auto()
    RequestRegisterWrite = auto()


LogEvent.LogDebug.subscribe(logger.debug)
LogEvent.LogInfo.subscribe(logger.info)
LogEvent.LogCritical.subscribe(logger.critical)
LogEvent.LogWarning.subscribe(logger.warning)
LogEvent.LogError.subscribe(logger.error)

LogEvent.LogToggleOutput.subscribe(lambda mode: logger.setLevel(mode))

SystemEvents.SettingsUpdated.subscribe(
    lambda: logger.setLevel(
        'DEBUG'
        if get_value('developer', 'debug logging')
        else 'INFO'
    ))

SystemEvents.ExceptionRaised.subscribe(LogEvent.LogError.emit)


__all__ = ["bus", 'system_paths', 'config', 'gb_logger', 'LogEvent', 'SystemEvents', 'GuiEvents', 'ComponentEvents']
