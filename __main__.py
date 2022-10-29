from argparse import ArgumentParser
from pathlib import Path
import __metadata__

NAME = 'GameBoa'

PARENT_PATH = Path(__file__).parent

DIST_PATH = PARENT_PATH / "dist"
BUILD_PATH = PARENT_PATH / "build"
SPEC_PATH = PARENT_PATH / f"{NAME}.spec"
WINDOWS_DIST_PATH = DIST_PATH / "windows"
EXE_PATH = WINDOWS_DIST_PATH / f"{NAME}.exe"


PERM = 0o777



argument_parser = ArgumentParser()
argument_parser.add_argument("--build", action="store_true")
argument_parser.add_argument("--test-build", action="store_true")
argument_parser.add_argument("--reset-build", action="store_true")
arguments = argument_parser.parse_args()


def _sweep(directory: Path):
    if not directory.exists():
        return
    directory.chmod(PERM)
    for item in directory.iterdir():
        item.chmod(PERM)
        if item.is_dir():
            _sweep(item)
        else:
            item.unlink()
    directory.rmdir()


def _cleanup_build():
    _sweep(BUILD_PATH)


def _cleanup_all():
    _cleanup_build()
    if EXE_PATH.exists():
        EXE_PATH.unlink()


def _build():
    from build_tools import build
    _sweep(DIST_PATH)
    build()
    _cleanup_build()


def _test_build():
    from subprocess import call
    test_build_path = str(EXE_PATH)
    if not EXE_PATH.exists() or arguments.reset_build:
        _build()
    call(test_build_path, shell=True)


def main():
    if arguments.build:
        _build()

    elif arguments.test_build:
        _test_build()

    else:
        _run_src()


def _run_src():
    from project import MainWindow
    main_window = MainWindow()
    main_window.mainloop()

__all__ = [
    "main", '__metadata__'
]

if __name__ == "__main__":
    main()

