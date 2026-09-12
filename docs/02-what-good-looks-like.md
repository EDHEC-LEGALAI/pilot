# What good looks like — scoring the output

*Print this. Use it on every run.*

---

## Read this first

The model you are using is very capable. Run any of these problems with an empty
skill file and what comes back will look like a real piece of legal work: headings,
clause references, a confident tone, a recommendation.

**That is the trap this session is really about.** Your job is not to be impressed.
Your job is to score it, find what is missing, and write an instruction that fixes
it. An output that looks professional and is not fit to send is more dangerous than
one that is obviously bad, because nobody checks it.

So: do not read the output and ask *"is this good?"* Score it against the twenty
points below and write down the number. Then change one thing in `skill.md` and
score it again.

---

## The scorecard

Two points each. Score honestly — the number only means something if you are hard
on it.

| # | Test | 0 | 1 | 2 |
|---|---|---|---|---|
| 1 | **It answers what was actually asked.** The client's real questions are in the matter file, not the brief. Did it find them and answer *those*? | Answers a question nobody asked | Answers some | Answers each, explicitly |
| 2 | **The answer comes first.** A reader who stops after the first section can still act. | Buries it | Summary exists but hedges | Clear answer up front, per question |
| 3 | **Every conclusion is anchored.** Clause number, or dated document. | Assertions | Some references | Anchored throughout |
| 4 | **It found the clauses that decide the matter** — the ones that kill or save the claim, not the ones that are easy to find. | Missed them | Found some | Found them and worked out what they mean in money |
| 5 | **Numbers are tested, not repeated.** The client's schedule is a wish list. | Adopts the client's total | Queries it | Head by head: recoverable, reduced or excluded, and why |
| 6 | **The other side's case is stated.** At its strongest. | Absent | A nod to it | Put properly, and the recommendation survives it |
| 7 | **Entitlement, recovery and action are kept apart.** What you *may* do, what you will *get*, what you *should* do. | Blurred | Two of three | All three, distinctly |
| 8 | **Next steps are executable.** Someone can act on Monday. | None | A list of topics | Numbered actions with an owner and a date |
| 9 | **Assumptions and gaps are declared.** What it did not see, what it took on trust. | None | Vague caveat | Listed, specific, with what would resolve each |
| 10 | **It fits the reader.** Length, register, and format for the person receiving it, including anything they asked for. | Ignores it | Roughly right | Exactly what that reader needs and no more |

**/20**

---

## Automatic failures

Any one of these means the note is not sendable, whatever it scored:

- **An invented fact.** A date, a figure, a clause number or a case that is not in
  the file. Check the ones that matter. Models produce these confidently, and this
  one has done it in testing — an advice note dated three weeks before the meeting
  it was written for.
- **A document described but not read.** Compare the note against the `-> read`
  lines in the terminal. If it characterises something it never opened, that is the
  end of the exercise.
- **A stated client constraint ignored.** If the client asked for short answers and
  got two thousand words, the note failed before anyone read it.
- **A conclusion with no source** on anything that decides the matter.

---

## How to turn a score into an instruction

The scorecard is not a marking exercise. Each row you scored 0 or 1 is a sentence
that is missing from `skill.md`.

| You scored low on | The instruction that fixes it |
|---|---|
| 1 — answers the question | *"The client's questions are in the file, not the brief. Find them, list them, and answer each one explicitly."* |
| 2 — answer first | *"Section 1 is the answers. One short paragraph per question, each starting with yes, no, or a qualified version of one."* |
| 3 — anchoring | *"Quote a clause number or a dated document for every conclusion. If you cannot, label it an assumption."* |
| 5 — quantum | *"Never adopt the client's total. Take each head of loss in turn and say whether it is recoverable, reduced or excluded, and why."* |
| 6 — the other side | *"Before the recommendation, write a paragraph headed 'What the other side will say', at its strongest. If the recommendation does not survive it, change it."* |
| 8 — next steps | *"Numbered actions, each with an owner and a deadline. No action without both."* |
| 9 — assumptions | *"End with open points: what you assumed, what you did not see, and what would resolve each."* |
| 10 — fit | *"No more than 900 words. Section 1 must be readable on its own by a board member who reads nothing else."* |
| Invented facts | *"Do not state a date, figure or clause number that is not in a document you opened. If you need one you do not have, list it as an open point."* |

Do not paste all nine at once. **One at a time, re-run, re-score.** You are running
an experiment, and you cannot read an experiment with nine variables.

---

## A note on repeat runs

Two runs of the same skill file will not be identical — the model is not
deterministic. A one-point difference is noise. A four-point difference is your
instruction working. If you are unsure, run it again before you conclude anything.
