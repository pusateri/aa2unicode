#!/usr/bin/env python

import getopt
import sys
from copy import deepcopy

help = """Module docstring.

Convert lineart from ASCII to other formats.
lineart [-h | --help]
lineart <input file>

"""

def print_chars(chars):
    for l in range(len(chars)):
        for c in chars[l]:
            print(c, end="")
        print("")


def above_char(l, c, chars):
    if l == 0:
        return None
    maxc = len(chars[l-1])
    if c > maxc - 1:
        return None
    return chars[l-1][c]


def below_char(l, c, chars):
    maxl = len(chars)
    if l == maxl - 1:
        return None
    maxc = len(chars[l+1])
    if c > maxc - 1:
        return None
    return chars[l+1][c]


def previous_char(l, c, chars):
    return chars[l][c-1]


def next_char(l, c, chars):
    maxc = len(chars[l])
    if c == maxc - 1:
        return None
    return chars[l][c+1]


def transform(l, c, old, new):
    """Replace select characters in new matrix based on surrounding characters"""
    if old[l][c] == ' ':
        return
    elif old[l][c] == '+':
        # left edge
        p = previous_char(l, c, old)
        n = next_char(l, c, old)
        b = below_char(l, c, old)
        a = above_char(l, c, old)
        # leading edge
        if (p == ' ' or p == None) and n == '-':
            if a == ' ' and b == '|':
                new[l][c] = '┌'
            elif a == '|' and b == '|':
                new[l][c] = '├'
            elif a == '|' and (b == ' ' or b == None):
                new[l][c] = '└'
        # interior
        elif p == '-' and n == '-':
            if a != '|' and b != '|':
                new[l][c] = '─'
            if a != '|' and b == '|':
                new[l][c] = '┬'
            if a == '|' and b != '|':
                new[l][c] = '┴'
            if a == '|' and b == '|':
                new[l][c] = '┼'
        # trailing edge
        elif p == '-' and (n == ' ' or n == None):
            if (a == ' ' or a == None) and b == '|':
                new[l][c] = '┐'
            if a == '|' and b == '|':
                new[l][c] = '┤'
            if a == '|' and (b == ' ' or b == None):
                new[l][c] = '┘'
    elif old[l][c] == '-':
        new[l][c] = '─'
    elif old[l][c] == '|':
        new[l][c] = '│'


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

    for arg in args:
        with open(arg) as file:
            lines = [line.rstrip() for line in file]

            chars = [list(line) for line in lines]

            out = deepcopy(chars)

            for l in range(len(chars)):
                for c in range(len(chars[l])):
                    transform(l, c, chars, out) 

            print_chars(out)

if __name__ == "__main__":
    main()
