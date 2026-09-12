# Writing a skill file

*This is the exercise. Everything else was set-up.*

---

## What you are actually doing

A skill file is an attempt to write down what a competent lawyer knows about
*how to do a particular kind of job* — the part that never appears in the
textbook because everyone in the room already has it.

Not the law. The model has read more law than you have. What it does not have is
the thing a supervising partner transmits in eighteen months of corrections:

- read the notices clause before you get excited about termination
- the client's loss schedule is a wish list, not a claim
- if you cannot say what the counterparty will argue, you have not finished
- never give the board options without a recommendation

That is what goes in the file.

---

## Run it once before you write anything

```bash
python3 run.py 1 --fresh
```

Read the answer in `problems/1-dispute/output/run-01-answer.md`.

**Be ready for it to be good.** With `skill.md` saying nothing but *"You are a
lawyer. Deal with this matter."*, this model produces about 1,400 words with
clause references, a correct reading of the sole-remedy clause, a sensible
commercial recommendation and a settlement strategy. It looks like something a
competent associate wrote.

That is the honest starting position, and it is the interesting one. The gap you
are working in is not *"the machine cannot do law."* It is narrower, and it is
where your actual value sits:

- It answered the questions it decided were being asked. It was not told to go
  and find what the client actually asked for.
- It invented a structure. Not your firm's structure, and not one anybody agreed.
- It gave you no chronology, and a dispute note without a chronology is not a
  dispute note.
- It never states what the other side will argue, so nobody can test it.
- Its next steps have no owner and no date, so nothing happens on Monday.
- It declared nothing it assumed, so you cannot tell which parts are load-bearing.
- In one test run it dated the note three weeks before the board meeting it was
  written for. It made the date up.

Every one of those is a sentence missing from `skill.md`.

**Now go and score it properly** against
[docs/02-what-good-looks-like.md](02-what-good-looks-like.md), and write the
number down. Twenty points. Most empty-skill runs land somewhere around eleven.

Then write your first three instructions — the three rows you scored lowest.

## The shape that works

Most good skill files have five parts. Use these headings or your own.

```markdown
# <name of the job>

## How to work
   what to read first, in what order, and when to stop reading

## What to look for
   the specific clauses, dates, numbers and traps in this kind of matter

## How to analyse
   the steps of the reasoning, in order

## What to produce
   the exact headings of the finished document, and its length

## House rules
   what to always do, and what to never do
```

---

## Six techniques, with examples

### 1. Give an order of work, not a list of topics

The agent has five turns. If it spends three of them on the wrong documents it
cannot recover.

> ✗ *"Review the relevant documents."*
>
> ✓ *"Read in this order and stop when you can answer the client's questions:
> (1) the client's instructions, so you know what is actually being asked;
> (2) the contract, because the answer is usually in it; (3) the correspondence,
> in date order; (4) anything about quantum, last. Do not read a background note
> before you have read the contract."*

### 2. Name the traps

This is the highest-value thing you can write. You know where the bodies are
buried in this kind of matter. The model does not know which of a hundred
possibilities matters *here*.

> ✗ *"Consider the limitation of liability provisions."*
>
> ✓ *"Before valuing any claim, find and quote: the sole-remedy clause, the
> exclusions of loss (loss of profit is almost always excluded), the liability
> cap and what it is calculated on, and the notice requirements for termination.
> A claim that fails on any of these is worth nothing, however good the merits.
> Check them before you write a word about merits."*

### 3. Make it check itself against the facts

Force the agent to test its own conclusions against the documents rather than
producing what usually happens in matters like this.

> ✓ *"For every conclusion, quote the clause number or the dated document it
> rests on. If you cannot, label it 'assumption' and list it in the open points
> section. Do not describe a document you have not opened."*

### 4. Specify the output precisely

Vague instructions about tone produce vague documents. Give it the skeleton.

> ✗ *"Write a clear and professional advice note."*
>
> ✓ *"Produce a note of no more than 900 words with these headings, in this
> order: 1. Answers (one sentence per client question, with a yes/no/qualified
> where possible); 2. What happened (a dated chronology, maximum eight lines);
> 3. Analysis (one sub-heading per question); 4. What we recommend (numbered
> actions, each with an owner and a deadline); 5. Risks and open points.
> Section 1 must be readable on its own by a board member who reads nothing
> else."*

### 5. Write the negative rules

Half of professional judgement is knowing what not to do. Models are agreeable
by default and will tell the client what they want to hear.

> ✓ *"Never accept the client's loss figures. Take each head of loss in turn and
> say whether it is recoverable, reduced or excluded, and why."*
>
> ✓ *"Never recommend litigation without stating what it costs, how long it
> takes and what happens to the commercial relationship."*
>
> ✓ *"If the client's preferred answer is wrong, say so in the first paragraph.
> Do not bury it."*

### 6. Make it argue the other side

> ✓ *"Before your recommendation, write one short paragraph headed 'What the
> other side will say', putting their best argument as strongly as you can. If
> your recommendation does not survive it, change the recommendation."*

---

## How to iterate

The whole skill is in the loop below. Do it five or six times.

```bash
python3 run.py 1 --fresh          # run it
# open output/run-01-answer.md    # read it critically
# open skill.md                   # change ONE thing
python3 run.py 1 --fresh          # run it again
# compare run-01-answer.md with run-02-answer.md
```

Three rules for iterating:

1. **Change one thing at a time.** Change five and you will not know which
   worked. This is an experiment.
2. **Use `--fresh`** while you are comparing, so each run starts from the same
   empty notebook. Otherwise you are comparing runs with different memory.
3. **Read `output/run-NN-transcript.md` when a run goes wrong.** It shows every
   turn: what the agent asked for, what it got, what it wrote down. Usually you
   can see the exact turn where it went off, and fix that turn.

---

## Things that will not work

**Writing the answer into the skill file.** *"Conclude that the cap applies and
the claim is worth 24,000."* You have written the answer once, for one matter. A
skill is instructions for a *kind* of work, and should still be right for the
next matter of that kind. Test: would this file still be useful with a different
contract in the folder?

**Length for its own sake.** A 4,000-word skill file is usually worse than a
600-word one. Long files contradict themselves and bury the instructions that
matter. If two instructions conflict, the agent will pick one, and not the one
you meant.

**Politeness.** *"Please try to be thorough and consider all relevant factors."*
This does nothing. Every word should be something you could be wrong about.

**Describing quality instead of causing it.** *"The analysis should be rigorous
and commercially aware."* Compare: *"State the recoverable quantum as a range,
with the assumptions that produce each end of it."* The second one is an
instruction. The first is a hope.

---

## Directing the notebook

One extra lever, easy to miss. The agent's memory (`memory.yaml`) is written by
the agent, so you can tell it how to keep notes:

> ✓ *"Write a memory note the moment you find anything decisive, and prefix every
> note with one of: FACT, DATE, CLAUSE, ISSUE, RISK. Record the clause number
> whenever you record a clause. Do not write a note that restates the brief."*

Then open `memory.yaml` after the run. A tidy, well-prefixed notebook is a
reliable sign that the run went well — and a mess in there usually explains a
mess in the output.

---

## The question to leave with

You are about to spend an hour discovering that most of what makes legal work
good is procedural, specific, and writable down — and that the last ten percent
of it is very hard to write down at all.

Both halves of that are the point. Keep track of which of your instructions were
easy to write, and which you could not make precise. **The second list is the
more interesting one**, and it is where the argument about what this technology
can and cannot absorb actually sits.
