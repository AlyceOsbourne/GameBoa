from tkinter import Frame, Text
from tkinter.constants import BOTH, DISABLED, END, NORMAL, WORD
from project.src.system.event_handler import EventHandler
from project.src.system.events import GuiEvents, SystemEvents, ComponentEvents

class RegistryView(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.text = Text(self, width=50, height=20, wrap=WORD)
        self.text.pack(fill=BOTH, expand=1)
        self.text.config(state=DISABLED)
        EventHandler.subscribe(ComponentEvents.RegisterWrite, self.update_view)

    def update_view(self, data):
        self.text.config(state=NORMAL)
        self.text.delete(1.0, END)
        self.text.insert(END, data)
        self.text.config(state=DISABLED)
