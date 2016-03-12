#!/usr/bin/env python3

import sys
import pype

for fname in sys.argv[1:]:
  pype.Pipeline(source=fname)
