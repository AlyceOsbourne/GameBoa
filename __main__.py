import argparse
from build_tools import build
import pathlib
from subprocess import call
argparser = argparse.ArgumentParser()

argparser.add_argument('--build', action='store_true')
argparser.add_argument('--test-build', action='store_true')
args = argparser.parse_args()

def _build():
    print('Building...')
    build()
    sweep = pathlib.Path(__file__).parent / 'build'
    for file in sweep.iterdir():
        file.unlink()
    sweep.rmdir()
    print('Done.')


if args.build:
    _build()

elif args.test_build:
    test_build_path = pathlib.Path(__file__).parent / 'dist' / 'GameBoa.exe'
    print(f'Testing build at {test_build_path}')
    if not test_build_path.exists():
        _build()
    call(str(test_build_path), shell=True)

else:
    from project.run import main
    print('Running...')
    main()
