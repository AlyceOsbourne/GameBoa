from pathlib import Path

import PyInstaller.__main__ as installer


WINDOWS_PATH = Path(__file__).parent.parent / "dist" / "windows"
ICON_PATH = (
    Path(__file__).parent.parent
    / "project"
    / "resources"
    / "gui"
    / "icons"
    / "icon.ico"
)


def build(exe_name):
    installer.run(
        [
            "__main__.py",
            "--clean",
            "--onefile",
            f"--name={exe_name}",
            f"--icon={ICON_PATH}",
            f"--distpath={WINDOWS_PATH}",
            "--add-data=project/resources;resources",
        ]
    )



