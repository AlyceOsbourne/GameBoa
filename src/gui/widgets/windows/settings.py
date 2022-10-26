from tkinter.ttk import Notebook
from Tkinter import BooleanVar, DoubleVar, IntVar, StringVar
from tkinter import (
    Entry,
    Frame,
    Label,
    Button,
    Spinbox,
    Toplevel,
    filedialog,
    Checkbutton,
)

from src.system import EventHandler, GuiEvents, SystemEvents
from src.system.config import (
    sections,
    get_value,
    set_value,
    option_type,
    save_config,
    section_options,
)


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

        tabs.pack(expand=1, fill="both")

    def create_tab(self, tab, section):
        for index, option in enumerate(section_options(section)):
            label = Label(tab, text=option)
            label.grid(row=index, column=0, sticky="w")
            value_type = option_type(section, option)

            if isinstance(value_type, bool):
                value = BooleanVar()
                value.set(get_value(section, option))
                value.trace(
                    "w",
                    lambda *args, section=section, option=option, value=value: set_value(
                        section, option, value.get()
                    ),
                )
                value = Checkbutton(tab, variable=value)
            elif isinstance(value_type, str):
                value = StringVar()
                value.set(get_value(section, option))
                value.trace(
                    "w",
                    lambda *args, section=section, option=option, value=value: set_value(
                        section, option, value.get()
                    ),
                )
                value = Entry(tab, textvariable=value)
            elif isinstance(value_type, int):
                value = IntVar()
                value.set(get_value(section, option))
                value.trace(
                    "w",
                    lambda *args, section=section, option=option, value=value: set_value(
                        section, option, value.get()
                    ),
                )
                value = Spinbox(tab, from_=0, to=100, textvariable=value)
            elif isinstance(value_type, float):
                value = DoubleVar()
                value.set(get_value(section, option))
                value.trace(
                    "w",
                    lambda *args, section=section, option=option, value=value: set_value(
                        section, option, value.get()
                    ),
                )
                value = Spinbox(tab, from_=0.0, to=100.0, textvariable=value)
            else:
                raise TypeError(f"Invalid type for option: {option}")

            value.grid(row=index, column=1, columnspan=3, sticky="w", padx=5)

            if section == "paths":
                button = Button(
                    tab,
                    text="Browse",
                    command=lambda section=section, option=option, value=value: self.browse(
                        section, option, value
                    ),
                )
                button.grid(row=index, column=4, sticky="w", columnspan=2)

    def browse(self, section, option, value):
        if option == "roms":
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


def open_settings_dialog(parent):
    SettingsWindow(parent).mainloop()
