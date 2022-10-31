from pathlib import Path
from argparse import ArgumentParser

import __metadata__


__all__ = ["main", "__metadata__"]

PARENT_PATH = Path(__file__).parent

DIST_PATH = PARENT_PATH / "dist"
BUILD_PATH = PARENT_PATH / "build"
WINDOWS_DIST_PATH = DIST_PATH / "windows"
SPEC_PATH = PARENT_PATH / f"{__metadata__.__app_name__}.spec"
EXE_PATH = WINDOWS_DIST_PATH / f"{__metadata__.__app_name__} Build [{__metadata__.__app_version__}].exe"


argument_parser = ArgumentParser()
argument_parser.add_argument("--build", action="store_true")
argument_parser.add_argument("--test-build", action="store_true")
argument_parser.add_argument("--reset-build", action="store_true")
argument_parser.add_argument("--run-unit-tests", action="store_true")
arguments = argument_parser.parse_args()


def _sweep(to_sweep: Path):
    if not to_sweep.exists():
        return


    if to_sweep.is_dir():
        for item in to_sweep.iterdir():

            if item.is_dir():
                _sweep(item)
            else:
                item.unlink()

        to_sweep.rmdir()
    else:
        to_sweep.unlink()


def _cleanup_build():
    _sweep(BUILD_PATH)
    _sweep(SPEC_PATH)



def _cleanup_all():
    _cleanup_build()

    if EXE_PATH.exists():
        EXE_PATH.unlink()


def _build():
    from build_tools import build

    _sweep(DIST_PATH)
    build(EXE_PATH.name)
    _cleanup_build()


def _test_build():
    from subprocess import call

    if not EXE_PATH.exists() or arguments.reset_build:
        _build()

    call(str(EXE_PATH), shell=True)


def _run_src():
    from project import run
    run()


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
        _sweep(PARENT_PATH / ".hypothesis")
    else:
        _run_src()


if __name__ == "__main__":
    main()
