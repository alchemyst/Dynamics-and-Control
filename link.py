#!/usr/bin/env python3
import pathlib
import urllib

def link(f):
    p = pathlib.Path(f)
    return f"[{p.stem.replace('_', ' ')}]({urllib.parse.quote(f)})"

if __name__ == "__main__":
    import sys
    for f in sys.argv[1:]:
        print(link(f))
