"""loop.py - THE LOOP. This is the heart of the harness.

Read this file top to bottom and you know how an AI agent works.

    build a first message  ->  ask the model  ->  it asks for things
    ->  do them  ->  hand back the results  ->  ask again, up to five times
    ->  ask it one last time to write the answer

That is it. Everything else is decoration.
"""

import re
import time

from . import memory as memory_module
from . import model, tools, ui

# ---------------------------------------------------------------------
# The harness's own instructions to the model.
#
# NOTE FOR STUDENTS: read this carefully, then notice what is NOT in it.
# There is nothing here about chronologies, or limitation clauses, or how
# an advice note should be structured, or being careful with quantum.
# It explains the machinery and stops.
#
# That is deliberate. Every piece of legal judgement in this system has to
# come from skill.md - the file you write.
# ---------------------------------------------------------------------
HARNESS_RULES = """You are working inside a small software harness. You cannot click,
browse, or open anything yourself. You can only think, speak, and call the three
tools you have been given:

  read_document  - opens one document from this matter and shows it to you.
  remember       - writes one line into your notebook, which survives this run
                   and is shown back to you every turn.
  done           - stops the gathering phase so you can write the answer.

You have %(max_loops)d turns. In each turn you may call as many tools as you like,
including several read_document calls at once.

While you are gathering, keep anything you say out loud to a sentence or two.
Do not draft the answer and do not write out your analysis during these turns -
you will be asked for the final work product at the end, and that is where it
belongs. If you work something out that you must not lose, call remember.

Call done as soon as you have what you need. Unused turns are not wasted."""

FINAL_INSTRUCTION = """Stop gathering information now and write the final work product.

Base it on the documents you have read and the notes in your notebook. Output the
work product itself and nothing else - no preamble, no commentary about the
process, no description of what you did."""

# Anything a student writes between <!-- and --> in skill.md is a note to
# themselves. We strip it out so it never reaches the model.
COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)


def clean_skill(skill_text):
    """Remove the <!-- notes --> and return what the agent will actually read."""
    return COMMENT.sub("", skill_text).strip()


def build_system_prompt(skill_text, brief_text, document_names, max_loops):
    """Glue the fixed harness rules to the student's skill file and the matter.

    skill.md is dropped in whole, exactly as written. Nothing edits it,
    summarises it, or checks it. What you type is what the agent gets.
    """
    return "\n\n".join(
        [
            "## HOW THIS SYSTEM WORKS",
            HARNESS_RULES % {"max_loops": max_loops},
            "## YOUR SKILL",
            "The following is your professional instruction set for this kind of work. "
            "Follow it closely.\n\n" + clean_skill(skill_text),
            "## THE MATTER",
            brief_text.strip(),
            "## DOCUMENTS IN THIS MATTER",
            "\n".join("- " + name for name in document_names) or "(none)",
        ]
    )


def run(problem, max_loops=5, fresh=False, show_thinking=False):
    """Run the agent over one problem. Returns the final work product."""

    skill_text = _read(problem["skill_file"])
    skill_sent = clean_skill(skill_text)
    brief_text = _read(problem["brief_file"])
    document_names = tools.list_documents(problem["documents_dir"])

    mem, switched = memory_module.start(problem["name"], fresh=fresh)
    if switched:
        ui.warn("memory.yaml belonged to a different problem, so it was cleared.")

    ui.field("problem", "%s - %s" % (problem["name"], problem["title"]))
    ui.field(
        "skill",
        "%s  (%d characters, %d sent to the agent)"
        % (problem["skill_file"], len(skill_text), len(skill_sent)),
    )
    ui.field("memory", "memory.yaml (%d notes)" % len(mem["notes"]))
    ui.field("model", "%s   max turns: %d" % (model.settings()["model"], max_loops))

    messages = [
        {
            "role": "system",
            "content": build_system_prompt(skill_text, brief_text, document_names, max_loops),
        },
        {"role": "user", "content": "Begin.\n\n" + _notebook(mem)},
    ]

    transcript = []
    documents_read = []
    total_tokens = 0

    # ------------------------------ THE LOOP ------------------------------
    for turn in range(1, max_loops + 1):
        ui.rule("TURN %d of %d" % (turn, max_loops))
        ui.step("asking the model...")

        started = time.time()
        reply = model.ask(messages, tools=tools.TOOLS, max_tokens=8000)
        total_tokens += reply["tokens"]
        ui.step("replied in %.0f seconds   (%s tokens used so far)"
                % (time.time() - started, "{:,}".format(total_tokens)))

        # The model thinks before it acts, and during the loop it usually says
        # nothing out loud - so the thinking is the interesting part to watch.
        if reply["thinking"]:
            ui.thinking(reply["thinking"], full=show_thinking)
            transcript.append(("TURN %d - thinking" % turn, reply["thinking"]))
        if reply["text"]:
            ui.quote(reply["text"])
            transcript.append(("TURN %d - said" % turn, reply["text"]))
        if reply["cut_off"]:
            ui.warn("the model ran out of room mid-answer")

        # The model's own turn goes back into the conversation.
        messages.append(model.assistant_message(reply))

        if not reply["tool_calls"]:
            # Not an error - the model spent the turn thinking. Keep it moving.
            ui.step("no tools called this turn")
            messages.append({"role": "user", "content":
                "Noted. Nothing was done, because you called no tool. To open a document "
                "call read_document, to save a point call remember, and when you are ready "
                "to write call done.\n\n" + _notebook(mem)
                + "\n\nContinue. You have used %d of %d turns." % (turn, max_loops)})
            continue

        # ---- do what it asked for, and hand each result back ----
        finished = False
        for call in reply["tool_calls"]:
            name, arguments = call["name"], call["arguments"]

            if name == "read_document":
                filename, contents, found = tools.read_document(
                    problem["documents_dir"], arguments.get("filename", "")
                )
                if found:
                    ui.action("read     ", "%s  (%s characters)" % (filename, "{:,}".format(len(contents))))
                    documents_read.append(filename)
                    transcript.append(("TURN %d - harness opened %s" % (turn, filename), contents))
                else:
                    ui.action("read     ", "no such document: %s" % filename, ui.YELLOW)
                result = contents

            elif name == "remember":
                note = arguments.get("note", "")
                if memory_module.add(mem, note):
                    ui.action("remember ", '"%s"' % _shorten(note, 66))
                    result = "Saved to your notebook."
                else:
                    result = "Not saved - it was empty or already in your notebook."
                memory_module.save(mem)

            elif name == "done":
                ui.action("done     ", _shorten(arguments.get("reason", ""), 66))
                result = "Understood. You will now be asked for the final work product."
                finished = True

            else:
                ui.action("?        ", "unknown tool: %s" % name, ui.YELLOW)
                result = "There is no tool called '%s'." % name

            # Every tool call must get a reply, or the conversation is malformed.
            messages.append(model.tool_result_message(call, result))

        if finished:
            break

        # Show the notebook again before going round.
        messages.append({"role": "user", "content":
            _notebook(mem) + "\n\nContinue. You have used %d of %d turns." % (turn, max_loops)})

    # ---------------------------- THE WRITE-UP ----------------------------
    ui.rule("WRITING THE FINAL WORK PRODUCT")
    ui.step("asking the model one last time...")
    messages.append({"role": "user", "content": _notebook(mem) + "\n\n" + FINAL_INSTRUCTION})

    final = model.ask(messages, max_tokens=6000)
    total_tokens += final["tokens"]
    if final["cut_off"]:
        ui.warn("the write-up was cut short - it may end mid-sentence")
    if final["thinking"]:
        transcript.append(("FINAL - thinking", final["thinking"]))
    transcript.append(("FINAL - the work product", final["text"]))

    memory_module.save(mem)
    return {
        "answer": final["text"],
        "transcript": transcript,
        "memory": mem,
        "documents_read": documents_read,
        "skill_chars": len(skill_sent),
        "tokens": total_tokens,
    }


def _notebook(mem):
    return "--- YOUR NOTEBOOK (memory.yaml) ---\n" + memory_module.for_prompt(mem)


def _read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _shorten(text, limit):
    text = " ".join(str(text).split())
    return text if len(text) <= limit else text[: limit - 1] + "..."
