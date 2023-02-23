#!/usr/bin/env python

import getopt
import sys
import fileinput
from copy import deepcopy

help = """Module docstring.

Convert artwork from ASCII to Unicode box characters
aa2unicode [-h | --help]
aa2unicode [<input file> <input file> ...]

"""


def print_chars(chars):
    for achar in range(len(chars)):
        for c in chars[achar]:
            print(c, end="")
        print("")


def above_char(line, c, chars):
    if line == 0:
        return None
    maxc = len(chars[line-1])
    if c > maxc - 1:
        return None
    return chars[line-1][c]


def below_char(line, c, chars):
    maxl = len(chars)
    if line == maxl - 1:
        return None
    maxc = len(chars[line+1])
    if c > maxc - 1:
        return None
    return chars[line+1][c]


def previous_char(line, c, chars):
    if c == 0:
        return None
    return chars[line][c-1]


def next_char(line, c, chars):
    maxc = len(chars[line])
    if c == maxc - 1:
        return None
    return chars[line][c+1]


def transform(line, c, old, new):
    """Replace select characters in new matrix based on surrounding characters"""
    if old[line][c] == ' ':
        return
    elif old[line][c] == '+':
        # left edge
        p = previous_char(line, c, old)
        n = next_char(line, c, old)
        b = below_char(line, c, old)
        a = above_char(line, c, old)
        # leading edge
        if (p == ' ' or p is None) and (n == '-' or n == '+' or n == ' '):
            if (a == ' ' or a is None or a == '.') and b == '|':
                new[line][c] = '┌'
            elif a == '|' and b == '|':
                new[line][c] = '├'
            elif a == '|' and (b == ' ' or b is None or b == '.'):
                new[line][c] = '└'
            elif b == '|':
                new[line][c] = '┌'

        # interior
        elif (p == '-' or p == '+') and (n == '-' or n == '+'):
            if a != '|' and b != '|':
                new[line][c] = '─'
            if a != '|' and b == '|':
                new[line][c] = '┬'
            if a == '|' and b != '|':
                new[line][c] = '┴'
            if a == '|' and b == '|':
                new[line][c] = '┼'
        # trailing edge
        elif (p == '-' or p == ' ') and (n == ' ' or n is None):
            if (a == ' ' or a is None or a == '.') and b == '|':
                new[line][c] = '┐'
            if a == '|' and b == '|':
                new[line][c] = '┤'
            if a == '|' and (b == ' ' or b is None or b == '.'):
                new[line][c] = '┘'
    elif old[line][c] == '-':
        new[line][c] = '─'
    elif old[line][c] == '|':
        new[line][c] = '│'


def main():
    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.error as msg:
        print(msg)
        print("for help use --help")
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print(help)
            sys.exit(0)

    lines = [line.rstrip() for line in fileinput.input(encoding="utf-8")]

    chars = [list(line) for line in lines]

    out = deepcopy(chars)

    for achar in range(len(chars)):
        for c in range(len(chars[achar])):
            transform(achar, c, chars, out)

    print_chars(out)


if __name__ == "__main__":
    main()
