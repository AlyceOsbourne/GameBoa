from enum import auto, Flag
from itertools import count

EVENT_IDS = count()


class Event(Flag):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return next(EVENT_IDS)

    @staticmethod
    def get_all_events():
        return {
            member.name: member
            for subcls in Event.__subclasses__()
            for member in subcls.__members__.values()
        }


class SystemEvents(Event):
    Log = auto()
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
