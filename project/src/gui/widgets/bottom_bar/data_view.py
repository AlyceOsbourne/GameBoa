from tkinter import Frame, Text
from tkinter.constants import BOTH, DISABLED, END, NORMAL, WORD

from project.src.system import EventHandler, GuiEvents


class DataView(Frame):
    def __init__(self, parent, publish_event):
        super().__init__(parent)
        self.text = Text(self, width=50, height=20, wrap=WORD)
        self.text.pack(fill=BOTH, expand=1)
        self.text.config(state=DISABLED)
        self.publish_event = publish_event
        EventHandler.subscribe(GuiEvents.Update, self.fetch_data)

    def update_view(self, data):
        self.text.config(state=NORMAL)
        self.text.delete(1.0, END)
        self.text.insert(END, data)
        self.text.config(state=DISABLED)

    def fetch_data(self):
        EventHandler.publish(self.publish_event, self.update_view)

