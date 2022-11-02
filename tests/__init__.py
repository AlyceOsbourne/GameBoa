import unittest

suite = unittest.TestLoader()
runner = unittest.TextTestRunner(verbosity=2, descriptions=True, failfast=False)


def run():
    runner.run(suite.discover("tests"))
