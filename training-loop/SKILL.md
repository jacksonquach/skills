---
name: training-loop
description: Turn ad hoc work into compounding AI capability — postmortem every significant task, graduate repeated patterns into playbooks, graduate rule-ready playbooks into skills, and make every skill run write back to its playbook. Trigger on "postmortem this", "log what we learned", "that task is done" (after >1 hr of work), "should this be a skill?", "capture how we did this", or "/training-loop".
---

# Training Loop

AI is a new employee. You don't train an employee by handing them the final deliverable —
they shadow you. They see the pre, the during, the post, and the reasoning between versions.
This skill is the shadowing system: a loop that turns finished tasks into training data, data
into playbooks, and playbooks into skills the AI runs itself.

Read it as: **postmortems are fuel, playbooks are memory, skills are muscle.**

```
[Do the task]
     │
     ▼
[Postmortem: pre / during / post + deltas + thread]
     │
     ▼
[Pattern shows up 2–3 times] ──► Playbook page (principle + decision tree)
     │
     ▼
[Confidence ≥ 4] ──► Skill package (AI runs it)
     │
     ▼
[Skill runs] ──► output + updated playbook (write-back)
```

## The three rules

1. **Postmortem before done.** Every significant task (>1 hr) closes with a postmortem —
   the artifact, the deltas (what changed between versions and *why*), and the thread
   (chat/voice/notes), **linked, not rewritten**. The final version alone is useless as
   training data; the thinking lives in the deltas and the thread.
2. **Graduation is earned, not declared.** A pattern seen in 2–3 postmortems at confidence
   ≥3 becomes a playbook page. Confidence ≥4 becomes a skill. The AI flags candidates; the
   human approves. Nothing graduates on vibes.
3. **Write-back.** Every skill run updates its parent playbook — run count, what worked,
   what broke, any rule that needed a human override. A skill that runs silently breaks the
   loop: the system stops learning exactly when it starts executing.

## The repeatability rubric (score every postmortem 1–5)

| Score | Meaning | Action |
|-------|---------|--------|
| 1 | One-off, unique context | Archive the postmortem, move on |
| 2 | Might repeat, context shifts too much | Playbook *principle* only, no skill |
| 3 | Repeatable but needs human judgment | Playbook page + checklist |
| 4 | Clear decision tree, minimal ambiguity | **Build the skill** |
| 5 | Bulletproof, zero human needed | **Fully automate** (schedule it) |

**Not a skill:** anything requiring taste or judgment mid-task. That stays a playbook page
until the judgment can be written as an if/then rule. A playbook's "judgment calls still
needed" list emptying is the graduation signal.

## Where things live

Keep the *learning* in one place, separate from the *work*:

```
<your governance / meta folder>/
├── POSTMORTEMS/    one file per task: <YYYY-MM-DD>-<task-slug>.md (date-first = chronological)
├── Playbooks/      one page per pattern: <domain>-<pattern>.md
└── <skills dir>/   graduated skills, in whatever format your agent runner loads
```

Task outputs stay in their project folders; only the learning lives here. One brain, many
limbs. (If you also use the `four-plane` skill: the loop is the four planes put on a time
axis — recordings = sources, postmortems + playbooks = knowledge, skills = machinery.)

## The postmortem template (5–15 minutes; voice-record first, then fill)

```markdown
---
date: YYYY-MM-DD
task: "<short name>"
domain: "<project/area>"
score:            # 1–5 rubric above
status: logged    # logged → playbook-drafted → graduated
---

## PRE — What triggered this?
- Input state / question / success criteria / assumptions going in

## DURING — What did you actually do?
- Approach chosen, and why
- Key decision points (2–3): picked what, rejected what, why ("tried X, Y happened, switched to Z")
- Versions / deltas: v1 → v2: … · v2 → v3: …
- Thread link (chat/session) · voice link (recording + transcript)

## POST — What came out?
- Final deliverable · met criteria? · surprises · next time, do differently

## PATTERN EXTRACTION
- Repeatable? · confidence (1–5) · minimum context an AI needs to run this alone
- Trigger rule: when should this fire automatically? ("day 2 of close, variance > 5%")
```

Rule of thumb: **the postmortem is the map; the deltas and threads are the territory.
Link, don't rewrite.** Capturing "moved the reveal earlier because pacing sagged" is the
training data — "shots moved" is not.

## Keeping an index

Maintain one running index file: a log table (date · task · score · playbook? · skill?) and
a graduation-candidates table the AI updates and the human reviews. The bottleneck is never
tooling — it's postmortem count. Don't build playbook/skill shelves before the fuel exists.

## Related

- Pairs with `four-plane/`: four-plane governs **space** (where things live so anything is
  findable in one step); training-loop governs **time** (how the system learns from what you
  do there).
