from tkinter import ttk

from project.src.components.cartridge import HEADER_FORMAT
from project.src.system import bus as dd, ComponentEvents


class CartridgeDataWidget(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        for i, attr in enumerate(sorted(f[0] for f in HEADER_FORMAT if f[0] not in ["logo", "global_checksum"])):
            label = ttk.Label(self, text=attr)
            value = ttk.Label(self, text="N/A")

            label.grid(row=i // 7 * 2, column=i % 7 * 2, sticky="w")
            value.grid(row=i // 7 * 2 + 1, column=i % 7 * 2, sticky="w")
            setattr(self, attr + "_value", value)

        ComponentEvents.HeaderLoaded(self.update_data)
        ComponentEvents.RequestReset(self.clear)

    def update_data(self, header_data):
        header_data = header_data._asdict()
        for k in (k for k in header_data if k not in ["logo", "global_checksum"]):
            getattr(self, k + "_value").config(text=str(header_data[k]))

    def clear(self, *_):
        for i, attr in enumerate(sorted(f[0] for f in HEADER_FORMAT if f[0] not in ["logo", "global_checksum"])):
            getattr(self, attr + "_value").config(text="N/A")
