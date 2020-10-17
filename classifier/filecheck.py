import sys
import os


def filechecker():
    file = sys.argv[1]
    if os.path.isfile(file):
        print(file, "is valid!")
    else:
        print(file, "is invalid!")


if __name__ == '__main__':
    filechecker()
