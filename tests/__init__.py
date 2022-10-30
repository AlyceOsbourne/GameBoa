import unittest

suite = unittest.TestLoader()
runner = unittest.TextTestRunner(
    verbosity=2
)

def run():
    runner.run(suite.discover('tests'))

