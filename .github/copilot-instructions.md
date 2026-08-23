# GitHub Copilot Instructions — ecos-substrate

This file gives GitHub Copilot (chat, code review, and the coding agent)
repo-specific context so its suggestions respect the conventions already
enforced by CI and documented in `AGENTS.md`. Read `AGENTS.md` in full
before proposing any change — this file summarizes the parts most relevant
to autocomplete/chat/review, not the full charter.

## What this repository is

`ecos-substrate` is a graph substrate for the Gr0ve ECOS knowledge base:
Markdown node files with YAML frontmatter under `entities/` and
`relationships/`, validated against `schema/schema.yaml`, on a path to a
future GraphRAG (embedding + community-graph) retrieval layer. See
`README.md` and `docs/GRAPH_CONVENTIONS.md` for the full picture.

## Hard rules to respect in any suggestion

1. **Frontmatter is mandatory.** Every `.md` file under `entities/` or
   `relationships/` (except `README.md`) must open with a YAML frontmatter
   block containing `type`, `title`, `description`, `tags`, `depends_on`,
   and `timestamp` — see `docs/GRAPH_CONVENTIONS.md`. Do not suggest a node
   file without it.
2. **`type` must already exist in `schema/schema.yaml`.** Never suggest an
   ad hoc `type:` value. If a concept doesn't fit an existing
   `entity_type`/`relation_type`, the correct move is to flag it as a
   schema proposal (see the `entity-proposal` issue template and the
   `council-consult` skill), not to invent a type inline.
3. **`depends_on` targets must resolve.** Every relative path listed in
   `depends_on` must point to a real file in the repo (checked by
   `scripts/validate_graph.py` in CI). Don't suggest a `depends_on` entry
   to a file that doesn't exist yet in the same PR.
4. **New `entities/<domain>/` directories need `_community.yaml`.** Copy
   `templates/_community.yaml.template` when introducing the first node in
   a new top-level domain.
5. **Schema changes are not content changes.** Adding/renaming/removing an
   `entity_type` or `relation_type` in `schema/schema.yaml`, or
   restructuring the community hierarchy, requires the `council-consult`
   skill (`skills/council-consult.skill.md`) and a human sign-off — never
   suggest merging this kind of change without that record present in the
   PR description (`### Council Consult:` block).
6. **Validate before suggesting a fix is complete.** The authoritative
   check is `python scripts/validate_graph.py`. If reasoning about whether
   a proposed node/edge is valid, reason as that script would (frontmatter
   completeness, declared type, resolvable `depends_on`).

## Review focus for Copilot code review

When reviewing a pull request, prioritize:
- Missing or malformed frontmatter fields.
- `type:` values not present in `schema/schema.yaml`.
- Dangling `depends_on` paths.
- Schema/convention changes (`schema/`, `SCHEMA_SPEC.md`,
  `docs/GRAPH_CONVENTIONS.md`) that lack a `### Council Consult:` block in
  the PR description — flag this explicitly rather than approving.
- Changes to `.github/workflows/wf-council.yaml` or `wf-audit.yaml` that
  would weaken or remove existing validation steps.

## What Copilot should NOT do

- Do not bypass `scripts/validate_graph.py` by editing the validator to
  make a bad node pass instead of fixing the node.
- Do not widen an existing `entity_type`'s meaning to avoid creating a new
  one — that's a council-consult decision, not an inline fix.
- Do not remove or rewrite `_community.yaml` files to "simplify" structure.
- Do not self-approve or suggest merging a schema-level change without a
  Council Consult record — `.github/CODEOWNERS` routes these to a human
  regardless of any automated review outcome.

## Related files

- `AGENTS.md` — full operating charter (read this first for anything
  beyond quick autocomplete).
- `docs/GRAPH_CONVENTIONS.md` — frontmatter/directory conventions.
- `schema/schema.yaml` — declared entity/relation/attribute types.
- `scripts/validate_graph.py` — authoritative validation logic.
- `skills/council-consult.skill.md` — required process for ambiguous or
  irreversible schema/structure changes.
- `agents/briefing.agent.md` — read-only PR summary agent; do not hand-write
  a substitute for its output.
