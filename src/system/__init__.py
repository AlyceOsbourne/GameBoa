import pathlib
import importlib
from .event_handler import EventHandler
from .events import SystemEvents, GuiEvents

for file in (pathlib.Path(__file__).parent / 'listeners').rglob('*.py'):
    if file.name != '__init__.py':
        module = importlib.import_module(f'system.listeners.{file.stem}')
        if hasattr(module, 'load'):
            module.load()

EventHandler.subscribe(SystemEvents.Quit, quit)