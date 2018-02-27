import unittest
from readablecode.checker import Checker

class MyTestCase(unittest.TestCase):
    def test_something(self):
        checker = Checker('/tests/testData/test1.cpp', None, None)
        self.assertEqual(True, False)

if __name__ == '__main__':
    unittest.main()