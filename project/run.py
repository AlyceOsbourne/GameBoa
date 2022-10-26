from project.src.gui import MainWindow, open_load_rom_dialog, open_settings_dialog

from functools import partial

from project.src.system.event_handler import EventHandler
from project.src.system.events import GuiEvents, SystemEvents

open_settings_dialog_publisher = partial(EventHandler.publish, GuiEvents.OpenSettingsDialog)
open_load_rom_dialog_publisher = partial(EventHandler.publish, GuiEvents.OpenLoadRomDialog)
open_about_dialog_publisher = partial(EventHandler.publish, GuiEvents.OpenAboutDialog)
unload_rom_publisher = partial(EventHandler.publish, GuiEvents.UnloadRom)
quit_program_publisher = partial(EventHandler.publish, SystemEvents.Quit)

main_window = MainWindow(
    open_load_rom_dialog_publisher,
    unload_rom_publisher,
    quit_program_publisher,
    open_settings_dialog_publisher,
    open_about_dialog_publisher
)

EventHandler.subscribe(SystemEvents.Quit, main_window.destroy)
EventHandler.subscribe(GuiEvents.OpenLoadRomDialog, open_load_rom_dialog)
EventHandler.subscribe(GuiEvents.OpenSettingsDialog, lambda: open_settings_dialog(main_window))


def main():
    main_window.mainloop()


if __name__ == '__main__':
    main()


