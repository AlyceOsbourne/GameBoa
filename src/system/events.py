from itertools import count
from enum import Flag, auto

event_ids = count()

class Event(Flag):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return next(event_ids)

class SystemEvents(Event):
    Quit = auto()
    LoadRom = auto()
    UnloadRom = auto()
    RomLoaded = auto()
    RomUnloaded = auto()
    HeaderLoaded = auto()
    LoadSettings = auto()
    SaveSettings = auto()

class GuiEvents(Event):
    OpenSettings = auto()
    OpenAbout = auto()
    UpdateRegisterView = auto()