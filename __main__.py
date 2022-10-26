import argparse
from build_tools import build
import pathlib
from subprocess import call

argparser = argparse.ArgumentParser()

argparser.add_argument('--build', action='store_true')
argparser.add_argument('--test-build', action='store_true')
args = argparser.parse_args()

if args.build:
    print('Building...')
    build()

elif args.test_build:
    path = pathlib.Path(__file__).parent / 'build_tools' / 'dist' / 'GameBoa.exe'
    print(f'Testing build at {path}')
    if not path.exists():
        print('Building...')
        build()

    call(str(path), shell=True)

else:
    from project.run import main
    print('Running...')
    main()
