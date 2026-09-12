#!/usr/bin/env python3
"""run.py - the button you press.

    python3 run.py            show the list of problems
    python3 run.py 1          run the agent on problem 1
    python3 run.py 1 --fresh  run it with an empty notebook
    python3 run.py 1 --think  run it and show all of the model's reasoning
    python3 run.py --check    check your setup is working (do this first)
    python3 run.py --selftest check the workshop files are intact (no key needed)

This file just works out WHICH problem you meant, then hands over to
harness/loop.py, which is where the interesting part lives.
"""

import datetime
import os
import shutil
import sys

from harness import loop, memory, model, tools, ui

PROBLEMS_DIR = "problems"


def find_problems():
    """Every folder inside problems/ is a problem."""
    found = []
    for name in sorted(os.listdir(PROBLEMS_DIR)):
        folder = os.path.join(PROBLEMS_DIR, name)
        brief = os.path.join(folder, "brief.md")
        if os.path.isdir(folder) and os.path.exists(brief):
            found.append(
                {
                    "name": name,
                    "number": name.split("-")[0],
                    "title": title_of(brief),
                    "folder": folder,
                    "brief_file": brief,
                    "skill_file": os.path.join(folder, "skill.md"),
                    "documents_dir": os.path.join(folder, "documents"),
                    "output_dir": os.path.join(folder, "output"),
                }
            )
    return found


def title_of(brief_file):
    """The first '# heading' line of brief.md is the problem's title."""
    with open(brief_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("# "):
                return line[2:].strip()
    return "(untitled)"


def show_menu(problems):
    ui.banner("EDHEC LEGAL AI - a tiny agent harness")
    print("  Choose a problem:\n")
    for p in problems:
        docs = len(tools.list_documents(p["documents_dir"]))
        print("   %s%s%s  %s" % (ui.BOLD, p["number"], ui.OFF, p["title"]))
        print("      %sfolder: %s   documents: %d%s" % (ui.DIM, p["folder"], docs, ui.OFF))
    print("\n  Run one like this:\n")
    print("     %spython3 run.py %s%s\n" % (ui.BOLD, problems[0]["number"], ui.OFF))
    print("  %sFirst time? Run  python3 run.py --check  to test your setup.%s\n" % (ui.DIM, ui.OFF))


def ensure_env_file():
    """Make the .env file for the student if it does not exist yet.

    Creating a file whose name begins with a dot is fiddly the first time,
    so the harness just does it. The student only has to paste their key in.
    """
    if os.path.exists(".env") or not os.path.exists(".env.example"):
        return False
    shutil.copyfile(".env.example", ".env")
    return True


def check_setup():
    """A 10-second test that everything is ready. Run this before class."""
    ui.banner("CHECKING YOUR SETUP")
    ok = True

    if ensure_env_file():
        ui.action("[new]", "I made you a .env file (copied from .env.example)", ui.YELLOW)
    if os.path.exists(".env"):
        ui.action("[ok]", "found your .env file")
    else:
        ui.action("[X] ", "there is no .env file and no .env.example to copy", ui.RED)
        return False

    cfg = model.settings()
    for label, key in (("API_KEY", "api_key"), ("BASE_URL", "base_url"), ("MODEL", "model")):
        value = cfg[key]
        if value == "paste-your-key-here":
            ui.action("[X] ", "you have not pasted your key into .env yet", ui.RED)
            ui.step("Open .env and replace paste-your-key-here with the key you were sent.")
            ok = False
        elif not value:
            ui.action("[X] ", "%s is missing from .env" % label, ui.RED)
            ok = False
        elif key == "api_key":
            ui.action("[ok]", "API_KEY is set (ends ...%s)" % value[-4:])
        else:
            ui.action("[ok]", "%s = %s" % (label, value))
    if not ok:
        return False

    ui.step("saying hello to the model (this takes a few seconds)...")
    try:
        reply = model.ask(
            [{"role": "user", "content": "Reply with exactly: ready"}], max_tokens=400
        )
    except model.ModelError as err:
        ui.error(str(err))
        return False
    ui.action("[ok]", 'the model answered: "%s"' % " ".join(reply["text"].split())[:60])

    print()
    ui.action("[ok]", "You are ready. Try:  python3 run.py 1", ui.GREEN)
    print()
    return True


def self_test():
    """Check the workshop files are intact. Needs no API key and no internet.

    Run this after changing anything, and once before class.
    """
    ui.banner("SELF TEST")
    problems = find_problems()
    failures = []

    def check(ok, description):
        ui.action("[ok]" if ok else "[X] ", description, ui.GREEN if ok else ui.RED)
        if not ok:
            failures.append(description)

    check(len(problems) == 3, "found 3 problems (found %d)" % len(problems))

    for p in problems:
        documents = tools.list_documents(p["documents_dir"])
        check(os.path.exists(p["skill_file"]), "%s has a skill.md" % p["name"])
        check(len(documents) >= 3, "%s has %d documents" % (p["name"], len(documents)))
        check(p["title"] != "(untitled)", "%s brief.md has a title" % p["name"])

        # The skill file's guidance notes must not leak into the model's prompt.
        raw = open(p["skill_file"], "r", encoding="utf-8").read()
        sent = loop.clean_skill(raw)
        check("<!--" not in sent and "-->" not in sent, "%s skill notes are stripped" % p["name"])
        check(len(sent) < 600, "%s starts from a near-empty skill (%d chars)" % (p["name"], len(sent)))

    # memory.yaml must survive a round trip, including awkward characters.
    scratch = os.path.join(problems[0]["output_dir"], ".selftest.yaml")
    sample = {"problem": "test", "notes": ['he said "no" \\ and: this', "second note"]}
    memory.save(sample, scratch)
    back = memory.load(scratch)
    os.remove(scratch)
    check(back["notes"] == sample["notes"], "memory.yaml survives a round trip")

    # The harness rules must stay free of legal guidance - that is the whole design.
    rules = loop.HARNESS_RULES.lower()
    leaked = [w for w in ("clause", "chronology", "quantum", "advice note") if w in rules]
    check(not leaked, "harness rules contain no legal guidance%s"
          % ("" if not leaked else " (found: %s)" % ", ".join(leaked)))

    print()
    if failures:
        ui.error("%d check(s) failed." % len(failures))
        return False
    ui.action("[ok]", "everything is intact.", ui.GREEN)
    print()
    return True


def next_run_number(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    used = [
        int(f.split("-")[1])
        for f in os.listdir(output_dir)
        if f.startswith("run-") and f.split("-")[1].isdigit()
    ]
    return max(used) + 1 if used else 1


def save_output(problem, result, run_number):
    os.makedirs(problem["output_dir"], exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    tag = "%02d" % run_number

    answer_path = os.path.join(problem["output_dir"], "run-%s-answer.md" % tag)
    with open(answer_path, "w", encoding="utf-8") as f:
        f.write(
            "<!-- run %s | %s | skill.md was %d characters | documents read: %s -->\n\n"
            % (tag, stamp, result["skill_chars"], ", ".join(result["documents_read"]) or "none")
        )
        f.write(result["answer"].strip() + "\n")

    transcript_path = os.path.join(problem["output_dir"], "run-%s-transcript.md" % tag)
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write("# Run %s transcript - %s\n\n" % (tag, stamp))
        f.write("Everything the model said, and everything the harness did.\n")
        for heading, text in result["transcript"]:
            f.write("\n\n---\n\n## %s\n\n%s\n" % (heading, text.strip()))

    return answer_path, transcript_path


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    flags = [a for a in argv if a.startswith("--")]

    if not os.path.isdir(PROBLEMS_DIR):
        ui.error("Run this from the folder that contains run.py and problems/.")
        return 1

    if "--selftest" in flags:
        return 0 if self_test() else 1

    if "--check" in flags:
        return 0 if check_setup() else 1

    ensure_env_file()

    problems = find_problems()
    if not problems:
        ui.error("No problems found inside the problems/ folder.")
        return 1

    if not args:
        show_menu(problems)
        return 0

    wanted = args[0].lstrip("0") or "0"
    chosen = next(
        (p for p in problems if p["number"].lstrip("0") == wanted or p["name"] == args[0]), None
    )
    if chosen is None:
        ui.error(
            "There is no problem '%s'. Available: %s"
            % (args[0], ", ".join(p["number"] for p in problems))
        )
        return 1

    max_loops = 5
    for flag in flags:
        if flag.startswith("--loops="):
            max_loops = max(1, min(10, int(flag.split("=")[1])))

    if not os.path.exists(chosen["skill_file"]):
        ui.error("There is no skill.md in %s" % chosen["folder"])
        return 1

    ui.banner("EDHEC LEGAL AI - a tiny agent harness")
    try:
        result = loop.run(
            chosen,
            max_loops=max_loops,
            fresh="--fresh" in flags,
            show_thinking="--think" in flags,
        )
    except model.ModelError as err:
        ui.error(str(err))
        return 1
    except KeyboardInterrupt:
        print("\n  stopped.\n")
        return 1

    run_number = next_run_number(chosen["output_dir"])
    answer_path, transcript_path = save_output(chosen, result, run_number)

    ui.rule("FINISHED")
    ui.quote(result["answer"], limit=2000)
    print()
    ui.action("[saved] ", "the work product : %s" % answer_path)
    ui.action("[saved] ", "the full transcript: %s" % transcript_path)
    ui.action("[memory]", "memory.yaml now has %d notes" % len(result["memory"]["notes"]))
    ui.action("[cost]  ", "this run used about %s tokens" % "{:,}".format(result["tokens"]))
    print(
        "\n  %sNow open %s, improve it, and run this again.\n"
        "  Compare run-%02d-answer.md with the next one.%s\n"
        % (ui.DIM, chosen["skill_file"], run_number, ui.OFF)
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
