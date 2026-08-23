# AGENTS.md

Operating charter for AI agents (and the humans directing them) contributing
to `ecos-substrate`. This file governs any agent — Claude, Copilot, a custom
LLM pipeline, or a human pasting agent output — that creates or modifies
files in this repository.

## Scope

This charter applies to any change under:
- `entities/`, `relationships/`, `schema/`
- `docs/GRAPH_CONVENTIONS.md`, `SCHEMA_SPEC.md`
- `config/`, `scripts/`
- `skills/`, `agents/`, `.github/`

## Ground rules

1. **Read before you write.** Before proposing any node, relation, or schema
   change, read `SCHEMA_SPEC.md` (source of truth for definitions) and
   `docs/GRAPH_CONVENTIONS.md` (source of truth for file structure).
2. **Frontmatter is non-negotiable.** Every entity/relationship Markdown file
   MUST carry the YAML frontmatter block defined in
   `docs/GRAPH_CONVENTIONS.md` (`type`, `title`, `description`, `tags`,
   `depends_on`, `timestamp`).
3. **No dangling edges.** Any `depends_on` reference must resolve to a real
   file in the same PR or an already-merged one. Run
   `python scripts/validate_graph.py` locally before opening a PR — CI
   (`wf-audit.yaml`) re-runs it and will block merge on failure.
4. **New types are schema changes, not content changes.** Introducing a new
   `entity_type` or `relation_type` requires updating `schema/schema.yaml`
   *and* getting a human or council sign-off (see Council Consult below) —
   never invent an ad hoc `type:` value in a node file.
5. **Community hygiene.** If you add the first node in a new
   `entities/<domain>/` directory, add a `_community.yaml`
   (`templates/_community.yaml.template`) in the same PR.

## When to invoke Council Consult

Use the `council-consult` skill (`skills/council-consult.skill.md`) whenever
a change is ambiguous, irreversible, or cross-cutting:
- Proposing a new `entity_type` or `relation_type`.
- Renaming or removing an existing type that other nodes already reference.
- Restructuring the community hierarchy (moving/merging `entities/<domain>/`
  directories).
- Any change flagged `needs-council-review` by a human reviewer or by
  `wf-council.yaml`.

Routine content additions (a new node using an existing type, correctly
linked) do not require council consult.

## Briefing agent

Every PR that touches `entities/`, `relationships/`, or `schema/` gets an
automatically generated summary from the Briefing Agent
(`agents/briefing.agent.md`), posted as a PR comment by `wf-council.yaml`.
Do not hand-write a substitute summary — if the automated briefing is wrong
or incomplete, fix the inputs (frontmatter, commit messages), not the
briefing itself.

## Review and ownership

`.github/CODEOWNERS` routes reviews by path. Schema-level changes
(`schema/`, `SCHEMA_SPEC.md`, `docs/GRAPH_CONVENTIONS.md`) always require a
human owner's approval regardless of council or CI outcome — agents may
draft and propose, but may not self-merge schema changes.

## Failure modes to avoid

- Do not bypass `wf-audit.yaml` by editing the validator instead of the
  content.
- Do not silently widen an existing `entity_type`'s meaning to avoid
  creating a new one — flag it for council consult instead.
- Do not delete `_community.yaml` files to "simplify" — community structure
  changes are schema changes (see above).

## Related files

- `SCHEMA_SPEC.md` — prose schema definitions
- `schema/schema.yaml` — machine-readable schema seed
- `docs/GRAPH_CONVENTIONS.md` — node/frontmatter/directory conventions
- `skills/council-consult.skill.md` — multi-perspective review skill
- `agents/briefing.agent.md` — automated PR summary agent
- `.github/workflows/wf-council.yaml`, `.github/workflows/wf-audit.yaml`
