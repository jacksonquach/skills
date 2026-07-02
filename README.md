# skills

Claude Code / Agent skills. Each top-level directory is one skill containing a `SKILL.md`
(YAML frontmatter + instructions) and any supporting scripts.

## Skills

- [`four-plane/`](four-plane/SKILL.md) — organize any project folder so anything is findable in one obvious step: four planes (MD/Dashboard/Inputs/Database+scripts), routing at top, one canonical home per thing, plus a bundled structure linter (`scripts/structure_check.py`) that catches decay. v2 (Fable).
- [`kanboard/`](kanboard/SKILL.md) — interact with a self-hosted [Kanboard](https://github.com/kanboard/kanboard) instance over its JSON-RPC API (projects, tasks, columns, comments).
- [`training-loop/`](training-loop/SKILL.md) — turn ad hoc work into compounding AI capability: postmortem every significant task, graduate repeated patterns into playbooks, graduate rule-ready playbooks into skills, write back every run. v1 (Fable).

## Using a skill

Point Claude Code at this repo (e.g. clone into your skills/plugins path, or reference the
directory). Claude loads the `SKILL.md` and follows its instructions. Skills that talk to
external services read credentials from environment variables — see each skill's setup section.
