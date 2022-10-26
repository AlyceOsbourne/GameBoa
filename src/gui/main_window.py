import tkinter
from tkinter.ttk import *
from .widgets import MenuBarWidget, CartridgeDataWidget, RegistryView
from src.system.paths import ico_path


class MainWindow(tkinter.Tk):


    bottom_bar: Notebook
    bottom_bar_collapse_button: Button

    registry_view: RegistryView
    cartridge_data: CartridgeDataWidget

    def __init__(self):
        super().__init__()
        self.title("GameBoa")
        self.geometry("800x600")
        self.iconphoto(True, tkinter.PhotoImage(file=ico_path))
        self.menu_bar = MenuBarWidget(self)
        self.make_bottom_bar()


    def make_bottom_bar(self):
        self.bottom_bar = Notebook(self, height=150)
        self.bottom_bar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        self.bottom_bar_collapse_button = Button(self, text="▼", command=self.toggle_bottom_bar)
        self.cartridge_data_tab = CartridgeDataWidget(self.bottom_bar)
        self.bottom_bar.add(self.cartridge_data_tab, text="Cartridge Data")
        self.bottom_bar_collapse_button = Button(
            self, text="▼", command=self.toggle_bottom_bar
        )
        self.bottom_bar_collapse_button.pack(side=tkinter.BOTTOM, fill=tkinter.X)

        self.registry_view = RegistryView(self.bottom_bar)
        self.cartridge_data = CartridgeDataWidget(self.bottom_bar)
        self.bottom_bar.add(self.registry_view, text="Registry")
        self.bottom_bar.add(self.cartridge_data, text="Cartridge Data")
        self.bottom_bar.bind(
            "<B1-Motion>",
            lambda e: self.bottom_bar.config(
                height=self.bottom_bar.winfo_height() - e.y
            ),
        )
        self.bottom_bar.bind(
            "<ButtonRelease-1>",
            lambda e: self.bottom_bar.config(
                height=self.bottom_bar.winfo_height() - e.y
            ),
        )

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
















