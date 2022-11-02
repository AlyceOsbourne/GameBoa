from tkinter.ttk import Notebook
from tkinter import (
    Entry,
    Frame,
    Label,
    Button,
    Spinbox,
    Toplevel,
    filedialog,
    Checkbutton,
    BooleanVar,
    DoubleVar,
    IntVar,
    StringVar,
)

from project.src.system import bus as dd, GuiEvents, SystemEvents
from project.src.system.config import (
    sections,
    get_value,
    set_value,
    option_type,
    save_config,
    load_config,
    section_options,
    reset_to_defaults,
)


class SettingsWindow(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Settings")
        self.geometry("500x500")
        self.tabs = Notebook(self)
        self.create_tabs(self.tabs)
        self.make_buttons()
        self.reset = None
        self.save_button = None
        self.cancel_button = None

    def make_buttons(self):
        self.reset = Button(self, text="Reset to Defaults", command=self.reset)
        self.save_button = Button(self, text="Save", command=self.save)
        self.cancel_button = Button(self, text="Cancel", command=self.cancel)
        self.reset.pack(side="left", padx=5, pady=5)
        self.save_button.pack(side="right", padx=5, pady=5)
        self.cancel_button.pack(side="right", padx=5, pady=5)

    def create_tabs(self, tabs):
        for section in sections():
            tab = Frame(tabs)
            self.create_tab(tab, section)
            tabs.add(tab, text=section)

        tabs.pack(expand=1, fill="both")
        tabs.pack_configure(padx=5, pady=5, ipadx=5, ipady=5)

    def create_tab(self, tab, section):
        for index, option in enumerate(section_options(section)):
            label = Label(tab, text=option)
            label.grid(row=index, column=0, sticky="w")
            value_type = option_type(section, option)

            if value_type == bool:
                value = BooleanVar()
                value.set(get_value(section, option))
                value.trace(
                    "w",
                    lambda *args, section=section, option=option, value=value: set_value(
                        section, option, value.get()
                    ),
                )
                value = Checkbutton(tab, variable=value)
            elif value_type == str:
                value = StringVar()
                value.set(get_value(section, option))
                value.trace(
                    "w",
                    lambda *args, section=section, option=option, value=value: set_value(
                        section, option, value.get()
                    ),
                )
                value = Entry(tab, textvariable=value)
                value.config(width=50)
            elif value_type == int:
                value = IntVar()
                value.set(get_value(section, option))
                value.trace(
                    "w",
                    lambda *args, section=section, option=option, value=value: set_value(
                        section, option, value.get()
                    ),
                )
                value = Spinbox(tab, from_=0, to=100, textvariable=value)
            elif value_type == float:
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
            value.grid(row=index, column=1, columnspan=3, padx=5)
            value.grid_configure(ipadx=20, ipady=10)
            if section == "paths":
                button = Button(
                    tab,
                    text="Browse",
                    command=lambda section=section, option=option, value=value: self.browse(
                        section, option, value
                    ),
                )
                button.grid(row=index, column=4, sticky="w", columnspan=2)

    def browse(self, section, option, value: Entry):
        if option == "roms":
            file = filedialog.askdirectory(initialdir=get_value(section, option))
        else:
            file = filedialog.askopenfilename(initialdir=get_value(section, option))

        if file:
            value.delete(0, "end")
            value.insert(0, file)
            set_value(section, option, file)

    def save(self):
        save_config()
        SystemEvents.SettingsUpdated()
        self.destroy()

    def cancel(self):
        load_config()
        self.destroy()

    def reset(self):
        reset_to_defaults()
        for tab in self.tabs.winfo_children():
            for child in tab.winfo_children():
                child.destroy()
            tab.destroy()
        self.create_tabs(self.tabs)


@GuiEvents.OpenSettingsDialog
def open_settings_dialog(parent):
    SettingsWindow(parent).grab_set()
