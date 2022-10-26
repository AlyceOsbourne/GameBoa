# a tkinter window that has tabs for each section in the config,
# and we create the widgets based on the value of the config

from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Notebook

from src.system.config import get_value, set_value, sections, section_options, option_type, save_config
from src.system import EventHandler, SystemEvents, GuiEvents



class SettingsWindow(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Settings")
        self.geometry("500x500")
        self.tabs = Notebook(self)
        self.create_tabs(self.tabs)

    def create_tabs(self, tabs):
        for section in sections():
            tab = Frame(tabs)
            self.create_tab(tab, section)
            tabs.add(tab, text=section)
        # make tabs fill width of window
        tabs.pack(expand=1, fill="both")

    def create_tab(self, tab, section):
        for i, option in enumerate(section_options(section)):
            label = Label(tab, text=option)
            label.grid(row=i, column=0, sticky="w")
            value_type = option_type(section, option)
            if value_type == bool:
                value = BooleanVar()
                value.set(get_value(section, option))
                value.trace("w", lambda *args, section=section, option=option, value=value: set_value(section, option, value.get()))
                value = Checkbutton(tab, variable=value)
            elif value_type == str:
                value = StringVar()
                value.set(get_value(section, option))
                value.trace("w", lambda *args, section=section, option=option, value=value: set_value(section, option, value.get()))
                value = Entry(tab, textvariable=value)
            elif value_type == int:
                value = IntVar()
                value.set(get_value(section, option))
                value.trace("w", lambda *args, section=section, option=option, value=value: set_value(section, option, value.get()))
                value = Spinbox(tab, from_=0, to=100, textvariable=value)
            elif value_type == float:
                value = DoubleVar()
                value.set(get_value(section, option))
                value.trace("w", lambda *args, section=section, option=option, value=value: set_value(section, option, value.get()))
                value = Spinbox(tab, from_=0, to=100, textvariable=value)
            else:
                raise TypeError("Invalid type for option: " + option)
            value.grid(row=i, column=1, columnspan=3, sticky="w", padx=5)
            if section in [
                'paths'
            ]:
                button = Button(tab, text="Browse", command=lambda section=section, option=option, value=value: self.browse(section, option, value))
                button.grid(row=i, column=4, sticky="w", columnspan=2)

    def browse(self, section, option, value):
        if option == 'roms':
            file = filedialog.askdirectory(initialdir=get_value(section, option))
        else:
            file = filedialog.askopenfilename(initialdir=get_value(section, option))
        if file:
            value.set(file)
            set_value(section, option, file)

    def save(self):
        save_config()
        EventHandler.publish(SystemEvents.SaveSettings)
        self.destroy()

    def cancel(self):
        self.destroy()

@EventHandler.subscriber(GuiEvents.OpenSettings)
def open_settings(parent):
    SettingsWindow(parent).mainloop()

