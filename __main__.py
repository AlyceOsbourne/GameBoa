from pathlib import Path
from argparse import ArgumentParser

import __metadata__


__all__ = ["main", "__metadata__"]

WRITE_PERMISSION = 0o777
PARENT_PATH = Path(__file__).parent

DIST_PATH = PARENT_PATH / "dist"
BUILD_PATH = PARENT_PATH / "build"
WINDOWS_DIST_PATH = DIST_PATH / "windows"
SPEC_PATH = PARENT_PATH / f"{__metadata__.__app_name__}.spec"
EXE_PATH = WINDOWS_DIST_PATH / f"{__metadata__.__app_name__}.exe"


argument_parser = ArgumentParser()
argument_parser.add_argument("--build", action="store_true")
argument_parser.add_argument("--test-build", action="store_true")
argument_parser.add_argument("--reset-build", action="store_true")
argument_parser.add_argument("--run-unit-tests", action="store_true")
arguments = argument_parser.parse_args()


def _sweep(directory: Path):
    if not directory.exists():
        return

    directory.chmod(WRITE_PERMISSION)

    for item in directory.iterdir():
        item.chmod(WRITE_PERMISSION)

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

    if not EXE_PATH.exists() or arguments.reset_build:
        _build()

    call(str(EXE_PATH), shell=True)


def _run_src():
    from project import MainWindow

    main_window = MainWindow()
    main_window.mainloop()


def _run_unit_tests():
    from tests import run

    run()


def main():
    if arguments.build:
        _build()
    elif arguments.test_build:
        _test_build()
    elif arguments.run_unit_tests:
        _run_unit_tests()
    else:
        _run_src()


if __name__ == "__main__":
    main()
