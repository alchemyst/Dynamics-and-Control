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

Enable it with ``make setup-git``. The ``.gitattributes`` entry is committed,
but the filter definition lives in ``.git/config`` and is *not* cloned - it has
to be set up once per checkout, or the filter silently does nothing.

Git may start this filter and then decide it does not want the answer, which it
signals by closing the pipes. That shows up here as a short read on stdin, a
broken pipe on stdout, or both, and is entirely normal - during a branch switch
git runs the filter over many files and stops as soon as it knows what it
needs. Neither is worth reporting, so a result git refused to read is discarded
in silence.
"""

import json
import os
import sys

STRIP_KEYS = ("anaconda-cloud", "widgets")
STRIP_CELL_KEYS = ("execution",)
DISPLAY_NAME = "Python 3"


def clean(raw):
    """Return (normalised bytes, warning or None).

    Anything we cannot parse is passed back untouched rather than guessed at,
    so the filter can never turn a file we do not understand into a broken one.
    """
    try:
        notebook = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        return raw, f"could not parse notebook, storing it unchanged ({exc})"

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
    return text.encode("utf-8"), None


def short_read(name, raw):
    """True when stdin held less than the file it came from.

    Git hands the clean filter the entire working tree file, so a short read
    means git closed the pipe partway through and has no use for the result.
    A small result can still be written into the pipe buffer without raising,
    so this is the only reliable way to tell that case apart from a notebook
    that is genuinely malformed.
    """
    if not name:
        return False
    try:
        return len(raw) < os.path.getsize(name)
    except OSError:
        return False


def main(argv):
    # Git substitutes %f with the path being filtered, so a warning can name it.
    name = argv[1] if len(argv) > 1 else None
    raw = sys.stdin.buffer.read()
    result, warning = clean(raw)

    try:
        sys.stdout.buffer.write(result)
        sys.stdout.buffer.flush()
    except BrokenPipeError:
        # Git is not reading the result. Point the remaining buffered output at
        # devnull so the interpreter's shutdown flush cannot raise again, and
        # say nothing.
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        return 0

    if warning and not short_read(name, raw):
        print(f"nbclean: {name or '<stdin>'}: {warning}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
