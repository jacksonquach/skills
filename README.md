# skills

Claude Code / Agent skills. Each top-level directory is one skill containing a `SKILL.md`
(YAML frontmatter + instructions) and any supporting scripts.

## Skills

- [`four-plane/`](four-plane/SKILL.md) — reorganize a messy project folder into a findable four-plane layout (MD/Dashboard/Inputs/Database+scripts, routing at top), safely: repoints code, verifies nothing breaks, never deletes content.
- [`kanboard/`](kanboard/SKILL.md) — interact with a self-hosted [Kanboard](https://github.com/kanboard/kanboard) instance over its JSON-RPC API (projects, tasks, columns, comments).

## Using a skill

Point Claude Code at this repo (e.g. clone into your skills/plugins path, or reference the
directory). Claude loads the `SKILL.md` and follows its instructions. Skills that talk to
external services read credentials from environment variables — see each skill's setup section.
