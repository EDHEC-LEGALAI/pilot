"""memory.py - the agent's notebook.

The model forgets everything the moment a run ends. So we give it a
notebook: a plain text file called memory.yaml that sits in this folder.

    - Before each loop we SHOW the agent what is in the notebook.
    - When the agent calls the remember tool, we ADD a line to it.

That is the whole idea of agent memory. It is a file.

The file looks like this:

    problem: 1-dispute
    updated: "2026-09-12 14:32"
    notes:
      - "FACT: the agreement is governed by French law (clause 21.1)"
      - "ISSUE: is the liability cap enforceable?"

YAML is a format for writing simple data as readable text. We only use
the small part of it shown above, so we can read and write it here in a
few lines rather than installing anything.
"""

import datetime
import os

MEMORY_FILE = "memory.yaml"


def _unquote(text):
    text = text.strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in ("'", '"'):
        text = text[1:-1]
    return text.replace('\\"', '"').replace("\\\\", "\\")


def _quote(text):
    text = " ".join(str(text).split())  # collapse newlines/tabs to single spaces
    text = text.replace("\\", "\\\\").replace('"', '\\"')
    return '"' + text + '"'


def load(path=MEMORY_FILE):
    """Read memory.yaml. Returns {'problem': ..., 'updated': ..., 'notes': [...]}."""
    memory = {"problem": None, "updated": None, "notes": []}
    if not os.path.exists(path):
        return memory

    reading_notes = False
    with open(path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.rstrip("\n")
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            if reading_notes and line.startswith(("  - ", "- ")):
                memory["notes"].append(_unquote(line.split("- ", 1)[1]))
                continue
            if not line.startswith(" ") and ":" in line:
                key, _, value = line.partition(":")
                key = key.strip()
                reading_notes = key == "notes"
                if not reading_notes:
                    memory[key] = _unquote(value) or None
    return memory


def save(memory, path=MEMORY_FILE):
    """Write memory.yaml back out."""
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "# The agent's memory. Written by the harness, readable by you.",
        "# Delete this file (or run with --fresh) to give the agent amnesia.",
        "problem: %s" % (memory.get("problem") or "none"),
        'updated: "%s"' % stamp,
        "notes:",
    ]
    for note in memory.get("notes", []):
        lines.append("  - " + _quote(note))
    if not memory.get("notes"):
        lines.append("  # (empty - the agent has not written anything down yet)")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def add(memory, note):
    """Add one note, ignoring blanks and exact duplicates."""
    note = " ".join(str(note).split())
    if not note or note in memory["notes"]:
        return False
    memory["notes"].append(note)
    return True


def for_prompt(memory):
    """Format the notebook for showing to the model."""
    if not memory["notes"]:
        return "(your notebook is empty - you have not written anything down yet)"
    return "\n".join("%d. %s" % (i, n) for i, n in enumerate(memory["notes"], 1))


def start(problem_name, fresh=False, path=MEMORY_FILE):
    """Load memory for this problem, clearing it if it belongs to a different one."""
    memory = load(path)
    switched = memory["problem"] not in (None, problem_name)
    if fresh or switched:
        memory = {"problem": problem_name, "updated": None, "notes": []}
    memory["problem"] = problem_name
    return memory, switched
