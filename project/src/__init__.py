from .system import bus
from .components import *
from .gui import *
from . import structs

def run():
    main_window = MainWindow()
    main_window.mainloop()

__all__ = [
    "run",
]
