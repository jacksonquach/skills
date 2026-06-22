# jaxonius/skills — Build & Handoff Guide

> **Purpose of this repo:** a personal collection of AI agent *skills*. The first (and currently only) entry is the **[obsidian-wiki](https://github.com/Ar9av/obsidian-wiki)** framework, added as a git submodule. Installing it copies 34 markdown "wiki-*" skills into your AI agents (Claude Code, etc.) so you can build and maintain an Obsidian knowledge base from inside any agent.
>
> This document is the **runbook**: how everything is wired, how to rebuild it from scratch on a fresh machine, the Windows/OneDrive gotchas we hit, and how to maintain and extend it. If you're picking this up cold, read "Current state" then "Rebuild from scratch."

---

## 1. Current state (what exists right now)

| Thing | Location | Notes |
|---|---|---|
| **This repo** (`jaxonius/skills`) | `…\OneDrive - TPx Communications\Git Pull\sandbox\skills\` | Git remote: `https://github.com/jaxonius/skills.git`, branch `main`. Lives inside the `Git Pull` working tree under `sandbox/` (which is untracked by Git-Pull — see gotcha #5). |
| **obsidian-wiki** (submodule) | `…\sandbox\skills\obsidian-wiki\` | Pinned to upstream `Ar9av/obsidian-wiki` commit `306c0c9` (tag `v2026.06.2`). |
| **Python** | `C:\Users\<USER>\AppData\Local\Programs\Python\Python312\python.exe` | 3.12.10, installed via winget. **Not on PATH** — invoke via full path or `py`. |
| **obsidian-wiki package** | editable install (`pip install -e`) pointing at the submodule | Run as `python -m obsidian_wiki` (the `.exe` shim is blocked — gotcha #2). |
| **Config** | `C:\Users\<USER>\.obsidian-wiki\config` | Written by `setup`. Stores skills path, bootstrap path, vault path. |
| **Installed skills** | `C:\Users\<USER>\.claude\skills\` (+ 11 other agent dirs) | 34 real skill folders, each with `SKILL.md`. **This is what Claude Code actually loads** — independent of the repo location. |
| **Obsidian vault** | `…\OneDrive - TPx Communications\ObsidianVault\` | Currently empty. Open it in Obsidian; run the `wiki-setup` skill to initialize structure. |

**One-line mental model:** the repo/submodule is the *source*; `pip install -e` + `setup` *copy* the skills into `~/.claude/skills/`; Claude Code reads them from there.

---

## 2. Prerequisites

- **Windows 10/11**, PowerShell, and **Git for Windows** (with the system credential manager configured — this is the default, and it's how pushes to GitHub authenticate; no `gh` CLI is required).
- A GitHub account with push access to `github.com/jaxonius/skills` (credentials are cached by Git Credential Manager the first time you push).
- **Python 3.9+** (we use 3.12). The steps below install it.
- Optional: **Obsidian** desktop app to view the vault.

---

## 3. Rebuild from scratch (fresh machine)

All commands are PowerShell. Replace `<USER>` with the Windows username. Set `$py` once per shell.

> ⚠️ Before running the CLI, **always** set `$env:PYTHONUTF8 = "1"` (gotcha #1).

### Step 1 — Install Python
```powershell
winget install -e --id Python.Python.3.12 --accept-source-agreements --accept-package-agreements --silent
# Verify (use the full path; PATH won't refresh in the current shell):
$py = "C:\Users\<USER>\AppData\Local\Programs\Python\Python312\python.exe"
& $py --version           # -> Python 3.12.x
& $py -m pip --version
```

### Step 2 — Clone this repo + its submodule
```powershell
cd "C:\Users\<USER>\OneDrive - TPx Communications\Git Pull\sandbox"
git clone https://github.com/jaxonius/skills.git
cd skills
git submodule update --init --recursive   # pulls obsidian-wiki at the pinned commit
```
If you're recreating the repo from nothing (it didn't exist yet), instead do:
```powershell
git clone https://github.com/jaxonius/skills.git ; cd skills
git submodule add https://github.com/Ar9av/obsidian-wiki.git obsidian-wiki
git submodule update --init --recursive
git add .gitmodules obsidian-wiki
git commit -m "Add Ar9av/obsidian-wiki as submodule"
git branch -M main
git push -u origin main
```

### Step 3 — Install the obsidian-wiki package (editable)
```powershell
$py = "C:\Users\<USER>\AppData\Local\Programs\Python\Python312\python.exe"
& $py -m pip install --disable-pip-version-check -e "C:\Users\<USER>\OneDrive - TPx Communications\Git Pull\sandbox\skills\obsidian-wiki"
& $py -m obsidian_wiki --version          # -> obsidian-wiki 2026.6.x
```
(Ignore the "script obsidian-wiki.exe is not on PATH" warning — we never use the shim.)

### Step 4 — Run setup (installs skills into your agents)
```powershell
$env:PYTHONUTF8 = "1"
$py = "C:\Users\<USER>\AppData\Local\Programs\Python\Python312\python.exe"
$vault = "C:\Users\<USER>\OneDrive - TPx Communications\ObsidianVault"
if (-not (Test-Path $vault)) { New-Item -ItemType Directory -Path $vault | Out-Null }
& $py -m obsidian_wiki setup --vault $vault
```
> **Do NOT add `--project` / `--copy --project`** on Windows. The repo's project-local bootstrap uses POSIX symlinks that don't materialize when `git core.symlinks=false`, so that step fails on a missing `AGENTS.md` and dirties the submodule (gotcha #3/#4). The plain `setup --vault` does the global install into `~/.claude/skills/` etc., which is all you need.

### Step 5 — Verify
```powershell
$env:PYTHONUTF8 = "1"
& $py -m obsidian_wiki info
```
Expect: 34 bundled skills, and every agent line shows `34/34` (Claude Code, Gemini, Codex, …). Then:
```powershell
(Get-ChildItem "C:\Users\<USER>\.claude\skills" -Directory | Where-Object { Test-Path (Join-Path $_.FullName 'SKILL.md') }).Count   # -> 34
```
In Claude Code, reload the session — the `wiki-*` skills now appear under `/`.

---

## 4. Windows / OneDrive gotchas (the stuff that bit us)

1. **Unicode banner crashes the CLI.** `setup`/`info` print box-drawing characters; the Windows cp1252 console raises `UnicodeEncodeError` and the command exits non-zero **even though the work completed**. Always set `$env:PYTHONUTF8 = "1"` first. If you still see a traceback, run `info` afterward to confirm the real outcome.
2. **The `.exe` shim is blocked.** `…\Python312\Scripts\obsidian-wiki.exe` returns "Access is denied" (AV/OneDrive), and `Scripts\` isn't on PATH anyway. **Always invoke `python -m obsidian_wiki`.**
3. **Symlinks don't check out.** The repo commits symlinks (agent skill mirrors, `CLAUDE.md`→`AGENTS.md`, etc.). With `git core.symlinks=false` (default without Developer Mode) they land as tiny text stubs and `AGENTS.md` may be missing — which is why `--project` setup fails. Stick to the global install.
4. **OneDrive locks block `git clean`.** If the submodule ever gets dirtied (e.g. someone ran `--copy --project`), `git checkout/clean` fails with "Permission denied" on the copied skill dirs. Fix:
   ```powershell
   cd "…\sandbox\skills\obsidian-wiki"
   foreach ($d in @('.agents\skills','.claude\skills','.cursor\skills','.kiro\skills','.pi\skills','.windsurf\skills')) {
     $p = Join-Path (Get-Location) $d; if (Test-Path $p) { Remove-Item $p -Recurse -Force }
   }
   git checkout --force -- .
   git status --short   # should be empty
   ```
5. **The repo is nested inside `Git Pull`.** `sandbox/` is untracked by the outer `Git Pull` repo, so the embedded `skills` repo is harmless — **but do not `git add sandbox/` in Git-Pull**, or it'll try to embed this repo. They are two separate repos that happen to be nested.
6. **Moving the repo breaks the install paths.** The editable install (`_editable_impl_obsidian_wiki.pth`) and `~/.obsidian-wiki/config` store absolute paths. If you relocate `skills\`, re-run Step 3 (`pip install -e <newpath>`) and Step 4 (`setup --vault`) to repoint them.

---

## 5. Day-to-day usage

- **Use the skills:** in any Claude Code session, the `wiki-*` skills trigger by description (e.g. "set up my wiki", "ingest this folder", "what do I know about X"). The backing Python CLI is `python -m obsidian_wiki`.
- **Initialize the vault:** run the `wiki-setup` skill (or ask Claude to) to scaffold the empty `ObsidianVault`.
- **View it:** open `ObsidianVault` in Obsidian (File → Open Vault).

## 6. Maintenance

- **Update obsidian-wiki to the latest upstream:**
  ```powershell
  cd "…\sandbox\skills\obsidian-wiki"
  git fetch origin && git checkout origin/main
  cd .. ; git add obsidian-wiki ; git commit -m "Bump obsidian-wiki submodule" ; git push
  & $py -m pip install --disable-pip-version-check -e .\obsidian-wiki   # rebuild package
  $env:PYTHONUTF8="1"; & $py -m obsidian_wiki setup --vault "…\ObsidianVault"   # reinstall skills
  ```
- **Re-install skills after an agent reset:** just re-run Step 4.

## 7. Extending — adding another skill source

Same submodule pattern keeps the collection clean and upstream-linked:
```powershell
cd "…\sandbox\skills"
git submodule add <repo-url> <folder-name>
git add .gitmodules <folder-name> ; git commit -m "Add <name>" ; git push
```
Then install that source however its README specifies (and prefer global/`--copy` installs on Windows to dodge the symlink issue).

## 8. The 34 skills installed

`claude-history-ingest`, `codex-history-ingest`, `copilot-history-ingest`, `cross-linker`, `daily-update`, `graph-colorize`, `hermes-history-ingest`, `impl-validator`, `llm-wiki`, `memory-bridge`, `openclaw-history-ingest`, `pi-history-ingest`, `skill-creator`, `tag-taxonomy`, `wiki-agent`, `wiki-capture`, `wiki-context-pack`, `wiki-dashboard`, `wiki-dedup`, `wiki-digest`, `wiki-export`, `wiki-history-ingest`, `wiki-import`, `wiki-ingest`, `wiki-lint`, `wiki-query`, `wiki-rebuild`, `wiki-research`, `wiki-setup`, `wiki-stage-commit`, `wiki-status`, `wiki-switch`, `wiki-synthesize`, `wiki-update`.

The canonical definitions live in `obsidian-wiki/.skills/<name>/SKILL.md`.

---

## 9. Quick reference

```powershell
# Standard preamble for any obsidian-wiki command on Windows:
$env:PYTHONUTF8 = "1"
$py = "C:\Users\<USER>\AppData\Local\Programs\Python\Python312\python.exe"

& $py -m obsidian_wiki info                 # status: paths, counts, per-agent install
& $py -m obsidian_wiki list                 # list bundled skills
& $py -m obsidian_wiki setup --vault <path> # (re)install skills globally
```

- Repo: `https://github.com/jaxonius/skills` · Upstream: `https://github.com/Ar9av/obsidian-wiki`
- Session transcript of the original build: `sandbox/claude-session_2026-06-22_obsidian-wiki-setup.md`
- Transcript converter: `sandbox/_jsonl_to_md.py`
