import argparse

argparser = argparse.ArgumentParser()

argparser.add_argument('--build', action='store_true')
args = argparser.parse_args()

if args.build:
    from build_tools import build
    print('Building...')
    build()

else:
    from project.run import main
    print('Running...')
    main()
