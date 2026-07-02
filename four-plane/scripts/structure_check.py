#!/usr/bin/env python3
"""structure_check.py — lint a project folder against the four-plane standard.

The standard decays silently when it lives only in prose; this makes it a tripwire.
Run it on demand, in an audit, or from a hook — it flags the failure modes that
actually cost people time hunting for files:

  FAIL  decoys      same-named files in two places (the "revised file is in the
                    OTHER folder" trap) — newer copy shown first
  FAIL  root        loose files / non-plane folders at the project root
  WARN  versions    dated/versioned siblings in active planes (v2, final, copy…)
                    — versions belong in Archive/, not next to the current file
  WARN  readme      missing README, or no find-it-fast table near the top
  WARN  empties     empty folders outside Archive/
  INFO  inbox       items waiting in the sanctioned drop zone (_inbox/, Inputs/inbox/)

Usage:  python3 structure_check.py <folder> [--max 20]
Exit:   0 = clean or warnings only · 1 = at least one FAIL

Stdlib only; works on macOS / Linux / Windows (OneDrive/Drive paths fine).
"""
import os
import re
import sys
import datetime
from collections import defaultdict
from pathlib import Path

PLANES = {"MD", "Dashboard", "Inputs", "Database", "scripts"}
OK_ROOT_DIRS = PLANES | {"Archive", "_inbox"}
OK_ROOT_FILES = {"README.md", "CLAUDE.md", "AGENTS.md", ".DS_Store", "Thumbs.db", "desktop.ini"}
LAUNCHER = re.compile(r"\.(command|bat|ps1|sh|desktop|lnk)$", re.I)
IDENTITY = re.compile(r"^(about-.*\.md|.+ Master\.(md|js)|.+\.code-workspace)$", re.I)
VERSION_SMELL = re.compile(r"(?i)(?:[ _-]v\d+(?=[ ._-]|$)|\(\d+\)|[ _-](final|copy|old)(?=[ ._-]|$)|[ _-]draft\d)")
# infra names that legitimately repeat everywhere — not decoys
INFRA = {"README.md", "_README.md", "index.md", "INDEX.md", "entry.md", "metadata.json",
         "notes.md", ".DS_Store", "Thumbs.db", "desktop.ini", "__init__.py"}
PRUNE_DIRS = {".git", "__pycache__", "node_modules", ".obsidian", ".claude"}
# app bundles are opaque units — never lint inside them (keep-bundles-intact rule)
BUNDLE_SUFFIXES = (".scriv", ".app", ".fcpbundle", ".drp", ".logicx", ".sparsebundle", ".photoslibrary")


def walk_files(base: Path, skip_top=()):
    """Yield files under base, pruning junk dirs and any top-level dir in skip_top."""
    for dirpath, dirnames, filenames in os.walk(base):
        rel = Path(dirpath).relative_to(base)
        if rel.parts and rel.parts[0] in skip_top:
            dirnames[:] = []
            continue
        dirnames[:] = [d for d in dirnames if d not in PRUNE_DIRS and not d.startswith(".") and not d.lower().endswith(BUNDLE_SUFFIXES)]
        for f in filenames:
            yield Path(dirpath) / f


def day(p: Path) -> str:
    try:
        return datetime.date.fromtimestamp(p.stat().st_mtime).isoformat()
    except OSError:
        return "?"


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    cap = 20
    if "--max" in sys.argv:
        cap = int(sys.argv[sys.argv.index("--max") + 1])
    if not args:
        print(__doc__)
        return 0
    base = Path(args[0]).expanduser().resolve()
    if not base.is_dir():
        print(f"not a folder: {base}")
        return 1

    fails, warns, infos = [], [], []

    # ---- root: routing/identity only -------------------------------------
    launchers = 0
    for e in sorted(base.iterdir()):
        if e.name.startswith("."):
            continue
        if e.is_dir():
            if e.name not in OK_ROOT_DIRS:
                # fractal rule: a dir that is itself a project (own routing/planes/.claude)
                # is a sub-project, not clutter — lint it separately, recursively
                marks = ("README.md", "CLAUDE.md", "AGENTS.md", ".claude") + tuple(PLANES)
                if any((e / m).exists() for m in marks):
                    infos.append(f"sub-project: `{e.name}/` — a project of its own; lint it separately (fractal rule)")
                else:
                    fails.append(f"root: folder `{e.name}/` is not a plane — route it (or it becomes the next junk drawer)")
        else:
            if LAUNCHER.search(e.name):
                launchers += 1
                continue
            if e.name in OK_ROOT_FILES or IDENTITY.match(e.name):
                continue
            fails.append(f"root: loose file `{e.name}` — every file lives on a plane, root is routing only")
    if launchers > 2:
        warns.append(f"root: {launchers} launchers — one obvious entry point, two max")
    if not any((base / p).is_dir() for p in PLANES):
        warns.append("no plane folders exist yet — this folder hasn't been organized (run the four-plane reorg)")

    # ---- decoys: same basename, different homes (MD + Dashboard) ---------
    homes = defaultdict(list)
    for plane in ("MD", "Dashboard"):
        pd = base / plane
        if pd.is_dir():
            for f in walk_files(pd, skip_top=("templates",)):
                if f.name not in INFRA:
                    homes[f.name].append(f)
    for name, paths in sorted(homes.items()):
        parents = {p.parent for p in paths}
        if len(parents) > 1:
            newest = sorted(paths, key=lambda p: p.stat().st_mtime, reverse=True)
            where = "  ⟷  ".join(f"{p.parent.relative_to(base)} ({day(p)})" for p in newest[:3])
            fails.append(f"decoy: `{name}` ×{len(paths)} — {where} — one canonical home; merge or name the winner in README")

    # ---- version smell in active planes ----------------------------------
    for plane in ("MD", "Dashboard"):
        pd = base / plane
        if pd.is_dir():
            for f in walk_files(pd):
                if VERSION_SMELL.search(f.stem):
                    warns.append(f"version-suffix: `{f.relative_to(base)}` — current file keeps the stable name; old versions go to Archive/")

    # ---- README + find-it-fast table --------------------------------------
    readme = base / "README.md"
    if not readme.is_file():
        fails.append("no README.md — nothing answers 'where is X?'")
    else:
        head = readme.read_text(encoding="utf-8", errors="replace").splitlines()[:25]
        if not any("|" in ln for ln in head):
            warns.append("README: no find-it-fast table in the first 25 lines — the answer to 'where's the latest?' goes first")

    # ---- empty dirs outside Archive ---------------------------------------
    for dirpath, dirnames, filenames in os.walk(base):
        rel = Path(dirpath).relative_to(base)
        if rel.parts and (rel.parts[0] in {"Archive"} | PRUNE_DIRS or rel.parts[0].startswith(".")):
            dirnames[:] = []
            continue
        dirnames[:] = [d for d in dirnames if d not in PRUNE_DIRS and not d.startswith(".") and not d.lower().endswith(BUNDLE_SUFFIXES)]
        if not dirnames and not filenames and rel.parts:
            warns.append(f"empty folder: `{rel}/` — archive it to Archive/_empty-folders/ or fill it")

    # ---- inbox backlog -----------------------------------------------------
    for ib in (base / "_inbox", base / "Inputs" / "inbox"):
        if ib.is_dir():
            n = sum(1 for _ in ib.iterdir())
            if n:
                infos.append(f"inbox: {n} item(s) in `{ib.relative_to(base)}/` waiting for triage")

    # ---- report ------------------------------------------------------------
    print(f"four-plane structure check — {base.name}/")
    shown = 0
    for tag, bucket in (("FAIL", fails), ("WARN", warns), ("INFO", infos)):
        for line in bucket:
            if shown >= cap:
                print(f"  … +{len(fails) + len(warns) + len(infos) - cap} more (raise --max)")
                print(f"RESULT: {len(fails)} fail · {len(warns)} warn · {len(infos)} info")
                return 1 if fails else 0
            print(f"  [{tag}] {line}")
            shown += 1
    if not (fails or warns or infos):
        print("  clean — one obvious path to everything ✓")
    print(f"RESULT: {len(fails)} fail · {len(warns)} warn · {len(infos)} info")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
