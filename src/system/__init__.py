from .event_handler import EventHandler
from .events import SystemEvents, GuiEvents, ComponentEvents

EventHandler.subscribe(SystemEvents.Quit, quit)