# ecos-substrate

Open-source, mathematically grounded ecological knowledge graph substrate for Gr0ve ECOS.

## What this is

`ecos-substrate` starts as a foundational schema specification (`SCHEMA_SPEC.md`)
and is designed to graduate, without a rewrite, into a full graph + vector
retrieval substrate (GraphRAG, with Voronoi/HNSW-based nearest-neighbor
indexing over a hierarchical community graph).

## Current stage: Foundational scaffolding

| Layer | Status | Where |
|---|---|---|
| Prose schema spec | Done | `SCHEMA_SPEC.md` |
| Machine-readable schema seed | Scaffolded | `schema/schema.yaml` |
| Node/frontmatter convention | Defined | `docs/GRAPH_CONVENTIONS.md` |
| Directory-as-community structure | Scaffolded | `entities/`, `relationships/` |
| Graph validation (CI) | Scaffolded | `.github/workflows/validate-graph.yml`, `scripts/validate_graph.py` |
| Embedding + Voronoi/HNSW index | Not started | future: per-directory index over `entities/` |
| Fused GraphRAG runtime | Not started | future: `config/graphrag.settings.template.yaml` → active config |

## Graduation roadmap

1. Extract concrete entity/relation types from `SCHEMA_SPEC.md` into
   `schema/schema.yaml`.
2. Decompose `SCHEMA_SPEC.md` into individual node files under `entities/`,
   following `docs/GRAPH_CONVENTIONS.md` (YAML frontmatter + `depends_on` links).
3. Let CI (`validate-graph.yml`) enforce frontmatter and link integrity as
   the node count grows.
4. Once retrieval needs exceed link-traversal (paraphrase, cross-domain
   similarity), add embeddings and a Voronoi/IVF or HNSW index scoped per
   top-level `entities/<domain>/` directory.
5. Fuse the vector index with hierarchical community detection (Leiden /
   C-HNSW-style) and activate `config/graphrag.settings.template.yaml` as a
   real pipeline configuration.

## Contributing

See `docs/GRAPH_CONVENTIONS.md` before adding new entity or relationship files.
