# Backlog

<!--
Copy to docs/backlog.md. If the project already has a tracker, this file is a view of it,
not a second copy: keep one system of record and name it in AGENTS.md.
Apply the fields when an item is pulled into work. Never convert an inherited backlog in bulk.
Check this file with: python3 tools/verify_status.py docs/backlog.md
Rules: docs/05-work-item-procedure.md (in the guidebook).
Delete these comments and the example rows when you start.
-->

Last verified: YYYY-MM-DD by `python3 tools/verify_status.py docs/backlog.md` (exit 0).

## Status summary

| Status | Count |
|---|---|
| proposed | 0 |
| ready | 0 |
| in-progress | 0 |
| in-review | 0 |
| merged | 1 |
| done | 2 |
| blocked | 0 |
| dropped | 0 |

<!--
Status values, exact and lower case:
proposed, ready, in-progress, in-review, merged, done, blocked, dropped.
merged = merged but not yet verified in the target environment.
done = verified, with Evidence and the Approvals its Risk tier needs.

Field values:
Type: build, decision, discovery, compliance, ops.
Risk tier: local (1 gate: change, always, before merge), shared (2 gates: plan, change),
irreversible (3 gates: plan, change, release, with two distinct humans on release).
Evidence kind: computational (a check produced it) or inferential (a named human judged it;
needs an evidence approval before done).
Blocked by: what blocks the item and the date it was blocked, for example "B-007 since 2026-10-04".
Evidence: a link or path to proof, never a self-report from the system that did the work.
Approvals: gate:who@YYYY-MM-DD entries separated by ";". Gates: plan, change, release,
launch-readiness, expedite, evidence. This cell is the index; the full record of each approval
is one line in docs/approvals.md.
Approvals needed by status: shared or irreversible items need plan before in-progress; every
item needs change before merged; irreversible items need release approvals from two distinct
humans before done.
An expedite approval (incident path) stands in for plan, change and release; an irreversible
item still needs two distinct humans across its release and expedite approvals.
-->

## Items

| ID | Title | Type | Status | Owner | Risk tier | Priority | Workstream | Scope | Specification | Acceptance criteria | Evidence kind | Unblocks | Blocked by | Evidence | Approvals |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | Walking skeleton: build, test and deploy to the dev environment | build | done | alice | shared | 1 | platform | `.ci/pipeline.yml`, `infra/dev/` | Add a pipeline that builds, runs the test suite and deploys an empty service to dev. | `curl -s https://dev.example.com/health` returns 200 with the commit hash of the merge. | computational | B-002 | | [CI run 1042](https://ci.example.com/runs/1042), `evidence/B-001-health.txt` | plan:carol@2026-10-02; change:bob@2026-10-03 |
| B-002 | Health check reports database status | build | merged | bob | shared | 2 | platform | `src/health.py`, `tests/test_health.py` | Extend the health endpoint with a database ping and a test for the failure case. | Health returns 503 when the database is down; regression test passes in CI. | computational | | | | plan:alice@2026-10-04; change:carol@2026-10-05 |
| B-003 | Decide the identity provider | decision | done | carol | shared | 1 | identity | `docs/decisions/` | Compare two options against the criteria in the ADR; the owner decides, agents only prepare the options. | ADR accepted by the owner before the decision deadline 2026-10-10. | inferential | B-004 | | [ADR 0000 (template)](decisions/0000-template.md) | plan:alice@2026-10-06; change:bob@2026-10-08; evidence:alice@2026-10-08 |
