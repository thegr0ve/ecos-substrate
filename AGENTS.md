---
repo: thegr0ve/ecos-substrate
role: root-orientation
read_order: [README.md, GAMEPLAN.md, operator/STATE.md, operator/TODO.md]
generated_files_do_not_edit: [operator/TODO.md, operator/STATE.md]
---

# AGENTS.md

PURPOSE: ecos-substrate = graph-substrate for Gr0ve ECOS (ecological knowledge
graph -> GraphRAG). Repo also self-governs as GOS ("Git Operating System"):
todos, direction, agent/skill defs are git-native artifacts, not external tools.

RULE: No deletion, ever. State = transition (Issue closed, gate advanced, PR
merged), not erasure. Reconstruct state from history, not memory.

## READ_ORDER (session start)
1. README.md -> graph-substrate stage
2. GAMEPLAN.md -> current direction
3. operator/STATE.md -> generated graph/gate snapshot
4. operator/TODO.md -> generated mirror of open `operator-todo` Issues
   (includes `approval-gate` subtype — see APPROVAL_GATE_PROTOCOL)

## GIT_RULES
- main <- PR only. PR body required fields: why | what | impact | rollback.
- PR must link Issue via `Closes #N`.
- Branch naming: `todo/<issue#>-slug` | `agent/<agent-name>/<task>` | `<domain>/proposals/<model>-<date>` | `<domain>/audits/<model>-<date>`
- Labels: `operator-todo` `agent-proposed` `ai-generated` `model:<name>` `gate:distill|review|ratify` `risk:low|medium|high` `council-requested` `audit-requested` `synthesis-ready` `council-response` `audit-response` `approval-gate` `approved` `rejected` `revision-round`
- risk:high (schema/, AGENTS.md, GAMEPLAN.md, .github/) edited directly -> operator approval required, routed through APPROVAL_GATE_PROTOCOL.
- risk:low content-only PRs -> mergeable on green CI, no gate.
- Individual raw submissions (single-model proposals/audits) -> auto-merge
  on green CI as ledger entries only.
- ANY synthesis PR (council or audit derived) -> routed through
  APPROVAL_GATE_PROTOCOL before merge. No auto-merge, ever.
- Todos = Issues. Closed (not deleted) when resolved.

## APPROVAL_GATE_PROTOCOL (approval IS a to-do, not a side-process)
TRIGGER: any PR requiring operator approval (synthesis PR, direct risk:high edit).
STEPS:
1. Automation opens ONE companion Issue: labels `operator-todo` +
   `approval-gate`, title "Approve PR #<n>: <topic>", linking the PR.
2. Issue body MUST be self-contained: topic summary, link to PR diff,
   contributing array files (if synthesis), consensus/confidence stats.
   A fresh session must brief the operator from THIS ISSUE ALONE.
3. Surfaces in operator/TODO.md like any other to-do — not a separate list.
4. Operator may open a fresh session, point it at the Issue only, get a
   brief from agents/briefing.agent.md (read-only, cannot approve/merge).
5. Operator decision recorded as a comment: `APPROVED` or `REJECTED: <reason>`.
6. APPROVED -> automation merges linked PR, closes Issue referencing merge
   commit. Label -> `approved`.
7. REJECTED -> PR closed without merge, Issue closed with reason logged
   verbatim. Label -> `rejected`. Permanent record, never deleted.
8. Revision after rejection -> REVISION_ROUND_PROTOCOL (below). Never
   reopen or mutate a closed Issue.

## REVISION_ROUND_PROTOCOL (rejected synthesis needing another attempt)
PRINCIPLE: inform the next round without letting it anchor on the rejected
answer. Seed context, but always re-run the full independent array.
STEPS:
1. Open a NEW topic Issue (`council-requested` or `audit-requested`),
   label `revision-round`, field `round: N+1`, `supersedes: #<rejected-issue>`.
2. New Issue body MUST include, verbatim: the operator's stated rejection
   reason, a link to the rejected synthesis PR, and a link to the full
   round-N input array (never deleted, still readable).
3. Every model in round N+1 submits an INDEPENDENT fresh position per
   COUNCIL_PROTOCOL/AUDIT_PROTOCOL — same schema, same equal weight. Models
   MAY cite round-N submissions as input but MUST NOT treat the rejected
   synthesis as a draft to lightly revise. Explicitly instructed to
   reconsider from first principles in light of the rejection reason, not
   patch the prior answer.
4. Round-N submissions and synthesis remain permanently in the ledger,
   linked via `supersedes`/`superseded_by`, so the chain of attempts stays
   traceable across however many rounds occur.
5. Round N+1 synthesis routes through APPROVAL_GATE_PROTOCOL exactly as
   any other synthesis. No shortcut to merge based on round count.
6. No hard cap on rounds by default, but repeated rejection on the same
   topic is itself a signal — operator may escalate scope (e.g. widen
   model set, add audit-requested alongside council-requested) at their
   discretion.

## COUNCIL_PROTOCOL (consultation on any topic)
TRIGGER: Issue labeled `council-requested`.
WEIGHT: equal across all participating models, no exceptions.
STEPS:
1. Each model submits ONE file `<domain>/proposals/<model>-<date>.md` on its
   own branch, own PR, per frontmatter schema below.
2. Submission PR auto-merges on green CI (frontmatter/path validation only).
3. When all requested models (or minimum quorum) have submitted, Issue
   label -> `synthesis-ready`.
4. A FRESH LLM session (must NOT have authored any submission under review)
   reads AGENTS.md + full merged array under `<domain>/proposals/`, reasons
   across all of them, produces ONE synthesis PR against the target file,
   citing which proposal(s) contributed which conclusions.
5. Synthesis PR enters APPROVAL_GATE_PROTOCOL.
6. All individual proposal files remain permanently, never deleted.

## AUDIT_PROTOCOL (structurally identical to COUNCIL_PROTOCOL)
TRIGGER: Issue labeled `audit-requested`.
STEPS: identical to COUNCIL_PROTOCOL but path = `<domain>/audits/<model>-<date>.md`,
labels `audit-response` -> `synthesis-ready` -> APPROVAL_GATE_PROTOCOL.

### Submission frontmatter schema (consultation)
```yaml
---
model: "<model-name>"
date: "YYYY-MM-DD"
topic_issue: "#<issue-number>"
round: 1
position: "<one-line stance>"
confidence: 0.0-1.0
rationale: |
  <structured reasoning>
---
```

### Submission frontmatter schema (audit)
```yaml
---
model: "<model-name>"
date: "YYYY-MM-DD"
audit_issue: "#<issue-number>"
round: 1
target: "<path/file/scope audited>"
findings:
  - severity: "low|medium|high"
    description: "<finding>"
confidence: 0.0-1.0
---
```

### Fresh-session synthesis rules
- Synthesizing session gets ONLY: AGENTS.md + the merged array of proposal/audit
  files for the given issue + round context (rejection reason if round > 1).
  No prior conversation carryover.
- Must explicitly disclose it did not author any input file before producing output.
- Output PR body must cite every contributing file by path.
- Output PR routes through APPROVAL_GATE_PROTOCOL. Never auto-merges.

## POINTERS (do not inline — read on demand)
- Frontmatter/node rules -> docs/GRAPH_CONVENTIONS.md
- Entity/relation types -> schema/schema.yaml
- Agent scopes -> agents/*.agent.md (see agents/briefing.agent.md)
- Reusable capabilities -> skills/*.skill.md
- Deterministic procedures -> workflows/*.yaml
- CI validation logic -> scripts/validate_graph.py

## BOUNDARIES
- Never edit operator/TODO.md or operator/STATE.md directly (generated).
- Never delete: Issues, proposal/audit files, closed PRs.
- Never let a synthesis session be authored by a model that submitted an
  input to that same synthesis.
- Never auto-merge a synthesis or risk:high PR. Route through
  APPROVAL_GATE_PROTOCOL, no exceptions.
- Never let a revision round treat the rejected synthesis as a base to
  patch — it is context, not a draft.
- A briefing agent (agents/briefing.agent.md) may summarize an approval-gate
  Issue but may never itself comment APPROVED/REJECTED or merge.
