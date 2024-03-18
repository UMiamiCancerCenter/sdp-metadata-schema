#!/usr/bin/env python

"""
Schema Example

Usage:
  jss example
  jss dynamic
  jss language
  jss randtree
  jss -h | --help

Options:
  -h --help     Show this screen.
"""

import example
import language
import dynamic
import randtree

from docopt import docopt


def main():
    """ call docopt and do what it says """
    opt = docopt(__doc__)
    if opt["example"]:
        example.example()
        return 0
    if opt["dynamic"]:
        dynamic.example()
        return 0
    if opt["language"]:
        language.example()
        return 0
    if opt["randtree"]:
        randtree.example()
        return 0
    print("unknown options", opt)
    return 0




if __name__ == "__main__":
    main()
