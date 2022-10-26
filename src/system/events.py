from itertools import count
from enum import Flag, auto

event_ids = count()

class Event(Flag):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return next(event_ids)

class SystemEvents(Event):
    Quit = auto()
    RomLoaded = auto()
    RomUnloaded = auto()
    HeaderLoaded = auto()
    LoadSettings = auto()
    SaveSettings = auto()

class GuiEvents(Event):
    OpenLoadRomDialog = auto()
    OpenSettings = auto()
    OpenAbout = auto()
    RequestRegisterStatus = auto
    UpdateRegisterView = auto()

class ComponentEvents(Event):
    UpdateRegister = auto()
    UpdateMemory = auto()
    UpdateStack = auto()