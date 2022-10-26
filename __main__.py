import argparse
import pathlib
argparser = argparse.ArgumentParser()
argparser.add_argument('--build', action='store_true')
argparser.add_argument('--test-build', action='store_true')
argparser.add_argument('--reset-build', action='store_true')
argparser.add_argument('--sweep', action='store_true')
args = argparser.parse_args()

def _sweep(directory: pathlib.Path):
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
    _sweep(pathlib.Path(__file__).parent / 'build')
    spec = pathlib.Path(__file__).parent / 'Gameboa.spec'
    if spec.exists():
        spec.unlink()

def _cleanup_all():
    _cleanup_build()
    _sweep(pathlib.Path(__file__).parent / 'dist')

def _build():
    from build_tools import build
    _sweep(pathlib.Path(__file__).parent / 'dist')
    print('Building...')
    build()
    _cleanup_build()
    print('Done.')

if args.build:
    _build()

elif args.test_build:
    from subprocess import call
    test_build_path = pathlib.Path(__file__).parent / 'dist' / 'GameBoa.exe'
    print(f'Testing build at {test_build_path}')
    if not test_build_path.exists() or args.reset_build:
        _build()
    print('Running...')
    call(str(test_build_path), shell=True)

elif args.sweep:
    print('Sweeping...')
    _cleanup_all()

else:
    from project.run import main
    print('Running...')
    main()
