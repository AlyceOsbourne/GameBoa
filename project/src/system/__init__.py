from .config import load_config, get_value, set_value, save_config
from .event_handler import EventHandler
from .events import SystemEvents, GuiEvents, ComponentEvents

EventHandler.subscribe(SystemEvents.Quit, quit)