# a canvas that we can draw the gameboy screen on
from array import array
from tkinter import Canvas

from PIL import ImageTk, Image

from project.src.system.system_paths import png_path, ico_path

pixel_color_mapping = {0x00: "#FFFFFF", 0x01: "#AAAAAA", 0x10: "#555555", 0x11: "#000000"}


class GameScreen(Canvas):
    # the canvas can be resized, but the number of "pixels" is fixed
    def __init__(self, master):
        super().__init__(master, bg="black")
        self.bind("<Configure>", self.on_resize)
        self.after(16, self.update)

    def update(self) -> None:
        self.update_pixel_data()
        self.after(16, self.update)

    def on_resize(self, event):
        self.configure(width=event.width, height=event.height)
        self.update_pixel_data()

    def update_pixel_data(self):
        self.delete("all")
        self.create_image(
            0,
            0,
            image=ImageTk.PhotoImage(Image.open(ico_path), width=self.winfo_width(), height=self.winfo_height()),
            anchor="nw",
            tags="all",
            state="normal",
        )
        self.create_text(
            self.winfo_width() // 2, self.winfo_height() * 0.75, text="GameBoa", fill="white", font=("Arial", 32)
        )
