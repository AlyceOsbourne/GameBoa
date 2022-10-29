import unittest
from memory import TestMemory
from register import TestRegister

def suite():
    _suite = unittest.TestSuite()
    _suite.addTest(unittest.makeSuite(TestMemory))
    _suite.addTest(unittest.makeSuite(TestRegister))
    return _suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
