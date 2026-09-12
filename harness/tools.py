"""tools.py - the three things the agent is allowed to DO.

A model can only produce text. So how does an "AI agent" open a file or save
a note? Like this:

    1. We send the model a list of tools it may ask for, with the arguments
       each one takes. That list is TOOLS, below.
    2. The model replies "I want to call read_document with filename =
       agreement-extract.md".
    3. WE open the file. WE paste the contents into the next message.

The model never touches anything. It asks, in a structured way, and the
harness does the work. That is all a tool is, and every AI agent that can
search the web or send an email or query a database works exactly this way.

Our agent has three tools. That is the whole toolbox.
"""

import os

MAX_DOCUMENT_CHARS = 12000

# This is the menu we hand to the model on every turn. The wording of each
# description matters: it is the only thing the model knows about the tool.
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_document",
            "description": (
                "Open one document from this matter's file and read it. "
                "You can call this several times in one turn to open several documents."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The exact filename, as listed in the matter file.",
                    }
                },
                "required": ["filename"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "remember",
            "description": (
                "Write one short line into your notebook. The notebook is a file that "
                "survives after this run ends, and is shown back to you every turn. "
                "Use it for anything you will still need later. One point per call."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "note": {
                        "type": "string",
                        "description": "A single short line. Not a paragraph.",
                    }
                },
                "required": ["note"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "done",
            "description": (
                "Stop gathering information. Call this when you have read enough and are "
                "ready to write the final work product."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "reason": {
                        "type": "string",
                        "description": "One sentence on why you have enough.",
                    }
                },
                "required": ["reason"],
            },
        },
    },
]


def list_documents(documents_dir):
    """Every file in this matter's documents folder."""
    if not os.path.isdir(documents_dir):
        return []
    return sorted(f for f in os.listdir(documents_dir) if not f.startswith("."))


def _match_filename(asked_for, available):
    """Be forgiving about how the model spells the filename."""
    asked_for = (asked_for or "").strip().strip("`'\"")
    asked_for = asked_for.replace("\\", "/").split("/")[-1]  # drop any folder prefix
    for name in available:
        if name.lower() == asked_for.lower():
            return name
    for name in available:
        if os.path.splitext(name)[0].lower() == os.path.splitext(asked_for)[0].lower():
            return name
    return None


def read_document(documents_dir, asked_for):
    """Open a document from this matter's folder. Returns (name, text, found)."""
    available = list_documents(documents_dir)
    name = _match_filename(asked_for, available)

    if name is None:
        # The model got the name wrong. Tell it so, and tell it the real names.
        # Handling the model's mistakes is most of what a harness does.
        return (
            asked_for or "(no filename given)",
            "There is no document called '%s' in this matter. The documents available "
            "are: %s" % (asked_for, ", ".join(available) or "none"),
            False,
        )

    with open(os.path.join(documents_dir, name), "r", encoding="utf-8") as f:
        text = f.read()
    if len(text) > MAX_DOCUMENT_CHARS:
        text = text[:MAX_DOCUMENT_CHARS] + "\n\n[... document truncated by the harness ...]"
    return name, "--- DOCUMENT: %s ---\n%s" % (name, text), True
