# How the harness works

*Read this once before class, or follow along as we go through it together. It
takes about ten minutes.*

---

## 1. The thing in the middle is not an agent

The model we are using is a very large program that does exactly one thing:

> **You give it text. It gives you back text that plausibly follows.**

That is all. It cannot open a file. It cannot search. It cannot remember you.
It has no hands and no memory. Ask it to "review the contract" and it will
happily produce something that *sounds* like a contract review, without ever
having seen a contract.

Everything that makes an "AI agent" feel like an agent is scaffolding built
around that one ability. That scaffolding is called a **harness**, and this
repository contains a very small one — about 300 lines — so that you can see all
of it at once.

Five files, five ideas:

| File | Idea |
|---|---|
| `harness/model.py` | how we send text to the model |
| `harness/loop.py` | doing it more than once |
| `harness/tools.py` | letting the model cause things to happen |
| `harness/memory.py` | letting it write things down |
| `harness/ui.py` | showing you what happened |

---

## 2. The conversation is a list

Open `harness/model.py`. The important part is this shape:

```python
[{"role": "system",    "content": "You are a lawyer advising on..."},
 {"role": "user",      "content": "Begin. Your notebook is empty."},
 {"role": "assistant", "content": "I should start with the contract."}]
```

That list is the model's **entire world**. There is no hidden state, no
database, no session. Every time we call the model we send the whole list again.

Two consequences worth sitting with:

- **The model has no memory of anything not in that list.** What looks like
  memory is us re-sending the conversation each time.
- **Whoever controls the list controls the model.** In this harness, the first
  item on the list — the `system` message — is assembled by `loop.py` out of the
  harness rules, *your* `skill.md`, the brief, and the list of documents. That is
  where your influence enters the system.

---

## 3. The loop

Open `harness/loop.py`. Strip out the printing and it is this:

```
for turn in 1..5:
      ask the model
      look at what it asked for
      do those things
      hand back the results
      go round again

then: ask it once more, for the final answer
```

Why loop at all? Because that is how the work is actually done. A junior lawyer
handed a matter file does not read one page and write the advice. They look at
the index, pick the contract, read it, notice something, go and check the
correspondence, notice something else, and only then start writing.

One pass through a model gives you a first impression. A loop gives you a
process. **The loop is where "reading the documents" becomes possible at all**,
because on turn one the model has not read anything yet.

Five turns is arbitrary. It is enough to see the behaviour and cheap enough to
run twenty times in an afternoon. Real harnesses run for dozens of turns.

---

## 4. Tools: how a text machine causes things to happen

This is the part that surprises people.

A model can only produce text. So we hand it a **menu**. On every turn we send,
alongside the conversation, a list of things it is allowed to ask for. That list
is `TOOLS` in `harness/tools.py`, and each entry says what the tool is called,
what it does, and what arguments it takes:

```python
{"name": "read_document",
 "description": "Open one document from this matter's file and read it.",
 "parameters": {"filename": {"type": "string"}}}
```

The model then replies, in a structured way, *"call read_document with filename =
agreement-extract.md"*. And **we** open the file. **We** paste the contents into
the next message.

The model did not read anything. It asked. The harness acted.

That is what a tool is. Every AI agent that browses the web, sends email or
queries a database is doing this, with a longer menu.

Our agent has three tools. That is the whole toolbox:

| Tool | What the harness does |
|---|---|
| `read_document(filename)` | opens that document and shows it to the agent next turn |
| `remember(note)` | writes one line into `memory.yaml` |
| `done(reason)` | ends the gathering phase so the write-up can start |

Watch the terminal during a run. Every `-> read` and `-> remember` line is one of
these, and each one exists because the model asked for it.

**The descriptions are not decoration.** That wording is the *only* thing the
model knows about each tool. Change "one short line" to "a paragraph" in the
`remember` description and the notebook fills up with essays. Tool descriptions
are prompt engineering.

**Watch what happens when it gets it wrong.** Ask for a file that does not exist
and the harness hands back an error naming the real files. Call no tool at all and
the harness says so and moves on. Handling the model's mistakes is most of what a
harness does.

### One wrinkle worth knowing

This particular model *thinks before it answers*, and the server returns that
thinking in a separate field. Two consequences you can see in the code:

- The terminal prints it on the `thinking:` lines. During the loop the model
  usually says almost nothing out loud — it thinks, then calls a tool — so the
  thinking is the interesting part to watch. Use `--think` to see all of it.
- When we send the conversation back, the model's own thinking has to go back
  with it, or the server rejects the request. That is what `reasoning_content`
  is doing in `harness/model.py`. Different model servers differ on details like
  this, and finding out is a normal part of the work.

## 5. Memory is a file

Open `memory.yaml` after your first run. It looks like this:

```yaml
problem: 1-dispute
updated: "2026-09-12 15:04"
notes:
  - "FACT: the agreement is governed by French law (clause 24.1)"
  - "CLAUSE: 4.3 makes service credits the sole remedy for late go-live"
  - "ISSUE: no valid notice was ever served under clause 22"
```

That is agent memory. Not a metaphor for one — an actual text file on disk, which
you can open, read, edit and delete.

The mechanism is two lines of the loop:

1. Before each turn, the harness pastes the notes into the message it sends.
2. When the model calls `remember`, the harness adds a line.

Why bother, when the conversation already contains everything? Three reasons,
and they are the same three reasons lawyers keep attendance notes:

- **It survives.** The conversation is thrown away when the run ends. The file is
  still there tomorrow. Run problem 1 twice and watch the second run start with
  what the first one learned.
- **It is selective.** The conversation holds everything, including the noise.
  The notebook holds what the agent decided was worth keeping. Deciding what to
  write down is a professional skill, and you can direct it from `skill.md`.
- **You can audit it.** You cannot easily inspect what a model "thinks". You can
  open a file and see, in one page, what it concluded and when.

Try this after a run: delete a line from `memory.yaml`, add a wrong one, and run
it again. The agent will believe you.

---

## 6. The skill file is the only interesting file

Everything above is plumbing. It is the same plumbing whether you are doing a
dispute, a share purchase or a compliance review.

Open `harness/loop.py` and find `HARNESS_RULES`. Read it. Notice what is *not*
there: nothing about chronologies, nothing about limitation clauses, nothing
about how an advice note should be structured, nothing about being careful with
quantum. It explains three tags and stops.

That is deliberate. It means the entire difference between a mediocre run and a
good one lives in **`skill.md`**, which is dropped into the system message word
for word:

```python
"## YOUR SKILL",
"The following is your professional instruction set for this kind of work. "
"Follow it closely.\n\n" + clean_skill(skill_text),
```

Nothing reads it, summarises it, checks it or improves it. What you write is
what the agent gets.

Right now `skill.md` says *"You are a lawyer. Deal with this matter."*

Run it. What comes back will be **good** — clause references, a correct reading of
the decisive clause, a sensible commercial recommendation. Better, probably, than
a first-year could produce in an afternoon.

That is the honest starting point, and it is the interesting one. The gap you are
working in is narrower than "the machine cannot do law", and it is exactly where
your value sits: it answered the questions it *guessed* were being asked, in a
structure *it* invented, with no chronology, no statement of the other side's
case, no owners or deadlines, and nothing declared about what it assumed.

**That gap is the subject of this session.** Not prompting, and not the model.
What, precisely, does a lawyer know that a very capable general system does not —
and how much of it can you actually write down?

Score it before you believe it: [02-what-good-looks-like.md](02-what-good-looks-like.md).

---

## 7. What we have simplified

Worth knowing, so you are not surprised later:

- **The toolbox.** Three tools. A production harness has dozens, and most of the
  hard engineering is in the tools, not the loop.
- **Retrieval.** We hand the agent a folder of five documents. Real systems
  search across thousands, which brings its own hard problems.
- **Verification.** Nothing here checks whether the agent's answer is *true*.
  Serious systems add citation checking, a second model to critique the first,
  and human review gates.
- **Cost and limits.** We ignore token budgets, rate limits and long-context
  behaviour, all of which dominate real deployments.
- **Confidentiality.** We are sending fictional documents to a third-party model.
  Doing this with a real matter file is a decision with rules attached.

None of these change the shape of what you have seen. They make it bigger.
