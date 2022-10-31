from tkinter import Label, Toplevel

from PIL import Image, ImageTk

from project.src.system.system_paths import ico_path, png_path
from project.src.system import data_distributor as dd
from __metadata__ import __authors__, __github_link__, __license__, __version__


class AboutWindow(Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.title("About")
        self.geometry("350x250")
        self.resizable(False, False)
        self.iconbitmap(str(ico_path))

        image = ImageTk.PhotoImage(
            Image.open(png_path, "r").resize((100, 100), Image.ANTIALIAS)
        )

        label = Label(self, image=image)
        label.image = image
        label.pack()

        title = Label(self, text=f"GameBoa {__version__}", font=("Arial", 20))
        title.pack()

        about_text = f"""\
            License: {__license__}\n
            Authors: {__authors__}\n
            Github: {__github_link__}\
            """

        Label(
            self,
            justify="left",
            text=about_text,
            font=("Arial", 10),
        ).pack()


@dd.subscribes_to(dd.GuiEvents.OpenAboutDialog)
def open_about_dialog(parent):
    AboutWindow(parent).grab_set()
