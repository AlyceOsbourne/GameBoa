import os
import pathlib
import sys

try:
    root = pathlib.Path(sys._MEIPASS).parent
    user_dir = pathlib.Path.home() / "GameBoa"
    user_dir.mkdir(exist_ok=True)
    print("Running from PyInstaller at:", root)

except Exception:
    root = pathlib.Path(__file__).parent
    user_dir = root

local_path = user_dir / 'local'
local_path.mkdir(exist_ok=True)

config_folder_path = local_path / "config"
config_folder_path.mkdir(exist_ok=True)

config_path = config_folder_path / "gameboa.config"

project_folder = root / "project"

resources = project_folder / "resources"

op_code_path = resources / "ops.bin"

resources_gui = resources / "gui"
resources_gui_icons = resources_gui / "icons"

ico_path = resources_gui_icons / "icon.ico"

src_path = project_folder / "src"
run_path = project_folder / "run.py"

build_path = root / "build_tools"
spec_path = build_path / 'tmp' / 'spec'
work_path = build_path / 'tmp' / 'work'
dist_path = build_path / 'dist'
test_build_path = dist_path / 'GameBoa.exe'


if __name__ == "__main__":
    for path in [
        root,
        local_path,
        config_folder_path,
        config_path,
        project_folder,
        resources,
        resources_gui,
        resources_gui_icons,
        ico_path,
        src_path,
        run_path,
        build_path,
        spec_path,
        work_path,
        dist_path,
    ]:
        print(path)
        print(path.exists())
        print()

