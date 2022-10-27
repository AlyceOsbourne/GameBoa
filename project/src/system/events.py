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
    RomLoaded = auto()
    RomUnloaded = auto()
    HeaderLoaded = auto()
    SettingsUpdated = auto()

class GuiEvents(Event):
    LoadRomFromlibrary = auto()
    UnloadRom = auto()
    OpenLoadRomDialog = auto()
    OpenSettingsDialog = auto()
    OpenAboutDialog = auto()
    RequestRegisterStatus = auto()
    UpdateRegisterView = auto()

class ComponentEvents(Event):
    RegisterWrite = auto()


print("Loaded Events", *Event.get_all_events(), sep="\n", end="\n\n")