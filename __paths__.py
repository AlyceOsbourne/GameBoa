import pathlib

root = pathlib.Path(__file__).parent

local_path = root / 'local'
local_path.mkdir(exist_ok=True)

config_folder_path = local_path / "config"
config_folder_path.mkdir(exist_ok=True)
config_path = config_folder_path / "gameboa.config"

project_folder = root / "project"
resources = project_folder / "resources"
resources_gui = resources / "gui"
resources_gui_icons = resources_gui / "icons"
ico_path = resources_gui_icons / "icon.ico"

src_path = project_folder / "src"
run_path = project_folder / "run.py"

build_path = root / "build_tools"

spec_path = build_path / 'tmp' / 'spec'
work_path = build_path / 'tmp' / 'work'
dist_path = build_path / 'dist'



if __name__ == "__main__":
    print(root)
    print(resources)
    print(resources_gui)
    print(resources_gui_icons)
    print(ico_path)
    print(src_path)
    print(run_path)