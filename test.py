import argparse
from tests.test_files_exist import TestInfoTable


parser = argparse.ArgumentParser(description="Hedge Learner Test Parser")
parser.add_argument("-v", "--verbose", action="store_true", default=False)

def test():
    global args
    args = parser.parse_args()
    TestInfoTable(verbose=args.verbose).run()


if __name__ == "__main__":
    test()