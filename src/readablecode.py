import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-P', '--path', help='Check readability of the code in directory.', action='store', default=None)