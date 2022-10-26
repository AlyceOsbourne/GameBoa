import tkinter
from tkinter.ttk import *
from src.gui.widgets import MenuBarWidget, CartridgeDataWidget

class MainWindow(tkinter.Tk):
    def __init__(self):
        super().__init__()

        self.title("GameBoa")
        self.geometry("800x600")

        self.menu_bar = MenuBarWidget(self)
        self.menu_bar.pack(side=tkinter.TOP, fill=tkinter.X)

        self.bottom_bar = Notebook(self)
        self.bottom_bar.pack(side=tkinter.BOTTOM, fill=tkinter.X)

        self.cartridge_data_tab = CartridgeDataWidget(self.bottom_bar)
        self.bottom_bar.add(self.cartridge_data_tab, text="Cartridge Data")

        self.collapse_button = Button(self, text="▼", command=self.toggle_bottom_bar)
        self.collapse_button.pack(side=tkinter.BOTTOM, fill=tkinter.X)

        self.bottom_bar.bind("<B1-Motion>", lambda e: self.bottom_bar.config(height=self.bottom_bar.winfo_height() - e.y))
        self.bottom_bar.bind("<ButtonRelease-1>", lambda e: self.bottom_bar.config(height=self.bottom_bar.winfo_height() - e.y))


    def toggle_bottom_bar(self):
        if self.bottom_bar.winfo_ismapped():
            self.bottom_bar.pack_forget()
            self.collapse_button.pack(side=tkinter.BOTTOM, fill=tkinter.X)
            self.collapse_button.config(text="▲")
        else:
            self.bottom_bar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
            self.collapse_button.pack_forget()
            self.collapse_button.pack(side=tkinter.BOTTOM, fill=tkinter.X)
            self.collapse_button.config(text="▼")
















