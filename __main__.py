from pathlib import Path
from subprocess import call
from project.run import main
from argparse import ArgumentParser


DIST_PATH = Path(__file__).parent / "dist"
BUILD_PATH = Path(__file__).parent / "build"
EXE_PATH = Path(__file__).parent / "dist" / "windows" / "Gameboa.exe"


argument_parser = ArgumentParser()
argument_parser.add_argument("--build", action="store_true")
argument_parser.add_argument("--sweep", action="store_true")
argument_parser.add_argument("--test-build", action="store_true")
argument_parser.add_argument("--reset-build", action="store_true")
arguments = argument_parser.parse_args()


def _sweep(directory: Path):
    if not directory.exists():
        return

    directory.chmod(0o777)

    for item in directory.iterdir():
        item.chmod(0o777)

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
    print("Building...")
    build()
    _cleanup_build()
    print("Done.")


if arguments.build:
    _build()

elif arguments.test_build:
    test_build_path = str(EXE_PATH)
    print(f"Testing build at {test_build_path}")

    if not EXE_PATH.exists() or arguments.reset_build:
        _build()

    print("Running...")
    call(test_build_path, shell=True)

elif arguments.sweep:
    print("Sweeping...")
    _cleanup_all()
    print("Done.")

else:
    print("Running...")
    main()
