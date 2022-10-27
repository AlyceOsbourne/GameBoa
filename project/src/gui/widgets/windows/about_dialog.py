# tkinter top level window that shows about information
from tkinter import (
    Label,
    Toplevel,
)

from PIL import Image, ImageTk
from __metadata__ import __authors__, __version__, __license__, __copyright_year__, __github_link__
from project.src.system.event_handler import EventHandler
from project.src.system.events import GuiEvents
from project.src.system import png_path, ico_path

class AboutWindow(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("About")
        self.geometry("350x250")
        self.resizable(False, False)
        self.iconbitmap(str(ico_path))
        image = ImageTk.PhotoImage(Image.open(png_path, 'r').resize((100, 100), Image.ANTIALIAS))
        label = Label(self, image=image)
        label.image = image
        label.pack()
        title = Label(self, text=f"GameBoa v{__version__}", font=("Arial", 20))
        title.pack()
        about_text = f"""
{__license__} {__copyright_year__}
Authors: {__authors__}
Github: {__github_link__}
"""
        Label(
            self,
            text=about_text,
            font=("Arial", 10),
            justify="left",
        ).pack()


@EventHandler.subscriber(GuiEvents.OpenAboutDialog)
def open_about_dialog(parent):
    AboutWindow(parent).mainloop()