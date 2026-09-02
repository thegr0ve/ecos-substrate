# Graph Substrate Conventions

This document defines how every content file in this repository participates
in the graph substrate described in `SCHEMA_SPEC.md` and `schema/schema.yaml`.

## Node Convention: YAML Frontmatter

Every entity-bearing Markdown file MUST begin with a YAML frontmatter block:

```yaml
---
type: "<one of schema/schema.yaml:entity_types[].name>"
title: "Human-readable node title"
description: "One or two sentence summary used for embedding/community seeding."
tags: ["domain-tag-1", "domain-tag-2"]
depends_on: ["./relative/path/to/other-node.md"]
timestamp: "YYYY-MM-DDTHH:MM:SSZ"
---
```

- `type` MUST match a value declared in `schema/schema.yaml`.
- `depends_on` MUST use relative paths to other files in this repository.
  These become graph edges and are validated by CI (see `.github/workflows/wf-audit.yaml`).
- `tags` seed the attribute layer used for community refinement once the
  repository graduates to automated clustering.

## Directory Convention: Community Hierarchy

Directories are not arbitrary — they encode the community hierarchy of the
graph:

- `entities/<domain>/` — top-level domains map to macro communities.
- `entities/<domain>/<subdomain>/` — subdirectories map to sub-communities.
- `relationships/` — cross-domain relationship definitions that don't belong
  to a single domain.
- Each directory SHOULD contain a `_community.yaml` summarizing its scope
  (see `templates/_community.yaml.template`).

## Graduation Path

1. **Now:** Prose spec + machine-readable schema seed (`schema/schema.yaml`).
2. **Next:** Populate `entities/` and `relationships/` with frontmatter'd
   nodes; enforce via CI.
3. **Then:** Generate per-domain embeddings and a Voronoi/IVF or HNSW index
   scoped to each top-level directory.
4. **Finally:** Fuse the embedding index with the community graph (C-HNSW /
   GraphRAG-style hierarchical retrieval) by activating
   `config/graphrag.settings.template.yaml` as the live pipeline
   configuration, seeded from `schema/schema.yaml`.

See `README.md` for the current stage.

## Type-Casing Convention

`entity_types` in `schema/schema.yaml` MUST use **PascalCase** names (e.g.
`Entity`, `Idea`, `Relationship`) — matching the convention already
established by the `Entity` and `Idea` types seeded in this repository.
Lowercase or `snake_case` entity-type names (e.g. the historical
`relationship` entity type) are a documentation gap, not an alternative
convention, and MUST be corrected to PascalCase when touched.

`relation_types` describe edge predicates and MUST use lowercase
`snake_case` names (e.g. `depends_on`, `related_to`). Frontmatter field names
also remain lowercase `snake_case` per the block above. The validator checks
both vocabularies and fails closed on duplicate, malformed, or incorrectly
cased schema names.
