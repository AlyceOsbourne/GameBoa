import argparse
from build_tools import build
import pathlib
from subprocess import call
from __paths__ import test_build_path
argparser = argparse.ArgumentParser()

argparser.add_argument('--build', action='store_true')
argparser.add_argument('--test-build', action='store_true')
args = argparser.parse_args()

if args.build:
    print('Building...')
    build()

elif args.test_build:
    print(f'Testing build at {test_build_path}')
    if not test_build_path.exists():
        print('Building...')
        build()

    call(str(test_build_path), shell=True)

else:
    from project.run import main
    print('Running...')
    main()
