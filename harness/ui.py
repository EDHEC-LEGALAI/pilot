"""ui.py - printing to the screen, so you can watch the agent work.

Nothing clever happens in this file. It exists so the interesting files
(loop.py, tools.py, memory.py) stay short and readable.
"""

import os
import shutil
import sys

USE_COLOUR = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None

DIM = "\033[2m" if USE_COLOUR else ""
BOLD = "\033[1m" if USE_COLOUR else ""
BLUE = "\033[34m" if USE_COLOUR else ""
GREEN = "\033[32m" if USE_COLOUR else ""
YELLOW = "\033[33m" if USE_COLOUR else ""
RED = "\033[31m" if USE_COLOUR else ""
OFF = "\033[0m" if USE_COLOUR else ""


def width():
    return min(shutil.get_terminal_size((80, 24)).columns, 92)


def banner(title):
    line = "=" * width()
    print("\n%s%s\n %s\n%s%s" % (BOLD + BLUE, line, title, line, OFF))


def rule(label):
    label = " %s " % label
    padding = max(0, width() - len(label) - 3)
    print("\n%s---%s%s%s" % (BOLD, label, "-" * padding, OFF))


def field(name, value):
    print("  %s%-9s%s %s" % (DIM, name, OFF, value))


def step(text):
    print("  %s%s%s" % (DIM, text, OFF))


def action(name, text, colour=GREEN):
    """One thing the harness did because the model asked for it."""
    print("  %s-> %s%s %s" % (colour, name, OFF, text))


def warn(text):
    print("  %s! %s%s" % (YELLOW, text, OFF))


def error(text):
    print("\n%sPROBLEM%s\n   %s\n" % (BOLD + RED, OFF, text.replace("\n", "\n   ")))


def thinking(text, limit=420, full=False):
    """Show the model's reasoning, dimmed, so it is obvious it is not the answer."""
    shown = " ".join(text.split())
    if not full and len(shown) > limit:
        shown = shown[:limit].rstrip() + " ... (rest in the transcript)"
    label = "thinking:"
    for line in _wrap(shown, width() - 4):
        print("  %s%s %s%s" % (DIM, label, line, OFF))
        label = " " * len(label)


def _wrap(text, columns):
    import textwrap

    return textwrap.wrap(text, max(30, columns - 10)) or [""]


def quote(text, limit=1400):
    """Show what the model said, indented, so it is obvious it is not us."""
    shown = text.strip()
    if len(shown) > limit:
        shown = shown[:limit].rstrip() + "\n[... rest of the reply is in the transcript file ...]"
    for line in shown.splitlines() or [""]:
        print("  %s|%s %s" % (DIM, OFF, line))
