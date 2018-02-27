import argparse
from checker.checker import Checker

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filePath',  help='Enter the path or file want to code readable check.')
    parser.add_argument('-T', '--text', help='Output the result to text file.', action='store', default=None)
    parser.add_argument('-E', '--excel', help='Output the result to excel file.', action='store', default=None)

    args = parser.parse_args()

    checker = Checker(args.filePath, args.text, args.excel)
    checker.check_code()

