# Teaching notes — three hours

*For the instructor. Not part of the student material.*

---

## Read this first: what the build actually found

The pilot was designed on the assumption that a near-empty skill file would
produce weak output, and that students would visibly rescue it. **Testing against
the real model disproved that**, and the session has been rebuilt around what is
actually true.

With `skill.md` saying only *"You are a lawyer. Deal with this matter."*, the
model produces roughly 1,400 words on problem 1 that:

- correctly identify clause 4.3 as a sole-remedy clause and grasp what it destroys;
- calculate the liability cap correctly (EUR 150,000 — fees *paid*, not the annual fee);
- spot that no valid notice was ever served, because email is excluded by clause 22.1;
- spot that the client's own withholding breaches clause 9.2;
- recommend settlement over termination, for sound commercial reasons.

That is a competent associate's first draft. **Do not plan a session around
laughing at the machine.** A sharp student will run it in the first ten minutes,
see that it is good, and you will lose the room.

### What the empty-skill run does *not* do

Measured across test runs, consistently:

| Missing | Why it matters |
|---|---|
| No chronology | A dispute note without dates is not a dispute note |
| No statement of the other side's case | Nobody can test the advice |
| Next steps with no owner and no date | Nothing happens on Monday |
| No declared assumptions | You cannot tell which parts are load-bearing |
| A structure it invented | Not the firm's, and not one anyone agreed |
| It answers the questions *it* inferred | It was never told to go and find what the client actually asked |
| In one run, an invented date | The note was dated three weeks before the board meeting it was written for |

### The measured A/B

Same problem, same model, same documents. Only `skill.md` changed. Both outputs
are committed in `docs/worked-examples/` — use them if the API is down.

| | Empty skill | Worked-example skill |
|---|---|---|
| Length | 1,373 words | 1,117 words |
| Structure | invented, 6 sections | the firm's 5 prescribed sections |
| Reading order | ad hoc | client's instructions first, as directed |
| Memory notes | 2, vague | 5, prefixed `CLAUSE:` / `DATE:`, with clause numbers |
| Chronology | absent | present |
| Quantum | asserted | head by head, each with a reason |
| Next steps | topics | numbered, each with an owner and a date |
| Assumptions | none | six, each with what would resolve it |

**So the lesson is not "AI cannot do law."** It is:

> The analysis is largely free now. What is not free is knowing what the client
> actually asked, what the firm sends, what must never be left out, and what has
> to be true before anyone signs it. That is the part you write down — and the
> part you cannot write down is what you are paid for.

That is a harder, more current, and considerably more defensible session than the
one originally planned. It also survives the model getting better next year.

## The one design decision to explain

`HARNESS_RULES` in `harness/loop.py` contains **no legal guidance whatsoever** —
there is a self-test that fails the build if the words "clause", "chronology",
"quantum" or "advice note" appear in it. It explains the machinery and stops.

Show them the code. Otherwise a sharp student will assume the good output came
from something hidden, and the point collapses.

Note also that the **briefs deliberately do not say what to produce.** The client's
actual questions live in the matter file (`client-instructions.md`,
`deal-team-instructions.md`). An agent that does not go looking will answer the
wrong question — and the skill file is what sends it looking.

---

## Before the day

- [ ] **Students create their own API keys** at
      [platform.ifm.ai](https://platform.ifm.ai/) — this is in `START-HERE.md`.
      **Verify the exact wording of the signup and key-creation screens yourself
      and correct `START-HERE.md` if it has drifted.** The site blocks automated
      access, so those steps were written generically and have not been checked
      against the live UI.
- [ ] Confirm the free allowance on a new IFM account covers the session. **Budget
      roughly 45,000 tokens per run**, and a working student will run it eight to
      twelve times. If the allowance is tight, say so up front and tell them to use
      `--loops=3` while drafting.
- [ ] Send `START-HERE.md` at least 48 hours ahead. Ask for a reply confirming
      `python3 run.py --check` passed. Chase non-repliers. **This is the single
      highest-value thing you can do.**
- [ ] Run `python3 run.py --selftest` on a fresh clone. No key needed.
- [ ] Time one full run on the day's network. It took **90–140 seconds** in testing.
      Say that number out loud in class so nobody thinks it has hung.
- [ ] Projector machine: terminal font ~18pt. Everything here is read off a terminal.
- [ ] Print `docs/02-what-good-looks-like.md`, one per student. The session does
      not work if they are eyeballing quality instead of scoring it.
- [ ] Decide on `docs/worked-examples/`. It holds a strong skill file for problem 1
      and both sample outputs. Recommended: leave it in, and say out loud that
      opening it early wastes their own hour.

## Contingencies

| If | Then |
|---|---|
| The API is down or rate-limited | `docs/worked-examples/sample-A-empty-skill.md` and `sample-B-worked-skill.md` are real outputs. The scoring and comparison exercise works entirely on paper. This is a complete fallback — the session survives with no model at all. |
| A student's free allowance runs out | Pair them. Two to a laptop is better than one watching you debug. |
| Runs are slow | `--loops=3`. Quality barely moves; the model usually calls `done` on turn three anyway. |
| A few never got set up | Pair them, and fix it at the break, not in the first ten minutes. |
| Someone commits their key | `.env` is gitignored, so this should not happen. If it does: delete the key at platform.ifm.ai, make a new one. Thirty seconds. Make it a teaching moment, not a drama. |

---

## Run sheet

### 0:00 – 0:10 · Setup triage

Do not start teaching. *"Everyone type `python3 run.py --check`. Hands up if you
do not see five green ticks."* Fix or pair those. Ten minutes here saves thirty later.

### 0:10 – 0:30 · Framing

No slides. One terminal.

1. **The model is a text machine.** Text in, text follows. No memory, no hands, no
   files. Demonstrate: ask it about "the contract" with no contract supplied and
   let the room watch it invent one confidently. This lands harder than any
   warning about hallucination.
2. **A harness is the scaffolding that makes it useful.** Loop, tools, memory. Draw
   the README diagram on the board.
3. **A skill is where the expertise goes.** Set the hour up honestly: *"The output
   you are about to see is good. Your job today is to find out why it is still not
   sendable, and to write down the difference."*

### 0:30 – 0:55 · The baseline run, and scoring it

On the projector: `python3 run.py 1 --fresh`

Talk over it as it goes. Point at each `-> read` and `-> remember` line as it
appears: *"that happened because the model asked, and the harness acted."* Point
at the `thinking:` lines: *"that is the model reasoning before it acts. We do not
act on it. We act on what it asks for."*

Then hand out the scorecard. **Do not critique the output yourself.** Give them
six minutes in pairs to score it out of twenty.

Collect the numbers on the board. They will cluster around 10–13. Then work
through the rows that scored 0, and ask for the sentence that would fix each.
**Those sentences are the class's first skill file, and they wrote them.**

If someone says "this is already better than what I'd write" — that is the best
thing that can happen. Agree with them, and ask: *"So what is left for you to do?"*
That question is the session.

### 0:55 – 1:15 · The harness tour

Four files, five minutes each. Show one thing in each; do not read code line by line.

| File | The one thing |
|---|---|
| `harness/model.py` | The messages list. *"This is the model's entire world. Every call sends all of it."* |
| `harness/loop.py` | The `for turn in range(...)` block — *"that is the agent"* — then `HARNESS_RULES`: *"notice there is no law in here."* |
| `harness/tools.py` | The `TOOLS` list. *"We hand it a menu. It picks. We do the work. It has no hands."* |
| `harness/memory.py` | Then open `memory.yaml`. *"That is agent memory. It is a file."* |

**Do this live:** edit a line in `memory.yaml` to something false, save, re-run, and
let them watch the agent rely on it. Thirty seconds, and it teaches more about AI
system risk than a lecture on hallucination.

### 1:15 – 1:25 · Break

### 1:25 – 2:25 · The exercise

*"Open `problems/1-dispute/skill.md`. Get the score up. One change at a time,
re-run, re-score."*

Point at `docs/01-writing-a-skill.md` and leave them alone for ten minutes before
circulating.

| Behaviour | Intervention |
|---|---|
| Writing the answer into the skill file | *"Would this still be right for a different contract? A skill is for a kind of job."* |
| Writing 3,000 words | *"Which three sentences are doing the work? Delete the rest and run it."* |
| "Be thorough and professional" | *"Give me an instruction you could be wrong about."* |
| Changing five things at once | *"You cannot tell which one worked. Revert four."* |
| Reading the output but not the transcript | Open `output/run-NN-transcript.md` with them and find the turn where it went wrong. |
| Declaring victory because it looks nice | Hand them the scorecard again. Ask for the number. |
| Finished early | Problem 2 or 3 — or better, the planted discovery below. |

**The planted discovery.** The worked-example skill contains one instruction that
does not work: *"say what the counterparty will argue"* sits inside a behaviour
list and gets absorbed, while the required-headings list next to it lands every
time. It is written up in `docs/worked-examples/1-dispute-skill.md`.

Most students will hit this on their own — they will ask for something and not get
it. When they do, do not fix it for them. Ask: *"Would its absence be obvious?"*
The rule is worth more than the exercise:

> **Instructions that specify a visible structure land. Instructions that specify
> a behaviour get approximated.**

Around 2:05, tell the room to stop editing and get one clean scored run saved.

### 2:25 – 2:45 · Show and tell

Three students, five minutes each, on the projector: skill file, run-01 score,
final score. Pick one who succeeded, one who over-engineered, one who found
something odd. Ask each: *"which single instruction moved the number most?"*

### 2:45 – 3:00 · Debrief

Two questions, in order. The first is warm-up. The second is the session.

1. **"What did you write down that made the biggest difference?"** Collect on the
   board. It will be procedural: reading order, named traps, required headings,
   negative rules. Point that out — *"none of that is law."*

2. **"What did you know that you could not write down?"** This is the one. Let it
   be slow. What usually surfaces: judging what the client actually wants as
   against what they asked for; how hard to push a weak argument; knowing which
   sentence in the file is the important one; deciding to tell a client something
   they do not want to hear.

Close on the honest version:

> *"Everything on the first list is now a file. It can be copied, run at three in
> the morning, and it does not get tired. That part of the job has changed
> permanently, and it changed while you were at university, not before you got
> here.*
>
> *The second list is what you are being paid for. Most lawyers have never had to
> say out loud what is on it. You just did — and you did it by trying to automate
> yourselves and watching exactly where it stopped working."*

---

## Discussion prompts

- Who is liable when the skill file is wrong — the author, the firm, or the model
  supplier? Does it change if the file was bought in?
- A skill file is transferable in a way judgement is not. What happens to the
  value of a firm's know-how when it can be copied as a text file?
- The agent read five documents. What breaks at fifty thousand?
- Nothing here checks whether the answer is *true*. What would you add, and who
  signs it off?
- We sent fictional documents to a third-party model in another jurisdiction.
  Walk through what you would need to establish before doing that with a real
  matter file. (Problem 3 is about exactly this, which is worth pointing out.)

## Extensions

- Same problem, two skill files, blind comparison — the room guesses which
  instructions produced which output.
- Have them write a skill file for a task from their own internship.
- `--loops=10`. Ask what improves and what does not. (Usually: nothing. It calls
  `done` on turn three either way. Good lesson about where the gains are not.)
- **Write an adversarial skill file** — instructions that make the output *look*
  more authoritative while being less reliable. Then ask how you would detect
  that from the outside. This one tends to produce the best discussion of the day.
