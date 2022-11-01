from pathlib import Path

import PyInstaller.__main__ as installer

ROOT = Path(__file__).parent.parent

WINDOWS_PATH = ROOT / "dist" / "windows"
ICON_PATH = (
    ROOT
    / "project"
    / "resources"
    / "gui"
    / "icons"
    / "icon.ico"
)
RUN_PATH = ROOT / "project" / "__init__.py"

def build(exe_name):
    installer.run(
        [
            # script file to be converted to executable
            f"{RUN_PATH.relative_to(ROOT)}",
            "--clean",
            "--onefile",
            f"--name={exe_name}",
            f"--icon={ICON_PATH}",
            f"--distpath={WINDOWS_PATH}",
            "--add-data=project/resources;resources",
        ]
    )



