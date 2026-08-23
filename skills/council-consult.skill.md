---
skill: council-consult
role: elicit-submit-synthesize-multi-model-array
repo: thegr0ve/ecos-substrate
covers: [consultation, audit]
---

# skills/council-consult.skill.md

PURPOSE: standardized way to (1) collect individual model consultations or
audit reports as ledger entries, and (2) run a fresh-session synthesis over
the full array into one final PR. Raw individual submissions auto-merge as
ledger entries. The synthesis PR — the compounded output — always requires
operator approval before it touches main.

## STAGE 1 — INDIVIDUAL SUBMISSION PROMPT (paste into any model session)
```
Repo: thegr0ve/ecos-substrate (GitHub).
1. Read AGENTS.md at repo root fully before responding.
2. Task: <consultation on topic_issue #N> OR <audit of target X, audit_issue #N>.
3. Produce ONE output matching the exact frontmatter schema in AGENTS.md
   (consultation or audit schema, as applicable). No text outside the block.
4. If you have git-write tools: create branch and file per AGENTS.md
   GIT_RULES naming, open PR labeled model:<your-name> +
   council-response|audit-response, linking the issue. Stop after opening it.
5. If you do NOT have git-write tools: output only the frontmatter block.
   It will be submitted on your behalf.
```

## STAGE 2 — SUBMISSION HANDLING
- Validate required fields present (see AGENTS.md schemas). Reject and
  request re-run on failure — never hand-patch a model's output.
- Valid submissions auto-merge on green CI (raw ledger entries only).
- Track quorum: when all requested models (or minimum count set on the
  issue) have merged submissions, flip label to `synthesis-ready`.

## STAGE 3 — FRESH-SESSION SYNTHESIS PROMPT (new session, new context)
```
Repo: thegr0ve/ecos-substrate (GitHub).
1. Read AGENTS.md fully.
2. Read every file under <domain>/proposals/ or <domain>/audits/ tagged
   to issue #N — this is the full array, weighted equally.
3. Confirm: you did not author any of these input files.
4. Reason across the full array. Produce ONE synthesis output for the
   target file/topic, citing which input file(s) support each conclusion.
5. Open the synthesis as a PR against the target, labeled
   council-derived|audit-derived + awaiting-operator, linking issue #N.
6. Do NOT merge. This PR requires explicit operator approval regardless
   of how strong consensus was across the array.
```

## STAGE 4 — OPERATOR GATE (mandatory, no exceptions)
- Every synthesis PR sits as `awaiting-operator` until reviewed and
  approved by the operator, no matter the model count, confidence scores,
  or consensus strength in the array.
- Compounded multi-model reasoning is evidence presented to the operator,
  not a merge authorization. Only the operator merges.

## VALIDATION (applies to stages 1-3)
- All schema fields present and correctly typed (confidence in [0,1]).
- Path/branch naming matches AGENTS.md GIT_RULES exactly.
- Synthesis session identity != any contributing submission's `model` field
  for that same issue.
- No submitted or synthesized file is ever deleted.

## EQUAL WEIGHT ENFORCEMENT
No model name maps to a priority multiplier anywhere in this skill, CI, or
synthesis instructions. Every valid submission under an issue counts once.
This applies to how the array is reasoned over — it does not extend to
merge authority, which remains exclusively the operator's.
