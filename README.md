# EDHEC Legal AI — the tiny agent harness

A three-hour workshop. You will run a real AI agent over a real legal matter,
then make it better by writing down what a lawyer knows.

**You will not write any code.** You will edit one file, `skill.md`, in English.

---

## The idea in one picture

```
   skill.md ─────────────┐                    the agent asks for:
   (what you write)      │
                         ▼                    read_document(filename)
   brief.md ───────►  ┌──────────────┐  ───►  remember(note)
   documents/ ─────►  │   THE LOOP   │  ───►  done(reason)
   memory.yaml ────►  │  (5 turns)   │  ◄───
                      └──────────────┘        and the harness does them
                            │
                            ▼
                    the work product
```

The harness is deliberately stupid. It knows how to run a loop, open a file and
write a note. It knows nothing about law — there is a test that fails the build if
a word like "clause" appears in its instructions. Every piece of legal judgement
in the system comes from `skill.md`, and you write that.

**Fair warning.** Run it with the skill file empty and the output will be good.
This is a very capable model. The session is not about rescuing a broken machine;
it is about finding the difference between an answer that looks professional and
one that is fit to send — and writing that difference down.

---

## Getting started

1. **[START-HERE.md](START-HERE.md)** — set up in about ten minutes. Do this before class.
2. **[docs/00-how-the-harness-works.md](docs/00-how-the-harness-works.md)** — what the five files do.
3. **[docs/01-writing-a-skill.md](docs/01-writing-a-skill.md)** — how to write a good skill file.
4. **[docs/02-what-good-looks-like.md](docs/02-what-good-looks-like.md)** — the scorecard. Print it.

Once you are set up:

```bash
python3 run.py --check     # test that everything works
python3 run.py             # see the three problems
python3 run.py 1           # run the agent on problem 1
python3 run.py 1 --fresh   # ... starting from an empty notebook
python3 run.py 1 --think   # ... showing all of the model's reasoning
```

A run takes 90 seconds to two minutes and uses about 45,000 tokens.

---

## The three problems

| # | Folder | Matter |
|---|---|---|
| 1 | `problems/1-dispute` | A supplier delivered a software platform four months late. Advise the client. |
| 2 | `problems/2-transaction` | A due diligence finding appears two weeks before signing. Advise the deal team. |
| 3 | `problems/3-compliance` | HR wants to switch on an AI CV screening tool. Advise the executive committee. |

Each folder contains:

```
brief.md      what the client wants          (read it; do not edit it)
documents/    the matter file                (the agent reads these)
skill.md      >>> THE ONLY FILE YOU EDIT <<<
output/       what the agent produced        (created when you run it)
```

---

## What is in this repository

```
run.py                the button you press
harness/              the harness itself, about 300 lines of plain Python
  loop.py               the loop
  memory.py             the notebook (memory.yaml)
  tools.py              the three things the agent can do
  model.py              talking to the AI model
  ui.py                 printing to the screen
problems/             the three matters
docs/                 the written material for the session
  worked-examples/      a strong skill file, and two real outputs to compare
.env                  your API key (never leaves your machine, never committed)
```

There is nothing to install. The harness uses only what comes with Python.

---

*All matters, parties, documents and events in this repository are fictional and
were written for teaching. Nothing here is legal advice.*
