"""Sphinx build configuration.

Sphinx has no pyproject.toml equivalent - it requires this file - but the
version is read from tbcontrol/version.py rather than repeated here, so there
is still only one place to change it. That file is the same source hatchling
builds the package version from, and is written to be exec'ed.
"""

import datetime
import pathlib

HERE = pathlib.Path(__file__).parent

extensions = [
    "myst_parser",
    "nbsphinx",
    "sphinx.ext.mathjax",
]

# Notebooks are committed with their output, and nbviewer and this site both
# serve those stored results, so Sphinx must not re-run them.
nbsphinx_execute = "never"
nbsphinx_allow_errors = True
nbsphinx_timeout = 1000

templates_path = ["_templates"]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

root_doc = "index"

project = "Dynamics and Control with Jupyter Notebooks"
author = "Carl Sandrock"
copyright = f"2018-{datetime.date.today():%Y}, {author}"

_version_namespace = {}
exec((HERE / "tbcontrol" / "version.py").read_text(), _version_namespace)
release = _version_namespace["__version__"]
version = ".".join(release.split(".")[:2])

language = "en"

exclude_patterns = [
    ".direnv",
    ".direnv/**",
    ".venv",
    ".venv/**",
    "_build",
    "**.ipynb_checkpoints",
    "Thumbs.db",
    ".DS_Store",
    # Work in progress, deliberately not part of the published site.
    "under_construction",
    "under_construction/**",
    # Repository front matter rather than course material, and nothing in the
    # documentation links to it. TOC.ipynb and Function index.ipynb are also
    # outside the toctree, but they link to each other, so those are marked
    # orphan in their own metadata instead of being excluded here.
    "README.md",
]

html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "collapse_navigation": False,
    # Part, chapter, notebook. The theme passes this as the sidebar toctree's
    # maxdepth, overriding the directive, so it is what keeps the headings
    # inside each notebook out of the navigation.
    "navigation_depth": 3,
}
html_static_path = []

htmlhelp_basename = "DynamicsControl"

latex_engine = "xelatex"
latex_documents = [
    (root_doc, "DynamicsControl.tex", "Dynamics and Control", author, "manual"),
]
