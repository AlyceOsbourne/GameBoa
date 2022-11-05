import unittest

suite = unittest.TestLoader()
runner = unittest.TextTestRunner(verbosity=5, descriptions=True, failfast=False)


def run():
    results = suite.discover("tests").run(unittest.TestResult())
    for test, err in results.errors:
        print(f"Error: {test} {err}")
    for test, err in results.failures:
        print(f"Failure: {test} {err}")
    for test, err in results.skipped:
        print(f"Skipped: {test} {err}")
    for test, err in results.expectedFailures:
        print(f"Expected Failure: {test} {err}")
    for test, err in results.unexpectedSuccesses:
        print(f"Unexpected Success: {test} {err}")
    if results.wasSuccessful():
        print("All tests passed")
