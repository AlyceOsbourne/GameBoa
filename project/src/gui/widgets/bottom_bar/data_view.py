from tkinter import Frame, Text
from tkinter.constants import BOTH, DISABLED, END, NORMAL, WORD

from project.src.system import bus as dd, GuiEvents


class DataView(Frame):
    def __init__(self, parent, publish_event):
        super().__init__(parent)
        self.text = Text(self, width=50, height=20, wrap=WORD)
        self.text.pack(fill=BOTH, expand=1)
        self.text.config(state=DISABLED)
        self.publish_event = publish_event
        GuiEvents.Update(self.update_view)

    def update_view(self):
        self.text.config(state=NORMAL)
        self.text.delete(1.0, END)
        self.text.insert(END, dd.request_data(self.publish_event))
        self.text.config(state=DISABLED)
