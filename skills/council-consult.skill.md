---
name: council-consult
description: >
  Convene a structured, multi-perspective review before an agent commits an
  ambiguous, irreversible, or cross-cutting change to the ecos-substrate
  graph (new/changed entity_type or relation_type, community restructuring,
  or anything a human reviewer tags needs-council-review).
version: "0.1.0"
---

# Skill: Council Consult

## Purpose

Prevent a single agent pass from unilaterally deciding ambiguous schema or
structural questions. Instead of one model producing one answer, this skill
runs the same decision through several fixed "council seats," each holding
a different mandate, and synthesizes their input into one recommendation
plus a written record.

## When to use this skill

Invoke `council-consult` when any of the following is true:
- You are about to add, rename, merge, or remove an `entity_type` or
  `relation_type` in `schema/schema.yaml`.
- You are about to restructure the community hierarchy under `entities/`
  (split, merge, or move a top-level domain directory).
- A human reviewer or the `wf-council.yaml` workflow has applied the
  `needs-council-review` label to an issue or PR.
- You are unsure whether a change is "routine content" or a "schema
  change" per `AGENTS.md`.

Do not invoke it for routine node additions that reuse existing,
unambiguous types.

## Council seats

Each seat is a fixed prompt persona applied to the same proposed change.
Seats are not separate services — they are perspectives the invoking agent
must explicitly reason through, in order, before producing a
recommendation:

1. **Schema Steward** — Does this fit cleanly into `SCHEMA_SPEC.md`'s
   existing definitions, or does it silently overload an existing concept?
   Would a domain expert reading `schema/schema.yaml` in six months
   understand why this type exists?
2. **Graph Architect** — What is the blast radius? How many existing nodes
   reference the type/community being changed (`depends_on` edges), and
   does `scripts/validate_graph.py` still pass after the change?
3. **Retrieval Engineer** — Does this change help or hurt the eventual
   GraphRAG graduation path (`config/graphrag.settings.template.yaml`)?
   Will it produce a coherent embedding/community boundary, or fragment
   one that already exists?
4. **Dissenting Reviewer** — Actively argue against the proposed change.
   What breaks, what becomes harder to maintain, what's the cheaper
   alternative?

## Procedure

1. **Frame the question** in one or two sentences: what is being added,
   renamed, merged, or removed, and why.
2. **Run each council seat** above against the framed question, producing
   2–4 sentences per seat. Seats must be argued from their stated mandate,
   not merged into one generic answer.
3. **Synthesize** a single recommendation: proceed, proceed with
   modification, or do not proceed — with a one-line justification citing
   the seat(s) that drove the decision.
4. **Record the decision.** Write the framed question, the four seat
   responses, and the synthesis into a short markdown block and attach it
   to the PR or issue description (or as a PR comment if the PR already
   exists). Do not discard the seat responses — they are the audit trail
   `wf-audit.yaml` and future contributors rely on.
5. **Proceed only after recording.** If the synthesis is "do not proceed,"
   stop and report back to the human requester instead of making the
   change.

## Output template

```
### Council Consult: <one-line question>

**Schema Steward:** ...
**Graph Architect:** ...
**Retrieval Engineer:** ...
**Dissenting Reviewer:** ...

**Synthesis:** proceed | proceed with modification | do not proceed — <why>
```

## Relationship to other files

- Triggered manually by any agent per `AGENTS.md`, or automatically flagged
  by `.github/workflows/wf-council.yaml` via the `needs-council-review`
  label (see `.github/labels.yml`).
- Its output feeds `agents/briefing.agent.md`, which includes the
  synthesis line (if present) in the PR briefing.
