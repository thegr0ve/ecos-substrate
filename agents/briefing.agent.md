---
name: briefing-agent
description: >
  Generates a concise, structured summary of graph-substrate changes in a
  pull request — new/changed entities, relationships, and schema types —
  and posts it as a PR comment. Triggered by wf-council.yaml on PRs that
  touch entities/, relationships/, or schema/.
version: "0.1.0"
---

# Agent: Briefing Agent

## Purpose

Give reviewers a single, consistent summary of what a PR changes in the
graph substrate, without requiring them to reconstruct it from a raw diff.
The briefing agent does not approve, block, or modify a PR — it only
reports.

## Inputs

- The PR diff, scoped to `entities/`, `relationships/`, `schema/`,
  `docs/GRAPH_CONVENTIONS.md`, `SCHEMA_SPEC.md`.
- Frontmatter (`type`, `title`, `description`, `tags`, `depends_on`) parsed
  from every added or modified `.md` file under `entities/` and
  `relationships/`.
- The output of `scripts/validate_graph.py`, if it has already run in CI.
- Any Council Consult record attached to the PR or issue (see
  `skills/council-consult.skill.md`), if present.

## Procedure

1. **Classify the diff** into: new entities, modified entities, new
   relationships, schema changes (`schema/schema.yaml`,
   `SCHEMA_SPEC.md`), convention changes (`docs/GRAPH_CONVENTIONS.md`),
   and other (CI, docs, config).
2. **For each new or modified node**, extract `type` and `title` from
   frontmatter and note any new `depends_on` edges it introduces.
3. **Flag risk signals**, if present:
   - A node whose `type` is not yet declared in `schema/schema.yaml`.
   - A `depends_on` target that does not exist in the PR or `main`.
   - A schema-level change (`schema/schema.yaml`, `SCHEMA_SPEC.md`)
     without an attached Council Consult record.
   - A new top-level `entities/<domain>/` directory missing
     `_community.yaml`.
4. **Include the Council Consult synthesis line**, verbatim, if the PR or
   its linked issue contains one.
5. **Post the briefing** as a single PR comment using the template below.
   Update the same comment on subsequent pushes rather than posting a new
   one each time.

## Output template

```
## Graph Substrate Briefing

**New entities:** <count> — <type: title, ...>
**Modified entities:** <count>
**New relationships:** <count>
**Schema changes:** <yes/no — files touched>
**Convention changes:** <yes/no>

**Risk flags:**
- <flag, or "none">

**Council Consult:** <synthesis line, or "not required for this change">

**Validator:** <pass/fail from scripts/validate_graph.py, or "not yet run">
```

## Boundaries

- Never edits repository content — read-only over the diff and repo state.
- Never overrides `scripts/validate_graph.py` or CI status; it reports what
  they found, it does not re-judge it.
- If frontmatter is missing or malformed on a file the briefing needs to
  summarize, it reports that file as unparseable rather than guessing its
  intent.
