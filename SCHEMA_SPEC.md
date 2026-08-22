# Specification: Gr0ve ECOS Graph Substrate (v1.0.0-rc1)
**An Open-Source, Mathematically Grounded Knowledge Substrate for Autonomous AI Reasoning**

---

## 1. Executive Summary & Core Architectural Axioms

The **Gr0ve Ecological Commons Operating System (ECOS)** is an AI-native, open-source knowledge graph substrate designed to achieve **closed-loop citation saturation** over complex ecological, technical, and economic domains.

Unlike unstructured vector databases that rely exclusively on fuzzy top-$k$ semantic similarity, ECOS organizes verified evidence into **deterministic intelligence atoms**. Each atom is a flat Markdown file structured with strict YAML frontmatter, typed directional graph relations, continuous eigenvector authority scores ($\Phi$), and latent Voronoi geometric partitioning.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        ECOS INTELLIGENCE STACK                         │
├────────────────────────────────────────────────────────────────────────┤
│  INTERFACE LAYER    : Hosted Remote MCP Gateway (Paid) | Local `stdio` │
├────────────────────────────────────────────────────────────────────────┤
│  COMPUTATIONAL LAYER: Voronoi Latent Partitioning | Recursive Φ Scoring│
├────────────────────────────────────────────────────────────────────────┤
│  SCHEMA LAYER       : Google OKF / YAML Frontmatter / SI Units         │
├────────────────────────────────────────────────────────────────────────┤
│  STORAGE LAYER      : Flat Markdown Files (.md) | Parquet | Git / OS   │
└────────────────────────────────────────────────────────────────────────┘
```

### Core Axioms
1. **Separation of Fact and Expression**: The substrate stores structured parameters, causal mechanisms, and pointers (DOIs/URLs). It never hosts copyrighted full-text prose.
2. **Deterministic Traversal Over Stochastic Retrieval**: Multi-hop reasoning follows verified directional edges (`supports`, `refutes`, `depends_on`, `prerequisite_for`) rather than loose context window stuffing.
3. **Continuous Epistemic Weighting**: Every node possesses a computed authority score $\Phi \in [0, 1]$ calculated via link-structure analysis to neutralize unverified claims and circular greenwashing.
4. **Local-First, Open Distribution**: The canonical knowledge base is versioned via Git under the MIT License and formatted under the Google Open Knowledge Format (OKF) specification.

---

## 2. File System Topology

The repository adheres to the **Google Open Knowledge Format (OKF v0.1)** and functions natively as an **Obsidian Vault**.

```
ecos-substrate/
├── .github/
│   └── workflows/
│       ├── validate-schema.yml       # YAML linting & link integrity tests
│       └── recompute-graph.yml       # Phi & Voronoi matrix generation
├── .okf/
│   └── manifest.json                 # OKF bundle specification & ontology
├── cells/                            # Voronoi partition directories
│   ├── cell_baseload_renewables/
│   ├── cell_carbon_mineralization/
│   ├── cell_regenerative_agronomy/
│   └── cell_transition_finance/
├── data/
│   ├── graph_adjacency.parquet       # Pre-indexed directional edge matrix
│   ├── graph_nodes.parquet           # Flattened node metadata with Phi scores
│   └── embeddings.parquet            # 1536-dim latent vectors for centroids
├── scripts/
│   ├── lint_schema.py                # Fast JSON-Schema validator
│   ├── compute_phi.py                # Eigenvector PageRank solver
│   └── generate_voronoi.py           # KMeans / Voronoi partitioner
├── llms.txt                          # Top-level index for AI crawlers
├── llms-full.txt                     # High-Phi landmark summary manifest
├── LICENSE                           # MIT License
└── README.md                         # Architecture overview & setup guide
```

---

## 3. Formal Intelligence Atom YAML Specification

Every node in `cells/**/*.md` must strictly conform to the following schema.

### 3.1 JSON-Schema Definition (`schema/atom.schema.json`)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Gr0veIntelligenceAtom",
  "type": "object",
  "required": [
    "id",
    "type",
    "domain",
    "version",
    "epistemic_status",
    "phi_authority_score",
    "voronoi_partition",
    "relations",
    "provenance"
  ],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^atom:[a-z0-9_-]+:[a-z0-9_-]+:[a-z0-9_#-]+$"
    },
    "type": {
      "type": "string",
      "enum": ["claim", "evidence", "technology", "bottleneck", "intervention", "methodology"]
    },
    "domain": {
      "type": "string",
      "enum": ["clean_energy", "soil_carbon", "transition_finance", "circular_materials", "ocean_systems", "governance"]
    },
    "version": { "type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$" },
    "epistemic_status": {
      "type": "string",
      "enum": ["axiom", "empirical_finding", "consensus_rule", "hypothesis", "contested"]
    },
    "confidence_score": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 1.0
    },
    "phi_authority_score": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 1.0
    },
    "voronoi_partition": {
      "type": "object",
      "required": ["generator_id", "distance_to_generator", "is_frontier_boundary"],
      "properties": {
        "generator_id": { "type": "string" },
        "distance_to_generator": { "type": "number" },
        "is_frontier_boundary": { "type": "boolean" },
        "adjacent_cells": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "relations": {
      "type": "object",
      "properties": {
        "supports": { "type": "array", "items": { "type": "string" } },
        "refutes": { "type": "array", "items": { "type": "string" } },
        "depends_on": { "type": "array", "items": { "type": "string" } },
        "prerequisite_for": { "type": "array", "items": { "type": "string" } },
        "quantifies": { "type": "array", "items": { "type": "string" } },
        "mitigates": { "type": "array", "items": { "type": "string" } }
      }
    },
    "metrics": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "required": ["value", "unit"],
        "properties": {
          "value": { "type": "number" },
          "uncertainty": { "type": "string" },
          "unit": { "type": "string" }
        }
      }
    },
    "provenance": {
      "type": "object",
      "required": ["canonical_url", "license_compatibility"],
      "properties": {
        "doi": { "type": "string" },
        "canonical_url": { "type": "string", "format": "uri" },
        "publisher": { "type": "string" },
        "license_compatibility": { "type": "string" }
      }
    }
  }
}
```

### 3.2 Canonical Markdown Node Example

```markdown
---
id: "atom:eco:energy:egs_plasma_drilling_2026"
type: "claim"
domain: "clean_energy"
version: "1.0.0"
epistemic_status: "empirical_finding"
confidence_score: 0.91
phi_authority_score: 0.945
last_validated: "2026-08-22"

voronoi_partition:
  generator_id: "atom:eco:energy:baseload_core"
  distance_to_generator: 0.082
  is_frontier_boundary: true
  adjacent_cells:
    - "cell_subsurface_mineral_rights"
    - "cell_transition_project_finance"

relations:
  supports:
    - "[[atom:eco:energy:clean_firm_power_dispatch]]"
  refutes:
    - "[[atom:eco:energy:geothermal_prohibitive_capex_legacy]]"
  depends_on:
    - "[[atom:eco:tech:non_contact_thermal_plasma_spallation]]"
  prerequisite_for:
    - "[[atom:eco:finance:deep_geothermal_de_risking_facility]]"
  mitigates:
    - "[[atom:eco:grid:renewable_intermittency_dunkelflaute]]"

metrics:
  levelized_cost_energy:
    value: 54.20
    uncertainty: "±3.80"
    unit: "USD/MWh"
  drilling_rate_penetration:
    value: 18.5
    uncertainty: "±1.2"
    unit: "m/h"
  depth_rating:
    value: 5500
    unit: "m"

provenance:
  doi: "10.1016/j.geothermics.2026.104402"
  canonical_url: "https://doi.org/10.1016/j.geothermics.2026.104402"
  publisher: "Elsevier Geothermics"
  license_compatibility: "OpenAccess-CC-BY-4.0"
---

# Summary and Causal Logic Core

## Assertion
Non-contact plasma spallation drilling reduces deep crystalline rock penetration costs by >65%, enabling levelized cost of energy (LCOE) below $55/MWh for enhanced geothermal systems at depths exceeding 5,000 meters.

## Causal Mechanism
1. Thermal spallation eliminates mechanical contact bit friction, reducing casing wear and trips per well by 4.2x.
2. Continuous downhole thermal energy creates high-permeability micro-fracture networks without hydro-shearing induced seismicity.
3. Supercritical working fluids achieve thermodynamic thermal efficiencies >32% at 280°C reservoir temperatures.

## Boundary Conditions and Failure Modes
- **Geological Constraint**: Applicable exclusively in crystalline basement rock; incompetent sedimentary formations cause bore collapse.
- **Capital Threshold**: Requires access to debt capital at interest rates $\le 6.5\%$; higher rates increase amortization costs beyond competitive merchant pricing.
```

---

## 4. Mathematical Graph Formulations

### 4.1 Recursive $\Phi$ Authority Scoring

To neutralize self-referential echo chambers, node authority $\Phi(u)$ is calculated via a directed, link-damped eigenvector centrality:

$$\Phi(u) = \frac{1 - d}{|V|} + d \sum_{v \in \mathcal{B}_u} \frac{\Phi(v) \cdot \omega(v, u)}{\sum_{k \in \mathcal{F}_v} \omega(v, k)}$$

Where:
- $\mathcal{B}_u$ is the set of all nodes directing links into $u$ (`inbound_authorities`).
- $\mathcal{F}_v$ is the set of all forward links originating from node $v$.
- $d = 0.85$ is the empirical damping factor.
- $\omega(v, u)$ is the relation-type weight multiplier:
  - `supports`: $\omega = 1.0$
  - `quantifies`: $\omega = 0.9$
  - `depends_on`: $\omega = 0.8$
  - `refutes`: $\omega = 1.2$ (High epistemic signal)

### 4.2 Latent Space Voronoi Partitioning

1. Compute document dense embeddings $\mathbf{e}_i \in \mathbb{R}^{1536}$ using `text-embedding-3-large` across the normalized `Assertion` and `Causal Mechanism` text.
2. Identify the top $K$ nodes with highest $\Phi$ ratings to serve as **Generators** $\mathcal{G} = \{g_1, g_2, \dots, g_K\}$.
3. Assign each node $u$ to a Voronoi Cell $C_k$:
   $$C_k = \{ u \in \mathcal{V} \mid \|\mathbf{e}_u - \mathbf{e}_{g_k}\|_2 \le \|\mathbf{e}_u - \mathbf{e}_{g_j}\|_2 \quad \forall j \neq k \}$$
4. Calculate Frontier Boundary status:
   $$\text{is\_frontier\_boundary}(u) = \text{True} \iff \frac{\min_{j \neq k} \|\mathbf{e}_u - \mathbf{e}_{g_j}\|_2}{\|\mathbf{e}_u - \mathbf{e}_{g_k}\|_2} \le 1.15$$

---

## 5. Continuous Integration (CI/CD) Pipeline

Every pull request or commit to `main` triggers automated validation via GitHub Actions.

```
[Git Commit]
     │
     ▼
[Step 1: Schema Validation] ────> Validates JSON Schema & YAML Syntax
     │
     ▼
[Step 2: Link Integrity]    ────> Checks that all [[wikilinks]] resolve
     │
     ▼
[Step 3: Graph Recompute]   ────> Solves Phi scores & Voronoi assignments
     │
     ▼
[Step 4: Serialization]     ────> Generates data/graph_*.parquet & llms.txt
     │
     ▼
[Step 5: Auto-Commit / PR]  ────> Writes updated frontmatter back to repo
```

---

## 6. Model Context Protocol (MCP) Interface Specification

The open-source local MCP tool (`@thegr0ve/local-mcp`) and hosted remote gateway implement the following standardized tools.

### 6.1 Tool: `query_atoms`
Searches atoms filtered by domain, epistemic status, minimum $\Phi$ score, and Voronoi cell.

```json
{
  "name": "query_atoms",
  "description": "Retrieve structured intelligence atoms filtered by graph properties",
  "inputSchema": {
    "type": "object",
    "properties": {
      "domain": { "type": "string" },
      "min_phi": { "type": "number", "default": 0.5 },
      "epistemic_status": { "type": "string" },
      "voronoi_generator": { "type": "string" }
    }
  }
}
```

### 6.2 Tool: `traverse_lineage`
Performs multi-hop directional path traversal from a seed node.

```json
{
  "name": "traverse_lineage",
  "description": "Trace causal dependencies and evidence branches across typed edges",
  "inputSchema": {
    "type": "object",
    "required": ["seed_atom_id", "depth"],
    "properties": {
      "seed_atom_id": { "type": "string" },
      "depth": { "type": "integer", "maximum": 5 },
      "edge_types": {
        "type": "array",
        "items": { "type": "string", "enum": ["supports", "refutes", "depends_on", "prerequisite_for"] }
      }
    }
  }
}
```

### 6.3 Tool: `detect_frontier_gaps`
Identifies boundary nodes between competing Voronoi domains where research conflicts or unlinked synergies exist.

```json
{
  "name": "detect_frontier_gaps",
  "description": "Retrieve high-authority nodes located on Voronoi cell boundaries",
  "inputSchema": {
    "type": "object",
    "required": ["primary_cell", "adjacent_cell"],
    "properties": {
      "primary_cell": { "type": "string" },
      "adjacent_cell": { "type": "string" },
      "min_phi": { "type": "number", "default": 0.75 }
    }
  }
}
```

---

## 7. Local Client Integration Configurations

### 7.1 Claude Desktop Configuration (`claude_desktop_config.json`)

```json
{
  "mcpServers": {
    "gr0ve-ecos": {
      "command": "npx",
      "args": [
        "-y",
        "@thegr0ve/local-mcp",
        "--vault-path",
        "/absolute/path/to/cloned/ecos-substrate"
      ]
    }
  }
}
```

### 7.2 DuckDB Local Analytical Querying

```python
import duckdb

con = duckdb.connect()

# Find high-certainty geothermal interventions with LCOE < $60/MWh
query = """
SELECT 
    id,
    phi_authority_score,
    metrics.levelized_cost_energy.value AS lcoe_usd,
    voronoi_partition.generator_id
FROM read_parquet('data/graph_nodes.parquet')
WHERE domain = 'clean_energy'
  AND phi_authority_score > 0.85
  AND metrics.levelized_cost_energy.value < 60.0
ORDER BY phi_authority_score DESC;
"""

results = con.execute(query).df()
print(results)
```

---

## 8. Licensing and IP Governance

1. **Substrate Schema & Code**: Licensed under **MIT License**.
2. **Metadata & Graph Weights**: Licensed under **Creative Commons CC0 1.0 Universal** (Public Domain Dedication).
3. **Synthetic Paraphrased Assertions**: Original editorial commentary licensed under **CC-BY 4.0**.
4. **Third-Party Authorities**: All original scientific papers and reports remain property of their respective copyright holders, referenced strictly via non-infringing DOI/URL pointers.
