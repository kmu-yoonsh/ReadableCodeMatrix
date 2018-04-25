import os
import sys
import unittest

class MyTestCase(unittest.TestCase):
    def test_basic_case(self):
        sys.path.insert(0, '../')
        from readablecode.checker import Checker

        checker1 = Checker('./tests/testData/test1.cpp', None, None)
        checker2 = Checker('./tests/testData/test2.cpp', None, None)
        checker3 = Checker('./tests/testData/test3.cpp', None, None)
        checker4 = Checker('./tests/testData/test4.cpp', None, None)
        checker5 = Checker('./tests/testData/test5.cpp', None, None)
        checker6 = Checker('./tests/testData/test6.cpp', None, None)
        checker1.check_code()
        checker2.check_code()
        checker3.check_code()
        checker4.check_code()
        checker5.check_code()
        checker6.check_code()
        result1 = checker1.check_result['test1.cpp']
        result2 = checker2.check_result['test2.cpp']['main']
        result3 = checker3.check_result['test3.cpp']['main']
        result4 = checker4.check_result['test4.cpp']
        result5 = checker5.check_result['test5.cpp']['main']
        result6 = checker6.check_result['test6.cpp']['main']

        # test 1
        self.assertEqual('print' in result1, True)
        self.assertEqual('main' in result1, True)
        self.assertEqual('add' in result1, False)

        # test 2
        self.assertEqual('temp' in result2['unsuitable_naming']['numbering'], True)
        self.assertEqual('a' in result2['unsuitable_naming']['too_short'], True)
        self.assertEqual('b' in result2['unsuitable_naming']['too_short'], True)
        self.assertEqual('v' in result2['unsuitable_naming']['too_short'], False)
        self.assertEqual(len(result2['unsuitable_naming']['too_short']), 4)
        self.assertEqual(len(result2['unused_variable']['variable']), 7)

        # test 3
        self.assertEqual(len(result3['unsuitable_naming']['numbering']), 0)
        self.assertEqual(len(result3['unsuitable_naming']['too_short']), 0)
        self.assertEqual(sum(result3['naming_rule']), 0)
        self.assertEqual(len(result3['unused_variable']['variable']), 6)

        # test 4
        self.assertEqual(len(result4['global']), 1)
        self.assertEqual('test_number' in result4['global'], True)

        # test 5
        self.assertEqual(len(result5['ternary_opt']), 1)
        self.assertEqual(result5['ternary_opt'][0], 8)

        # test 6
        self.assertEqual(len(result6['condition_combine']), 2)
        self.assertEqual(result6['condition_combine'][0], 9)
        self.assertEqual(result6['condition_combine'][1], 13)



if __name__ == '__main__':
    unittest.main()