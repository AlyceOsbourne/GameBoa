import tkinter
from tkinter.ttk import *
from src.gui.widgets import MenuBarWidget, CartridgeDataWidget, RegistryView
from src.system.paths import ico_path


class MainWindow(tkinter.Tk):

    left_bar: Notebook
    bottom_bar: Notebook
    bottom_bar_collapse_button: Button
    left_bar_collapse_button: Button
    menu_bar: MenuBarWidget
    cartridge_data_tab: CartridgeDataWidget
    registry_view: RegistryView

    def __init__(self):
        super().__init__()

        self.title("GameBoa")
        self.geometry("800x600")
        self.iconphoto(True, tkinter.PhotoImage(file=ico_path))
        self.menu_bar = MenuBarWidget(self)
        self.menu_bar.pack(side=tkinter.TOP, fill=tkinter.X)
        self.make_bottom_bar()
        self.make_left_bar()

    def make_left_bar(self):
        self.left_bar = Notebook(self, width=200)
        self.left_bar.pack(side=tkinter.LEFT, fill=tkinter.Y)
        self.registry_view = RegistryView(self.left_bar)
        self.registry_view.pack(side=tkinter.LEFT, fill=tkinter.Y)
        self.left_bar.add(self.registry_view, text="Registers")
        self.left_bar_collapse_button = Button(self, text="▶", command=self.toggle_left_bar, width=3)
        self.left_bar_collapse_button.pack(side=tkinter.LEFT, fill=tkinter.Y)
        self.left_bar.bind("<B1-Motion>", lambda e: self.left_bar.config(width=self.left_bar.winfo_width() - e.x))
        self.left_bar.bind("<ButtonRelease-1>", lambda e: self.left_bar.config(width=self.left_bar.winfo_width() - e.x))

    def make_bottom_bar(self):
        self.bottom_bar = Notebook(self)
        self.bottom_bar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        self.cartridge_data_tab = CartridgeDataWidget(self.bottom_bar)
        self.bottom_bar.add(self.cartridge_data_tab, text="Cartridge Data")
        self.bottom_bar_collapse_button = Button(self, text="▼", command=self.toggle_bottom_bar)
        self.bottom_bar_collapse_button.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        self.bottom_bar.bind("<B1-Motion>",
                             lambda e: self.bottom_bar.config(height=self.bottom_bar.winfo_height() - e.y))
        self.bottom_bar.bind("<ButtonRelease-1>",
                             lambda e: self.bottom_bar.config(height=self.bottom_bar.winfo_height() - e.y))

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

    def toggle_left_bar(self):
        if self.left_bar.winfo_ismapped():
            self.left_bar.pack_forget()
            self.left_bar_collapse_button.pack(side=tkinter.LEFT, fill=tkinter.Y)
            self.left_bar_collapse_button.config(text="◀")
        else:
            self.left_bar.pack(side=tkinter.LEFT, fill=tkinter.Y)
            self.left_bar_collapse_button.pack_forget()
            self.left_bar_collapse_button.pack(side=tkinter.LEFT, fill=tkinter.Y)
            self.left_bar_collapse_button.config(text="▶")

    def run(self):
        self.mainloop()
















