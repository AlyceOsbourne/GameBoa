from itertools import count
from enum import Flag, auto

event_ids = count()

class Event(Flag):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return next(event_ids)

    @staticmethod
    def get_all_events():
        return {member.name: member for subcls in Event.__subclasses__() for member in subcls.__members__.values()}


class SystemEvents(Event):
    Quit = auto()
    SettingsUpdated = auto()
    ExceptionRaised = auto()

class GuiEvents(Event):
    Update = auto()
    WindowShow = auto()
    LoadRomFromLibrary = auto()
    DeleteRomFromLibrary = auto()
    UpdateRomLibrary = auto()
    OpenLoadRomDialog = auto()
    OpenSettingsDialog = auto()
    OpenAboutDialog = auto()
    RequestRegistryStatus = auto()
    RequestMemoryStatus = auto()


class ComponentEvents(Event):
    RequestRegisterRead = auto()
    RequestRegisterWrite = auto()
    RequestMemoryRead = auto
    RequestMemoryWrite = auto()
    MemoryLoaded = auto()
    RequestOpCode = auto()
    RequestDecode = auto()
    RequestExecute = auto()
    RomLoaded = auto()
    RomUnloaded = auto()
    HeaderLoaded = auto()
    RequestReset = auto()


print("Loaded Events", *Event.get_all_events(), sep="\n", end="\n\n")