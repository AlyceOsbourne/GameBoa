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


def build():
    installer.run(
        [
            "__main__.py",
            "--clean",
            "--onefile",
            "--name=GameBoa",
            f"--icon={ICON_PATH}",
            f"--distpath={WINDOWS_PATH}",
            "--add-data=project/resources;resources",
        ]
    )


if __name__ == "__main__":
    build()
