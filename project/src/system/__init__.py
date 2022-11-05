import pprint
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

    RequestExecute = auto()

    RequestMemoryRead = auto()
    RequestMemoryWrite = auto()

    RequestRegisterRead = auto()
    RequestRegisterWrite = auto()

    RequestHalt = auto()
    RequestUnhalt = auto()

    RequestInterrupt = auto()
    RequestInterruptAcknowledge = auto()
    RequestInterruptDisable = auto()
    RequestInterruptEnable = auto()

    RequestTimerTick = auto()
    RequestTimerRead = auto()
    RequestTimerWrite = auto()

    RequestJoypadRead = auto()
    RequestJoypadWrite = auto()

    RequestSerialRead = auto()
    RequestSerialWrite = auto()

    RequestVideoRead = auto()
    RequestVideoWrite = auto()

    RequestAudioRead = auto()
    RequestAudioWrite = auto()



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

if events := Event.get_all_events():
    LogEvent.LogInfo.emit(f'System loaded {len(events)} events')
    LogEvent.LogDebug.emit(f'Events: \n{pprint.pformat(list(events.keys()), indent=4)}')

LogEvent.LogDebug.emit('System initialized')

__all__ = ["bus", 'system_paths', 'config', 'LogEvent', 'SystemEvents', 'GuiEvents', 'ComponentEvents']
