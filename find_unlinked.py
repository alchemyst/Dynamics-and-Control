#!/usr/bin/env python3

import re
import nbformat
import urllib
import pathlib

linkre = re.compile(r'\* \[.*\]\((.*)\)')

toc = nbformat.read('TOC.ipynb', as_version=4)

linkedfiles = set()

for cell in toc.cells:
    if cell.cell_type != 'markdown':
        continue
    links = linkre.findall(cell.source)
    for link in links:
        link = urllib.parse.unquote(link)
        if not pathlib.Path(link).exists():
            print(f"Linked file '{link}' doesn't exist")
        linkedfiles.add(link)

for f in pathlib.Path('.').glob('**/*.ipynb'):
    if 'ipynb_checkpoints' in str(f):
        continue
    if str(f) not in linkedfiles:
        print(f"File '{str(f)}' not linked in TOC")

