# Dynamics and Control notebooks

The `tbcontrol` package collects functions useful for the kinds of problems encountered in undergraduate process control
textbooks. It is the distributable part of this larger collection of Jupyter notebooks for CPN321 (Process Dynamics) and
CPB421 (Process Control) at the University of Pretoria.

There is also a [Dynamics and Control YouTube channel](https://www.youtube.com/channel/UCOf3CPrYPMG4BrgkVPupPqA) with
videos related to the notebooks.

## Environment setup

The supported notebook environment is managed by [uv](https://docs.astral.sh/uv/) and pinned to Python 3.13 through
`.python-version`. The published `tbcontrol` library is intentionally less restrictive: it supports Python 3.10 and newer,
has no upper bounds on its runtime dependencies, and is tested separately across Python 3.10–3.14.

On macOS, install uv with Homebrew:

```shell
brew install uv
```

Other platforms can use the [official uv installation instructions](https://docs.astral.sh/uv/getting-started/installation/).

A plain sync installs the ordinary notebook environment:

```shell
uv sync
uv run jupyter lab
```

The neural-network notebook and the test tools are kept in focused groups. Install them when running the complete test
suite:

```shell
uv sync --group ml-ai --group test --group notebook-test
uv run --group ml-ai --group test pytest tests
uv run --group ml-ai --group test --group notebook-test pytest -n 2 --verbose test_all_notebooks.py
```

The dependency groups are:

- `default`: Jupyter and the constrained numerical, symbolic, control, spreadsheet, plotting, and notebook-diff packages
  used by this repository.
- `ml-ai`: TensorFlow and Keras for `1_Dynamics/7_System_identification/Neural networks.ipynb`.
- `test`: the lightweight `tbcontrol` package-test dependency.
- `notebook-test`: notebook execution and parallel-test tooling.
- `docs`: Sphinx and the documentation extensions used by Read the Docs.

To build the documentation locally:

```shell
uv sync --group docs
uv run --group docs sphinx-build -M html . _build
```

### Direnv

The repository's `.envrc` uses `layout uv`. Install direnv, add its shell hook, and install the
[uv layout from the direnv wiki](https://github.com/direnv/direnv/wiki/Python#uv), then run:

```shell
direnv allow
```

Configure editors and notebook clients to use `.venv/bin/python`.

## Notebook and documentation links

- [Notebook table of contents](https://nbviewer.org/github/alchemyst/Dynamics-and-Control/blob/master/TOC.ipynb)
- [Repository on GitHub](https://github.com/alchemyst/Dynamics-and-Control)
- [Published documentation](https://dynamics-and-control.readthedocs.io/)

[![Tests](https://github.com/alchemyst/Dynamics-and-Control/actions/workflows/test.yml/badge.svg)](https://github.com/alchemyst/Dynamics-and-Control/actions/workflows/test.yml)
[![Documentation Status](https://readthedocs.org/projects/dynamics-and-control/badge/?version=latest)](https://dynamics-and-control.readthedocs.io/en/latest/?badge=latest)
