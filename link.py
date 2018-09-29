#!/usr/bin/env python3


import pathlib
import urllib
import sys

for f in sys.argv[1:]:
    p = pathlib.Path(f)
    print(f"[{p.stem.replace('_', ' ')}]({urllib.parse.quote(f)})")
