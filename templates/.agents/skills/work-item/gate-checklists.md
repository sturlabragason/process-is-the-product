# Gate checklists

<!--
Checklists for the gates of the standard procedure, by risk tier, and the approval record
format. For the authoritative rules, see the guidebook, docs/05-work-item-procedure.md (not copied into the project).
If this file and that one disagree, that one wins and this file gets fixed. It lives next to the standard procedure
(SKILL.md). Trim items you never use.
-->

## Gates by phase

| Phase | Ends with | The gate approves |
|---|---|---|
| 1 Review (read-only) | plan gate | Starting the build as planned |
| 2 Build (own workspace) | change gate | Merging the change into a shared branch |
| 3 Release (started by a human) | release gate | The exact release action in the target environment |

Other gates: `launch-readiness` (inside the release phase, before the release gate, for a first
production release), `expedite` (incident path), `evidence` (a named human judges inferential
evidence).

## Which gates each risk tier needs

| Risk tier | What it means | Plan | Change | Release | Second human |
|---|---|---|---|---|---|
| local | Reversible, affects only the item's own workspace | no | yes, always, before merge | no | no |
| shared | Affects shared code, environments or other people | yes | yes | no | no |
| irreversible | Cannot be undone, touches production, money, personal data or regulated scope | yes | yes | yes | yes, on the release gate |

When unsure, go up one tier. An agent reviewer adds findings and never replaces the human
approval. The second human is not the owner or the author.

## Approvals needed for each status

These follow the status transitions; see the guidebook, docs/05-work-item-procedure.md (not copied into the project).

| Moving to | Approval needed before the move |
|---|---|
| `in-progress` | shared or irreversible: `plan`. local: none. |
| `merged` | every tier: `change`, dated before the merge. |
| `done` | evidence for each criterion in the target environment. irreversible: `release` (or `expedite`) approvals from two distinct humans, dated before the release action, plus `launch-readiness` for a first production release. Inferential evidence: `evidence`. |

An `expedite` approval stands in for `plan`, `change` and `release` on the incident path. On an
irreversible item the backfill adds a second human's `release` approval within 48 hours, so two
distinct humans appear across the `release` and `expedite` entries. The item cannot be `done`
until the backfill is linked.

## How to ask for a gate

1. Stop. Do not start the next step.
2. Send one message to the approver named for that gate in `docs/roles.md`, with: the gate and
   the item ID; the exact action (command, target environment, version, commit or plan file);
   the expected changes, counted; the rollback, or "no rollback"; the evidence so far.
3. Wait. Silence is not approval. Approval of a different action does not cover this one. If the
   counted changes differ from the planned ones, the approval lapses. A refusal stands.
4. Record the approval (format below) before you act on it.

## Plan gate

- [ ] Latest state pulled; item and the items it blocks or unblocks read.
- [ ] Every claim in the item checked against the source of truth: confirmed, unconfirmed or
      wrong, with evidence.
- [ ] Baseline recorded for everything that will be measured afterwards.
- [ ] Documents and files the change will affect are listed.
- [ ] Risk tier stated, with the reason; irreversible actions the item needs are listed.
- [ ] Plan written: steps, expected changes, tests, how each criterion is checked, cost estimate.
- [ ] Open questions are real decisions, put to the owner; none answered by the agent.
- [ ] irreversible: rollback written; second human named.

## Change gate

- [ ] Change made in its own workspace with one owner.
- [ ] Tests that prove the acceptance criteria exist, cover them, and would fail without the
      change.
- [ ] Verified locally on the final commit; command and output linked.
- [ ] No green re-run without a code change counted as success (that is a flaky test).
- [ ] Independent reviewer got the change and the acceptance criteria, not the author's
      reasoning; findings attached.
- [ ] Affected documents updated.
- [ ] `python3 tools/verify_status.py docs/backlog.md` exits 0.
- [ ] Pull request description matches the change. The author does not approve their own change.
- [ ] User-facing items: logs, metrics and alerts are in the acceptance criteria.

## Launch-readiness gate (first production release only)

- [ ] Rollback plan written and tried at least once outside production.
- [ ] On-call named, with access and a runbook for the new service.
- [ ] Monitoring and alerts live and routed to on-call.
- [ ] Staged rollout where possible.

## Release gate (before the action)

The release gate comes before the irreversible action, never after it.

- [ ] The exact action is named: command, target environment, version or plan file.
- [ ] Planned changes compared with expected changes, item by item; counts recounted, not
      estimated.
- [ ] Second human approval recorded, from someone who is not the owner or the author.
- [ ] A human starts the action, or explicitly lets the agent start that exact action.
- [ ] Verification plan: the check against the live system (not a status report) and who runs it.

After the action: verify against the live system, write the done entry with evidence, then close
the item.

## Evidence gate (inferential evidence)

- [ ] The criterion was labelled `inferential` when the item became `ready`, with a named judge.
- [ ] The material the judgement rests on is linked.
- [ ] The judge is a human, not an agent.

## Expedite (incident path)

- [ ] The incident lead approves each action as it happens, recorded as `expedite`.
- [ ] Reversible mitigations preferred.
- [ ] Item opened once stable, tier `irreversible` unless the incident lead records a lower one.
- [ ] Backfill linked within the agreed window: baseline, evidence the mitigation worked, a
      retrospective `change` review of code merged during the incident, a rule from the incident,
      and (irreversible) a `release` approval from a second human.

## Approval record format

The backlog Approvals cell is the index, one entry per approval, separated by `;`:

```
gate:who@YYYY-MM-DD
plan:alice@2026-10-01; change:bob@2026-10-02; release:carol@2026-10-03; release:dave@2026-10-03
```

`gate` is `plan`, `change`, `release`, `launch-readiness`, `expedite` or `evidence`.
`tools/verify_status.py` checks this format.

The full record is one line in the approval log, `docs/approvals.md` (template:
[docs/approvals.md](../../../docs/approvals.md)), kept where it cannot be edited later:

```
gate | item | who | when | what exactly was approved | link
change | B-001 | bob, code owner | 2026-10-02T14:05+02:00 | commit 3f2c1a9 and pull request 42 description, merge to main | <link to the approval>
```

An approval covers exactly what it names. A later commit needs a new approval.
