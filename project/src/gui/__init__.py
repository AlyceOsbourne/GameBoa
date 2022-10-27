import tkinter
from tkinter.ttk import Notebook
from project.src.system import get_value, EventHandler, SystemEvents, GuiEvents, ico_path
from .widgets import *



class MainWindow(tkinter.Tk):
    bottom_bar: Notebook
    bottom_bar_collapse_button: tkinter.Button

    registry_view: RegistryView
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
        self.canvas = tkinter.Canvas(self, width=800, height=600)

        EventHandler.subscribe(GuiEvents.WindowShow, self.show)
        EventHandler.subscribe(SystemEvents.SettingsUpdated, self.update_dev_view)
        EventHandler.subscribe(SystemEvents.Quit, self.destroy)


    def make_bottom_bar(self):
        self.bottom_bar = Notebook(self, height=150)
        self.bottom_bar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        self.bottom_bar_collapse_button = tkinter.Button(self, text="▼", command=self.collapse_bottom_bar)
        self.cartridge_data_tab = CartridgeDataWidget(self.bottom_bar)
        self.registry_view = RegistryView(self.bottom_bar)
        self.bottom_bar.add(self.cartridge_data_tab, text="Cartridge Data")
        self.bottom_bar.add(self.registry_view, text="Registry")
        self.bottom_bar_collapse_button = tkinter.Button(
            self, text="▼", command=self.collapse_bottom_bar
        )
        self.bottom_bar_collapse_button.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        self.toggle_bottom_bar()

    def toggle_bottom_bar(self):
        if get_value('developer', 'debug'):
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
            self.bottom_bar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
            self.bottom_bar_collapse_button.pack_forget()
            self.bottom_bar_collapse_button.pack(side=tkinter.BOTTOM, fill=tkinter.X)
            self.bottom_bar_collapse_button.config(text="▼")

    def update_title_bar(self):
        # if debug mode is enabled, set title bar to GameBoa (debug)
        if get_value('developer', 'debug'):
            self.title("GameBoa (debug)")
        else:
            self.title("GameBoa")

    def update_dev_view(self):
        self.update_title_bar()
        self.toggle_bottom_bar()

    def show(self):
        try:
            self.mainloop()
        except KeyboardInterrupt:
            EventHandler.publish(SystemEvents.Quit)
        except Exception as e:
            EventHandler.publish(SystemEvents.ExceptionRaised, e)
            raise e

__all__ = [
    'MainWindow'
]