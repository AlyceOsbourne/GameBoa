from tkinter import ttk

from project.src.system import data_distributor
from project.src.structs.gb_header import HEADER_FORMAT


class CartridgeDataWidget(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        for index, attribute in enumerate(
            sorted(
                format[0]
                for format in HEADER_FORMAT
                if format[0] not in ["logo", "global_checksum"]
            )
        ):
            label = ttk.Label(self, text=attribute)
            value = ttk.Label(self, text="N/A")

            label.grid(row=index // 7 * 2, column=index % 7 * 2, sticky="w")
            value.grid(row=index // 7 * 2 + 1, column=index % 7 * 2, sticky="w")
            setattr(self, attribute + "_value", value)

        data_distributor.subscribe(
            data_distributor.ComponentEvents.HeaderLoaded, self.update_data
        )
        data_distributor.subscribe(
            data_distributor.ComponentEvents.RequestReset, self.clear
        )

    def update_data(self, header_data):
        header_data_dict = header_data._asdict()

        for key_item in (
            key for key in header_data_dict if key not in ["logo", "global_checksum"]
        ):
            getattr(self, key_item + "_value").config(
                text=str(header_data_dict[key_item])
            )

    def clear(self):
        for index, attribute in enumerate(
            sorted(
                format[0]
                for format in HEADER_FORMAT
                if format[0] not in ["logo", "global_checksum"]
            )
        ):
            getattr(self, attribute + "_value").config(text="N/A")
