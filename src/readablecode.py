import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-T', '--text', help='Output the result to text file.', action='store', default=None)
    parser.add_argument('-E', '--excel', help='Output the result to excel file.', action='store', default=None)