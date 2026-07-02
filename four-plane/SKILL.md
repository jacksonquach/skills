---
name: four-plane
description: Organize any project folder so anything is findable in one obvious step — four planes (MD/Dashboard/Inputs/Database+scripts), routing at top, one canonical home per thing, and a bundled linter (scripts/structure_check.py) that catches decay before it costs anyone a night of hunting. Trigger on "I can't find X", "where is/was the file", "reorganize this folder", "clean up this project", "make this easier to navigate", "/four-plane <path>", or to check a folder with "lint the structure".
---

# Four-Plane

**Version:** 2.0 · Fable · 2026-07-02 *(v1: Opus 4.8, same day — v2 is the post-mortem
rewrite after v1's standard failed in the field: a night lost hunting a revised file that
sat in a sibling folder under the same name. Every v2 addition traces to a real failure.)*

The point, in one line (after Steve Krug): **don't make me think.** Anything a person wants
must be reachable in ≤2 clicks from the folder's README, named plainly. If finding a file
requires memory, search, or choosing between two similar-looking things, the *structure*
failed — fix the structure, not the person's search habits.

The acceptance test: **the 11pm test.** Could the folder's owner, tired at 11pm, find the
latest revised version of anything without opening a single wrong folder?

## The four planes

```
<project>/
├── README.md            # FIRST section = find-it-fast table ("You want X → it's here")
├── <identity files>      # CLAUDE.md/AGENTS.md, config, at most 1–2 entry-point launchers
├── MD/                   # the DESK — all readable/editable working content
├── Dashboard/            # the WALL — rendered things you open and read (reports, compiled outputs, views)
├── Inputs/                # the FILE CABINET — raw immutable sources; cite, never edit
│   └── inbox/             # the DOORMAT — the ONE sanctioned drop zone (see law 5)
└── Database/ + scripts/   # the MACHINE SHOP — derived data + the code that turns MD+Inputs into Dashboard
```

Omit a plane rather than create it empty. Root is routing only — if you can't say in one
word why a file sits at the root, it belongs on a plane.

## The six laws (v2 — each one bought with a real failure)

1. **Routing at top.** README's first section is a find-it-fast table; below the fold is
   optional. A launcher (`Start X.command` / `.bat`) may sit at root — one obvious entry
   point, two max.
2. **One plane per file, no plane aliases.** Exactly one folder plays each role. A legacy
   `sources/` living next to `Inputs/` means raw files have two homes — that *is* the decoy
   trap, just one level up. Fold aliases in; don't tolerate them as "grandfathered."
3. **One canonical home per thing — and revisions go home.** The failure that motivated v2:
   revised work parked in a working folder (`notes/…`) while the canonical location
   (`story-bible/…`) kept stale files under the *same names*. Work-in-progress may fork;
   **the session that finishes it must merge it back to the canonical home before ending.**
   If a fork must persist, the README names which copy is canonical — silence is a trap.
4. **Stable names; versions to Archive.** The current file keeps the plain stable name
   (`report.md`, not `report-v3-final.md`); superseded versions move to `Archive/` (dated),
   never sit as siblings. Dated *notes* are fine; dated *artifacts pretending to be current*
   are not. Never delete — archive with origin preserved (`Archive/_empty-folders/<origin>`
   for emptied husks).
5. **Entropy gets a doormat, not a doorway.** People drop files somewhere no matter what —
   sanction ONE drop zone (`Inputs/inbox/` or root `_inbox/`) and make triage-to-planes a
   routine step. Otherwise the root becomes the de facto inbox and law 1 dies quietly.
6. **Structure is fractal.** A folder inside a project that grows its own machinery/outputs
   becomes a *sub-project*: it gets its own routing + planes inside, and moves as a whole
   unit. (v1's blind spot: the standard governed the top level while a workspace below it
   rotted — rules that don't recurse leave exactly one ungoverned level, and that's where
   the mess moves.)

## Enforcement — the standard is executable

Prose standards decay silently; nobody notices drift until someone loses a night to it.
So the standard ships as a linter:

```bash
python3 scripts/structure_check.py <folder>        # exit 0 clean · 1 FAIL findings
```

It flags: same-named files in two homes (decoys, newest first with dates), loose files and
non-plane folders at root, version-suffix siblings in active planes, missing find-it-fast
table, empty folders outside Archive, and inbox backlog. Sub-projects (fractal rule) and
app bundles (`.scriv`, `.app`, …) are respected, not flagged. Run it after any reorg, on
new-project creation, or from a scheduled audit — **the tripwire, not discipline, is what
keeps the shape.**

## When to run a reorg (and when not to)

Reorganize on **pain** (someone couldn't find a thing), on **creation** (new project starts
on the standard — cheapest possible time), or on a **linter FAIL**. Do *not* reorganize
recreationally: a working folder that passes the 11pm test stays as it is, and a reorg that
breaks a pipeline is worse than clutter.

## The safe reorg procedure (proven; unchanged from v1)

0. **Pre-flight:** if another process/editor/agent session is live in the folder, defer or
   coordinate — bulk moves under live edits corrupt work.
1. **Map every dependency before moving anything:** grep code, launchers, configs, commands,
   and content citations for paths that will change. Build the full repoint list first.
2. **Classify every file into exactly one plane.** For lookalikes: mtime + size + content
   head before judging; hash-compare before calling anything a "dup" (`_v2` files are usually
   distinct). **Never silently pick winners, merge, or delete — ambiguity goes back to the human.**
3. **Move by renaming whole folders where possible** (`mv sources Inputs` beats file-by-file).
   Bundles move whole. Never move an open file (lock/swap siblings → skip + flag).
4. **Archive, never delete.** Reorg-emptied folders → `Archive/_empty-folders/<origin>`;
   never recursive-sweep (it eats VCS internals, caches, and intentional drop zones).
5. **Repoint everything from step 1 in the same pass** — script constants, config refs, UI
   strings, launcher commands, citations. Grep for residuals until zero.
6. **Verify, don't assume:** run the build, start the server, open the output, check logs
   clean, screenshot. Then run the linter.
7. **Rewrite routing last:** find-it-fast table first; name the canonical copy of anything
   that still exists twice.
8. **Report:** what moved, what got repointed, what's flagged for a human call.

## Archetype cautions

| Folder type | Watch for |
|---|---|
| Pipeline (build/data) | script OUT-paths; copy-based mirrors (drop them); test server endpoints after |
| Creative / knowledge | apps that read content by path (repoint their ROOT); never guess which draft supersedes; bundles stay whole |
| Records / sensitive | baked vs. loader dashboards; privacy — don't resurface sensitive files in a README; append-only files stay put |
| Generic | route purely by file role → plane |

## Output

A process skill: produces the reorganized folder, a clean linter run, and a short report
(moved / repointed / flagged). Log the reorg in the host project's changelog convention if
one exists; otherwise the chat summary is the record.
