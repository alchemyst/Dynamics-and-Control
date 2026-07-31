#!/usr/bin/env python3
"""Git clean filter: normalise notebook metadata on the way into the index.

Reads a notebook on stdin and writes the normalised form to stdout. Git runs
this when staging, so the working tree is never modified - editors and Jupyter
clients can keep writing whatever metadata they like without it reaching a
commit.

Cell outputs are deliberately left untouched. This repository publishes its
stored output through nbviewer and Read the Docs, which is why the usual
nbstripout setup is not appropriate here.

At notebook level:

  * ``anaconda-cloud`` - vestigial, left behind by old Anaconda Jupyter
  * ``widgets`` - ipywidgets state keyed by random UUIDs, so it re-churns on
    every execution while carrying no rendered image
  * ``kernelspec.display_name`` - editors stamp their own kernel labels here

At cell level:

  * ``execution`` - wall-clock timestamps recorded by ipykernel, which differ on
    every run. Deliberate authoring choices such as ``collapsed``, ``scrolled``
    and ``slideshow`` are left alone.

Enable it with::

    git config filter.nbclean.clean "python3 tools/nbclean.py"
    git config filter.nbclean.required true

The ``.gitattributes`` entry is committed, but the filter definition above
lives in ``.git/config`` and is *not* cloned - it has to be run once per
checkout, or the filter silently does nothing.
"""

import json
import sys

STRIP_KEYS = ("anaconda-cloud", "widgets")
STRIP_CELL_KEYS = ("execution",)
DISPLAY_NAME = "Python 3"


def clean(raw):
    """Return the normalised notebook bytes, or the input unchanged."""
    try:
        notebook = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        # Store it untouched rather than risk mangling something we do not
        # understand. Git shows this on stderr.
        print(f"nbclean: passing through unparsed notebook ({exc})", file=sys.stderr)
        return raw

    metadata = notebook.get("metadata", {})
    for key in STRIP_KEYS:
        metadata.pop(key, None)
    kernelspec = metadata.get("kernelspec")
    if kernelspec:
        kernelspec["display_name"] = DISPLAY_NAME

    for cell in notebook.get("cells", []):
        cell_metadata = cell.get("metadata", {})
        for key in STRIP_CELL_KEYS:
            cell_metadata.pop(key, None)

    text = json.dumps(notebook, indent=1, sort_keys=True, ensure_ascii=False) + "\n"
    return text.encode("utf-8")


if __name__ == "__main__":
    sys.stdout.buffer.write(clean(sys.stdin.buffer.read()))
