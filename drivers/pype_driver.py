#!/usr/bin/env python3

import sys
import pype

if __name__ == '__main__':
    for fname in sys.argv[1:]:
        pype.Pipeline(source=fname)
