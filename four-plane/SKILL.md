---
name: four-plane
description: Reorganize a messy project folder into a findable four-plane layout (MD/Dashboard/Inputs/Database+scripts, routing at top), safely — repointing code, verifying nothing breaks, and never deleting content. Trigger on "I can't find X", "where is/was the file", "reorganize this folder", "clean up this project", "make this easier to navigate", or "/four-plane <path>".
---

# Four-Plane

A repeatable, safe procedure for taking any project folder from "I opened folder after folder
and never found it" to "one obvious path to everything." Named for the four functional planes
every project folder gets sorted into.

The standard it enforces, borrowed from Steve Krug's *Don't Make Me Think*: **anything the user
wants should be reachable in ≤2 clicks from the folder's README, named plainly.** If finding a
file requires memory, search, or guessing between two similarly-named things, the structure
failed — fix the structure, not the user's search skills.

## When to use this skill

- Someone says they couldn't find a file, or had to open several folders to locate something.
- A project folder has accumulated loose files at the root, duplicate-looking subfolders, or
  stale copies sitting next to current ones.
- Before shipping a new project structure — apply this as the standard, not just the fix.

## The target layout

```
<project>/
├── README.md          # find-it-fast table FIRST, then everything else
├── <identity files>    # CLAUDE.md / config / at most 1-2 entry-point launchers
├── MD/                 # ALL readable/editable content — notes, docs, source material being worked on
├── Dashboard/          # rendered, OPEN-and-READ artifacts — compiled outputs, reports, generated views
├── Inputs/              # raw, immutable sources — never edited, only cited/read
└── Database/ + scripts/ # machinery — derived data + the code that generates Dashboard/ from MD/+Inputs/
```

Omit a plane rather than create it empty. Root holds only routing/identity — if you can't say
in one word why a file is at the root, it belongs on a plane.

**Detect the project's archetype and adapt:**

| Archetype | Signals | Special handling |
|---|---|---|
| **Pipeline** (data/build project) | a `serve.py`/build script, generated outputs, config-driven generators | repoint script OUTPUT paths; drop any `copy`-based mirroring step; test the server/build after (hit endpoints, check exit code) |
| **Creative / knowledge** (writing, research, wikis) | content bundles, big note collections, versioned drafts (`v2`, `v3`) | **keep self-contained project bundles intact — don't flatten them**; never guess which draft supersedes another |
| **Records / tracking** (logs, structured data, sensitive info) | append-only files, baked/self-contained dashboards, PII or other sensitive content | verify dashboards are self-contained (don't introduce a broken loader); be privacy-aware about what gets surfaced where; leave append-only files alone |
| **Generic** | none of the above | route purely by file role → plane |

## The safety-first procedure

Each step below exists because skipping it caused a real problem in practice at some point.
Don't skip them.

0. **Pre-flight: check for concurrent work.** If another process, editor, or agent session has
   the target folder open, defer or coordinate first — bulk moves under live edits corrupt work.
1. **Map every dependency before moving anything.** Grep code, launcher scripts, config files,
   and any content that cites internal paths (frontmatter, includes, relative links). Build the
   full list of things that will need repointing — don't discover them one broken run at a time.
2. **Classify every file into exactly one plane.** For anything that looks like a duplicate:
   check mtime, size, and content head before deciding — `_v2`/`_v3`/`(1)` suffixes are usually
   *distinct* documents, not duplicates. Hash-compare (`sha256`) before ever calling two files
   "the same." **Never silently pick a winner or delete content on a guess** — if it's ambiguous,
   flag it for the human instead of resolving it yourself.
3. **Move by renaming whole folders where possible** (`mv sources Inputs` beats moving file by
   file). Keep self-contained project bundles as units. Never move a file that's currently open
   (check for lock files / editor swap files first — skip and flag instead).
4. **Archive emptied folders, never delete.** Anything the reorg itself emptied goes to an
   `Archive/_empty-folders/<original path>` location, preserving where it came from. Only archive
   folders *this reorg* emptied — never recursively sweep everything (that catches version
   control internals, caches, and intentional empty drop-zones you didn't mean to touch).
5. **Repoint every dependency found in step 1, in the same pass as the move.** Script path
   constants, config file references, UI strings, launcher commands, content citations — all of
   it, right away. If you move the artifact but not its generator's output path, the next run
   just recreates the old mess.
6. **Verify — don't assume.** Run the build. Start the server. Open the generated output. Check
   logs/console are clean. If any moved HTML/config has a relative loader path (`src=`, `href=`,
   `fetch(...)` to a local file), confirm it still resolves or fix it.
7. **Rewrite the routing docs last.** The README's find-it-fast table goes first, above the fold.
   If two things share a name or purpose, the README must say which one is canonical — don't
   leave that ambiguity for the next person to rediscover.
8. **Report what moved and what's still a judgment call.** Anything ambiguous (which draft is
   current, whether to merge two near-duplicate sources) goes back to the human — don't decide
   silently on their behalf.

## Output

This is a process skill with no single artifact — it produces a reorganized folder plus a short
report of what moved, what got repointed, and what's flagged for a human decision. If the host
project has its own changelog/update-log convention, log the reorg there; otherwise a short
summary in the chat response is enough.
