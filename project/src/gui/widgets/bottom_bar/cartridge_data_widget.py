from tkinter import ttk

from project.src.structs.gb_header import HEADER_FORMAT
from project.src.system.event_handler import EventHandler
from project.src.system.events import SystemEvents, ComponentEvents



class CartridgeDataWidget(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        for i, attr in enumerate(sorted(f[0] for f in HEADER_FORMAT if f[0] not in ['logo', 'global_checksum'])):
            label = ttk.Label(self, text=attr)
            value = ttk.Label(self, text='N/A')

            label.grid(row=i // 7 * 2, column=i % 7 * 2, sticky= 'w')
            value.grid(row=i // 7 * 2 + 1, column=i % 7 * 2, sticky= 'w')
            setattr(self, attr + "_value", value)

        EventHandler.subscribe(ComponentEvents.HeaderLoaded, self.update_data)
        EventHandler.subscribe(ComponentEvents.RequestReset, self.clear)

    def update_data(self, header_data):
        header_data = header_data._asdict()
        for k in (k for k in header_data if k not in ['logo', 'global_checksum']):
            getattr(self, k + "_value").config(text=str(header_data[k]))


    def clear(self):
        for i, attr in enumerate(sorted(f[0] for f in HEADER_FORMAT if f[0] not in ['logo', 'global_checksum'])):
            getattr(self, attr + "_value").config(text='N/A')

