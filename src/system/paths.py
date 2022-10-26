import pathlib

root = pathlib.Path(__file__).parent.parent.parent
resources = root / "resources"
resources_gui = resources / "gui"
resources_gui_icons = resources_gui / "icons"
ico_path = resources_gui_icons / "icon.png"
