import os
import unittest
from readablecode.checker import Checker

class MyTestCase(unittest.TestCase):
    def test_basic_case(self):
        print(os.getcwd())
        print(os.listdir('./tests'))
        print(os.listdir('./tests/testData'))
        checker1 = Checker('./tests/testData/test1.cpp', None, None)
        checker2 = Checker('./tests/testData/test2.cpp', None, None)
        checker3 = Checker('./tests/testData/test3.cpp', None, None)
        checker1.check_code()
        checker2.check_code()
        checker3.check_code()
        result1 = checker1.check_result['test1.cpp']
        result2 = checker2.check_result['test2.cpp']['main']
        result3 = checker3.check_result['test3.cpp']['main']

        self.assertEqual('print' in result1, True)
        self.assertEqual('main' in result1, True)
        self.assertEqual('add' in result1, False)

        self.assertEqual('temp' in result2['unsuitable_naming']['numbering'], True)
        self.assertEqual('a' in result2['unsuitable_naming']['too_short'], True)
        self.assertEqual('b' in result2['unsuitable_naming']['too_short'], True)
        self.assertEqual('v' in result2['unsuitable_naming']['too_short'], False)
        self.assertEqual(len(result2['unsuitable_naming']['too_short']), 4)
        self.assertEqual(len(result2['unused_variable']['variable']), 5)

        self.assertEqual(len(result3['unsuitable_naming']['numbering']), 0)
        self.assertEqual(len(result3['unsuitable_naming']['too_short']), 0)
        self.assertEqual(sum(result3['naming_rule']), 0)
        self.assertEqual(len(result3['unused_variable']['variable']), 6)



if __name__ == '__main__':
    unittest.main()