import tkinter
from tkinter.ttk import Notebook
import sys
from .widgets import *
from .widgets import MenuBarWidget, CartridgeDataWidget, RegistryView, open_load_rom_dialog, open_settings_dialog
from __paths__ import ico_path

class MainWindow(tkinter.Tk):
    bottom_bar: Notebook
    bottom_bar_collapse_button: tkinter.Button

    registry_view: RegistryView
    cartridge_data_tab: CartridgeDataWidget

    def __init__(self):
        super().__init__()
        self.title("GameBoa")
        self.geometry("800x600")
        if not hasattr(sys, '_MEIPASS'):
            self.iconbitmap(ico_path)
        self.menu_bar = MenuBarWidget(self)
        self.make_bottom_bar()

    def make_bottom_bar(self):
        self.bottom_bar = Notebook(self, height=150)
        self.bottom_bar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        self.bottom_bar_collapse_button = tkinter.Button(self, text="▼", command=self.toggle_bottom_bar)
        self.cartridge_data_tab = CartridgeDataWidget(self.bottom_bar)
        self.registry_view = RegistryView(self.bottom_bar)
        self.bottom_bar.add(self.cartridge_data_tab, text="Cartridge Data")
        self.bottom_bar.add(self.registry_view, text="Registry")
        self.bottom_bar_collapse_button = tkinter.Button(
            self, text="▼", command=self.toggle_bottom_bar
        )
        self.bottom_bar_collapse_button.pack(side=tkinter.BOTTOM, fill=tkinter.X)



    def toggle_bottom_bar(self):
        if self.bottom_bar.winfo_ismapped():
            self.bottom_bar.pack_forget()
            self.bottom_bar_collapse_button.pack(side=tkinter.BOTTOM, fill=tkinter.X)
            self.bottom_bar_collapse_button.config(text="▲")
        else:
            self.bottom_bar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
            self.bottom_bar_collapse_button.pack_forget()
            self.bottom_bar_collapse_button.pack(side=tkinter.BOTTOM, fill=tkinter.X)
            self.bottom_bar_collapse_button.config(text="▼")

    def show(self):
        self.mainloop()