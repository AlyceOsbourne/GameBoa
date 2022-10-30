import tkinter
from tkinter.ttk import Notebook
from PIL import Image, ImageTk
from project.src.system import (
    get_value,
    EventHandler,
    SystemEvents,
    GuiEvents,
    ComponentEvents,
    ico_path,
    png_path,
)
from .widgets import *


class MainWindow(tkinter.Tk):
    bottom_bar: Notebook
    bottom_bar_collapse_button: tkinter.Button

    registry_view: DataView
    memory_view: DataView

    cartridge_data_tab: CartridgeDataWidget

    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.iconbitmap(ico_path)
        self.menu_bar = MenuBarWidget(self)
        self.make_bottom_bar()
        self.update_dev_view()
        self.rom_listbox = RomLibrary(self)
        self.rom_listbox.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)
        self.canvas = tkinter.Canvas(
            self, width=self.winfo_screenwidth(), height=self.winfo_screenheight()
        )
        self.canvas.create_rectangle(
            0, 0, self.winfo_screenwidth(), self.winfo_screenheight(), fill="black"
        )

        self.canvas.bind(
            "<Configure>", lambda e: self.canvas.config(width=e.width, height=e.height)
        )

        EventHandler.subscribe(SystemEvents.SettingsUpdated, self.update_dev_view)
        EventHandler.subscribe(SystemEvents.Quit, self.destroy)
        EventHandler.subscribe(ComponentEvents.RomLoaded, self.switch_to_canvas)
        EventHandler.subscribe(ComponentEvents.RequestReset, self.switch_to_library)

    def make_bottom_bar(self):
        self.bottom_bar = Notebook(self, height=150)
        self.bottom_bar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        self.bottom_bar_collapse_button = tkinter.Button(
            self, text="▼", command=self.collapse_bottom_bar
        )
        self.cartridge_data_tab = CartridgeDataWidget(self.bottom_bar)
        self.registry_view = DataView(self.bottom_bar, GuiEvents.RequestRegistryStatus)
        self.memory_view = DataView(self.bottom_bar, GuiEvents.RequestMemoryStatus)

        self.bottom_bar.add(self.cartridge_data_tab, text="Cartridge Data")
        self.bottom_bar.add(self.registry_view, text="Registry")
        self.bottom_bar.add(self.memory_view, text="Memory")
        self.bottom_bar_collapse_button = tkinter.Button(
            self, text="▼", command=self.collapse_bottom_bar
        )
        self.bottom_bar_collapse_button.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        self.toggle_bottom_bar()

    def toggle_bottom_bar(self):
        if get_value("developer", "debug"):
            self.bottom_bar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
            self.bottom_bar_collapse_button.pack_forget()
            self.bottom_bar_collapse_button.pack(side=tkinter.BOTTOM, fill=tkinter.X)
            self.bottom_bar_collapse_button.config(text="▼")
        else:
            self.bottom_bar_collapse_button.pack_forget()
            self.bottom_bar.pack_forget()

    def collapse_bottom_bar(self):
        if self.bottom_bar.winfo_ismapped():
            self.bottom_bar.pack_forget()
            self.bottom_bar_collapse_button.pack(side=tkinter.BOTTOM, fill=tkinter.X)
            self.bottom_bar_collapse_button.config(text="▲")
        else:
            was_canvas = self.canvas.winfo_ismapped()
            if was_canvas:
                self.canvas.pack_forget()
            self.bottom_bar.pack(side=tkinter.BOTTOM, fill=tkinter.BOTH)
            self.bottom_bar_collapse_button.pack_forget()
            self.bottom_bar_collapse_button.pack(side=tkinter.BOTTOM, fill=tkinter.X)
            self.bottom_bar_collapse_button.config(text="▼")
            if was_canvas:
                self.canvas.pack(side=tkinter.TOP, fill=tkinter.BOTH)

    def update_title_bar(self):
        # if debug mode is enabled, set title bar to GameBoa (debug)
        if get_value("developer", "debug"):
            self.title("GameBoa (debug)")
        else:
            self.title("GameBoa")

    def switch_to_canvas(self, _):
        self.rom_listbox.pack_forget()
        self.canvas.pack(side=tkinter.TOP, fill=tkinter.BOTH)

    def switch_to_library(self):
        self.canvas.pack_forget()
        self.rom_listbox.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

    def update_dev_view(self):
        self.update_title_bar()
        self.toggle_bottom_bar()

    def show(self):
        self.update_loop()
        self.mainloop()

    def update_loop(self):
        self.after(1000, self.update_loop)
        EventHandler.publish(GuiEvents.Update)


__all__ = ["MainWindow"]
