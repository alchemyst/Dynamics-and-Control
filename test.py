#!/usr/bin/env python
import pytest
import pathlib
import fnmatch

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor, CellExecutionError

searchpath = pathlib.Path('.')
ignores = [line.strip() for line in open('.testignore') if line.strip()]
notebooks = [notebook for notebook in searchpath.glob('**/*.ipynb')
             if not (any(parent.startswith('.')
                         for parent in notebook.parent.parts)
                     or any(notebook.match(pattern)
                            for pattern in ignores))]
notebooks.sort()

@pytest.mark.parametrize("notebook", notebooks, ids=[str(n) for n in notebooks])
def test_run_notebook(notebook):
    with open(notebook) as f:
        nb = nbformat.read(f, as_version=4)
    ep = ExecutePreprocessor(timeout=600)
    ep.preprocess(nb, {'metadata': {'path': notebook.parent}})
