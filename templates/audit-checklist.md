# Harness audit checklist

<!--
Stage 9: retrospective and harness maintenance. Run it on a fixed schedule (for example every two
weeks) and after any incident. The "harness" is the context file, roles, skills, procedures,
templates and scripts that agents load.
Exit criteria: the audit finds no high-severity stale instructions.
Changes this audit proposes to existing instruction or context files are irreversible actions:
they need a recorded human approval first. Removal rules: see the guidebook,
docs/06-adoption-and-measurement.md (not copied into the project).
-->

Date: YYYY-MM-DD
Auditor: <!-- someone other than the main author of the files, or a read-only reviewer agent -->
Files in scope: `AGENTS.md`, `docs/`, `.agents/skills/`, `tools/`, <!-- others -->

## Checks

| # | Check | How | Finding | Severity |
|---|---|---|---|---|
| 1 | Stale paths | Every path and link in the harness files exists | | |
| 2 | Stale components | Every service, resource, tool or role named still exists | | |
| 3 | Contradictions | No two files give different rules for the same thing | | |
| 4 | Duplicates | Each rule lives in one place; others link to it | | |
| 5 | Unused rules | Rules not triggered or cited for N weeks (N set in the adoption doc) | | |
| 6 | Status values | Only the eight status values appear anywhere | | |
| 7 | Status verification | `python3 tools/verify_status.py docs/backlog.md --check-paths` exits 0 | | |
| 8 | False done | Sample done rows; evidence still proves the claim against the live system | | |
| 9 | Gates | Every Approvals entry in the backlog has a line in `docs/approvals.md` that names what was approved, dated before the action | | |
| 10 | Ownership | Every area, gate and the context file has a current owner | | |
| 11 | AI stance | Tools, data classes and budget still match practice | | |
| 12 | Size | Context file still short enough to load whole; agent rules at most 150 lines | | |
| 13 | Over-building | Every stage in use has a named trigger that fired; no artifacts for others | | |
| 14 | Incidents | Each incident since the last audit became a rule, or a note says why not | | |
| 15 | Expedite backfill | Every item approved by `expedite` has its backfill linked within the window | | |

Severity: high (an agent following it would do harm or report false status), medium (wasted
work or confusion), low (wording).

## Retrospective

- What worked since the last audit:
- What failed, and which stage trigger it points to:
- Gate wait time, false-done rate and rework since the last audit (if measured):

## Actions

<!-- Each action becomes a backlog item. Prefer removing a rule to adding one. -->

| Action | Remove, change or add | Backlog item | Owner | Approved by |
|---|---|---|---|---|
| | | | | <!-- change:bob@YYYY-MM-DD --> |
