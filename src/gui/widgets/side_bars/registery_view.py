from tkinter import *
from src.system import EventHandler, GuiEvents

class RegistryView(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.text = Text(self, width=50, height=20, wrap=WORD)
        self.text.pack(fill=BOTH, expand=1)
        self.text.config(state=DISABLED)
        EventHandler.subscribe(GuiEvents.UpdateRegisterView, self.update_view)

    def update_view(self, data):
        self.text.config(state=NORMAL)
        self.text.delete(1.0, END)
        self.text.insert(END, data)
        self.text.config(state=DISABLED)

