# Work item procedure

Stage 7 of the [method](03-method.md) in detail: the standard procedure that takes one work item
from `proposed` to `done`. This file is the reference for gates, risk tiers, irreversible actions,
the expedite path and evidence rules. Checklists: [gate checklists](../templates/.agents/skills/work-item/gate-checklists.md).
Backlog fields: [../templates/docs/backlog.md](../templates/docs/backlog.md). Agent rules:
[../agent/METHOD.agent.md](../agent/METHOD.agent.md). Status check:
[../tools/verify_status.py](../tools/verify_status.py).

The example project ran the three phases, three human gates, the rules from incidents and a
status script. The rest of this file is design that closes gaps from the gap report, marked once
per section.

## The three phases

The procedure has three phases. Each ends at a gate, and each gate comes **before** the action it
approves. A gate is a decision against stated criteria, as in stage-gate, where gates are "tough
decision meetings" [Cooper]. It is not a status update.

| Phase | Where | Ends with | The gate approves |
|---|---|---|---|
| 1 Review | Read-only, on the latest state | Plan gate | Starting the build as planned |
| 2 Build | One new isolated workspace, one owner | Change gate | Merging the change into a shared branch |
| 3 Release | Started by a human | Release gate | The release action in the target environment |

### Phase 1: review (read-only)

1. Pull the latest state.
2. Read the item and its neighbours (what it unblocks, what blocks it).
3. Check every claim in the item against the source of truth. Mark each one confirmed,
   unconfirmed or wrong, with evidence.
4. Record a **baseline** for everything you will measure afterwards.
5. List the documents and files the change will affect.
6. Classify the risk tier (see below) and list any irreversible actions the item will need.
7. Write the plan: steps, expected changes, tests, how each criterion is checked, cost estimate.
8. Ask the human only about real decisions.
9. **Plan gate.** The approver approves the plan before any workspace is created.

### Phase 2: build (isolated workspace)

1. Create a new workspace (for example a git worktree) with one owner.
2. Write or update the tests that prove the acceptance criteria, then make the change.
3. Verify locally: run the tests and the acceptance checks, and keep their output.
4. Independent reviewers check the change in parallel. They get the change and the acceptance
   criteria, not the author's reasoning: a reviewer that "never saw your conversation"
   [Anthropic BP].
5. Update the affected documents and run the status verification script.
6. **Change gate.** The approver approves the change and the pull request description before
   the merge.

### Phase 3: release (started by a human)

1. Count the expected changes again and compare them with the planned ones, item by item.
2. For a first production release, pass the launch-readiness check (see observability below).
3. **Release gate.** The approver approves the exact release action before it runs.
4. A human starts the action, or explicitly lets the agent start that exact action.
5. Verify the result against the live system, not against a status report.
6. Write the done entry with its evidence before the item is closed.

### Rules from incidents

These came from real failures on the example project and stay as they are:

- Measure a baseline before you change anything.
- A system reporting its own success is not evidence.
- Count the expected changes again before release instead of trusting an estimate.
- Write the done entry before the work item is closed, or it can get lost.
- If a human refuses a permission, the answer stands.

## Risk tiers

One gate weight for every change is too heavy for scaffolding and too light for payments or
personal data. The risk tier sets how many gates an item passes. (untested proposal)

| Risk tier | What it means | Plan gate | Change gate | Release gate | Second human |
|---|---|---|---|---|---|
| local | Reversible, affects only the item's own workspace | no | yes | no | no |
| shared | Affects shared code, shared environments or other people | yes | yes | no | no |
| irreversible | Cannot be undone, or touches production, money, personal data or regulated scope | yes | yes | yes | yes, on the release gate |

- A `local` item's one gate is the change gate, approved before merge.
- A `shared` item that deploys to a shared non-production environment through an automatic
  pipeline after merge needs no release gate, provided the change gate approval names that
  deploy. Anything that reaches production is `irreversible`.
- On an `irreversible` item, the second human approves the release gate and is not the owner or
  the author. Where regulation requires a human reviewer, an agent reviewer does not replace one
  (see [04-variants.md](04-variants.md)).

### How to classify an item

Answer the questions in order. The first "yes" sets the tier.

1. Does any step deploy or apply to production, delete data or resources, spend money, change
   permissions or secrets, read production data with credentials, send anything outside the
   repository, or touch personal data or regulated scope? Then `irreversible`.
2. Does the change, once merged, alter code, configuration, environments, contracts or documents
   that other people, agents or systems depend on? Then `shared`.
3. Otherwise `local`.

Rules for the classification:

- **When unsure, go up one tier.** Moving down needs the plan gate approver to agree and to
  record why.
- The tier belongs to the item, and the highest-risk step decides it. If one step of ten is
  irreversible, the whole item is `irreversible`, or that step becomes its own item.
- Re-classify when the scope changes. A tier never moves down silently.

## Gates come before the action

**The approval record must be dated before the action it approves.** A status verification
script could compare approval times with merge and release times. The reference script does not
(see [tools/README.md](../tools/README.md)). (untested proposal)

### Status transitions

Status values are exact and lower case. These are the only allowed transitions.

| From | To | Required before the transition |
|---|---|---|
| (new) | `proposed` | ID, title, type. Nothing else. |
| `proposed` | `ready` | Owner, risk tier, scope, specification, acceptance criteria, evidence kind (`computational` or `inferential`). Every criterion is a check that can be true or false, or is labelled `inferential` with a named human judge. |
| `ready` | `in-progress` | Review phase complete. Tier `shared` or `irreversible`: a `plan` approval record. Tier `local`: none. |
| `in-progress` | `in-review` | Workspace exists; tests for the acceptance criteria exist and pass locally; pull request or equivalent open; status verification script passes. |
| `in-review` | `in-progress` | A reviewer or approver sends it back. Record the findings. |
| `in-review` | `merged` | A `change` approval record, dated before the merge, for every tier. CI result on the final commit (see evidence quality). |
| `merged` | `done` | Evidence that each acceptance criterion holds in the target environment. Tier `irreversible`: a `release` approval record from the approver and a second from a second human, both dated before the release action; plus a `launch-readiness` record for a first production release. |
| any of `proposed`, `ready`, `in-progress`, `in-review`, `merged` | `blocked` | Blocked by: what, and the date. |
| `blocked` | the status it had before | The blocker is resolved; note the date. |
| any status except `done` or `dropped` | `dropped` | A reason and who decided. Anything already merged or released is reverted or recorded as left in place. |

Rules that apply to the whole table:

- `done` and `dropped` are final. Reopening means a new item that links to the old one.
- `merged` means merged but not yet verified in the target environment. Reporting `merged` as
  `done` is the failure stage 8 exists to catch.
- `done` without an evidence link is invalid, whatever the tier.

## Irreversible actions

An agent never takes one of these actions without an approval record that names that exact
action. This list applies at every risk tier. On a `local` or `shared` item, finding one of
these steps usually means the tier was wrong. (untested proposal)

1. Deploy or apply to a shared or production environment.
2. Delete data or resources.
3. Merge to a shared branch.
4. Send anything outside the repository or to an external party: messages, emails, tickets,
   uploads, requests to other teams.
5. Spend money: purchases, new paid resources, raising quotas or limits that are billed.
6. Change permissions, roles, access or secrets.
7. Edit an existing instruction or context file (the context file, a skill, an agent role, the
   procedure itself).
8. Read production data with credentials.

For merging, the change gate approval is the record.

### How an agent asks

The request is one message to the named approver for that gate. It contains:

- the gate and the item ID;
- the exact action, for example the command, the target environment and the version, commit or
  plan file it applies;
- the expected changes, counted (for example "3 resources changed, 0 deleted");
- the rollback, or "no rollback" if there is none;
- the evidence so far: the baseline and the check output.

Then the agent waits. Silence is not approval, and approval of a different action does not cover
this one. If the counted changes differ from the planned ones, the approval lapses. A refusal
stands.

### Approval record format

Each approval has two parts. The item's Approvals field in the backlog holds a short index entry,
`gate:who@YYYY-MM-DD`, separated by `;`, which the status verification script reads. The full
record goes in the approval log, `docs/approvals.md` ([template](../templates/docs/approvals.md)),
one line per approval:

```
gate | item | who | when | what exactly was approved | link
```

| Field | Content |
|---|---|
| gate | `plan`, `change`, `release`, `launch-readiness`, `expedite` or `evidence` |
| item | The item ID |
| who | A named human and their role. Never an agent, never "the team". |
| when | Date and time with time zone, ISO 8601 |
| what exactly was approved | The action, target and version, as precise as the request |
| link | Where the decision is recorded: a pull request approval, a signed comment, a ticket |

Example:

```
release | ITEM-042 | <approver name>, service owner | 2026-10-31T14:05+01:00 | apply plan file sha256:ab12... to production, 3 changes, 0 deletions | <link to recorded approval>
release | ITEM-042 | <second human>, security reviewer | 2026-10-31T14:20+01:00 | same plan file and target | <link>
```

## Gate owners

In a team, gates need named owners. R does the work for the gate, A approves, C is consulted,
I is informed. (untested proposal)

| Gate | Solo engineer | Small team (2 to 8) | Multi-squad |
|---|---|---|---|
| plan | R: agent. A: the engineer. | R: item owner (with agent). A: a peer or the tech lead, not the owner. C: product owner for scope. | R: item owner. A: squad tech lead. C: owners of any other squad's contract the item touches. I: product owner. |
| change | R: agent and agent reviewers. A: the engineer. | R: author. A: a code owner of the touched paths, not the author. C: agent reviewers. | R: author. A: code owners of every touched path; both sides for a cross-squad contract. C: agent reviewers. |
| release | R: agent. A: the engineer. Second human: someone outside, arranged in advance. | R: owner. A: release approver. Second human: another team member, not the owner. | R: owner. A: service owner. Second human: per the organisation's change policy. I: on-call. |
| launch-readiness | A: the engineer, plus the second human. | A: tech lead, C: on-call. | A: service owner, C: on-call and support. |
| expedite | A: the engineer as incident lead. | A: incident lead. | A: incident lead. I: affected squads. |
| evidence (inferential) | A: the engineer, or the client contact who judges value. | A: product owner. | A: product owner of the squad. |

A solo engineer cannot be their own second human. For `irreversible` items, name the second
human in the plan (a peer, a client approver, a security contact) before the item reaches `ready`.

### Mapping pull request review onto the change gate

- The change gate is the pull request approval by a required reviewer.
- Code owner rules decide who the approver is for the touched paths. The context file and the
  procedure files have code owners too.
- Branch protection enforces "no merge without approval". The approval event in the hosting tool
  is the approval record: it is dated, attributed and cannot be edited.
- Agent reviewers add findings. They do not count as the human approval.
- The author never approves their own change.

### Human review capacity is a work-in-progress limit

Agents produce changes faster than people can check them, so each approver's queue is a
work-in-progress limit.

- Set a limit per approver for items waiting at their gates. A default of 3 is a starting point
  to tune, not a finding.
- When an approver's queue is full, agents do not move more items into `in-review` for that
  approver. They review, write tests or prepare plans instead.
- Track gate wait time per gate; see
  [06-adoption-and-measurement.md](06-adoption-and-measurement.md).

## Expedite path for incidents

During an incident there is no time to review first. The expedite path keeps one approver and
moves the paperwork after mitigation. (untested proposal)

1. **Mitigate first, under the incident lead.** The incident lead is the single approver for
   every action during mitigation, including irreversible ones. The agent still asks before each
   irreversible action, and the incident lead's answer is recorded as an `expedite` approval,
   with time and exact action, as it happens.
2. Prefer reversible mitigations: roll back, switch off a feature, scale up.
3. **Open the item afterwards.** Create the item as soon as the system is stable, with tier
   `irreversible` unless the incident lead records a lower one. Link the incident record.
4. **Backfill within the agreed window.** The default is 48 hours, a value to tune per team.
   Backfill means: the baseline (from monitoring data before the incident), the evidence that the
   mitigation worked, a retrospective `change` review of any code merged during the incident, and
   a **rule from the incident** added to the procedure or the context file. For an `irreversible`
   item the backfill also adds a `release` approval from a second human, dated after the
   mitigation.
5. **No `done` before the backfill.** The item cannot move to `done` until every backfill part is
   linked. A missed window is reported, not hidden.

The expedite path is the one exception to "the gate comes before the action": the `expedite`
record stands in for the `plan`, `change` and `release` records that would have preceded each
mitigation step. The reference script accepts an `expedite` record in their place. It cannot see
whether the backfill happened; the stage 9 audit checks that.

## Testing as a required sensor

The status script checks evidence links, not regressions. An automated regression suite is a
required sensor and runs on every change before the change gate. (untested proposal)

- **Tests come with the change.** Each acceptance criterion that can be checked by a computer has
  a test, added or updated in the same change.
- **Reviewers check the tests, not only the colour of CI.** At the change gate the approver
  checks that tests exist, that they cover the acceptance criteria, and that they would fail
  without the change. Green CI with no relevant tests is not evidence for the item.
- **A failing build is fixed first.** As in continuous integration: "should the integration build
  fail, then it needs to be fixed right away" [Fowler CI].
- **Measure the workflow, don't mandate it.** It is tempting to require test-driven development
  inside the agent loop. A 2026 experiment found "no clearly discernable difference" between
  agents told to follow a TDD workflow and agents that weren't [Böckeler TDD]. That is one
  experiment, so it settles nothing. Require the tests and their coverage, leave the order of
  writing them to the team, and measure escaped defects and rework before and after any
  workflow rule.

## Evidence quality

Agent output is only as good as the check that judges it. Ask for "evidence: the command it ran
and its output" [Anthropic BP]. These rules decide whether a piece of output counts.
(untested proposal)

| Situation | Counts as evidence? |
|---|---|
| Check run on the final commit, passed, output kept | Yes |
| Green re-run with no code change after a red run | No. It is evidence of a flaky test. Quarantine the test and open an item for it. |
| Cancelled run | No |
| Skipped run or skipped tests covering the criterion | No |
| A system's own report that it succeeded (a pipeline status, a tool saying "done") | No. Verify the result directly in the target system. |
| Agent saying "I believe" or "should work" | No. That is unconfirmed. |
| Human judgement labelled `inferential` and approved by a named human | Yes, for criteria that cannot be computed (see below) |

Flaky tests:

- Quarantine a flaky test: move it out of the gating suite and open an item for it. A
  quarantined test covers no acceptance criterion.
- Re-running until green is hope, and "hope is not a strategy" [SRE].

### Audit-grade evidence

Evidence an auditor will read must hold up when nobody remembers the context.

- **Immutable.** Store evidence where it cannot be edited afterwards: a CI run record, a commit,
  a write-once log. A link to a page that changes is not evidence.
- **Dated.** Every piece of evidence and every approval has a date and time with time zone.
- **Attributed.** Each piece says who or what produced it: the person, or the agent and the
  human who directed it.
- **Retained** for at least the audit window the project's compliance owner sets. Record that
  window in the context file.
- **Approvals recorded** in the format above, for every gate, with who and when.

The approach follows evidence-based auditing as in [ISO 19011].

### Inferential evidence

Usability, value and interview findings cannot be checked by a computer. They use inferential
evidence, as opposed to computational sensors [Böckeler].

- Prefer computational evidence: first try to turn the criterion into a count or measurement.
- An inferential criterion is labelled `inferential` in the item's Evidence kind field when the
  item becomes `ready`, with the named human who will judge it.
- The evidence is the material the judgement rests on (session notes, interview summaries,
  recordings where permitted) plus an `evidence` approval record from that human.
- An agent can collect and summarise the material. It cannot be the judge.

## Observability and launch readiness

An item that changes something users see is not done if nobody would notice it breaking.
(untested proposal)

- **Observability is part of the acceptance criteria.** For user-facing items, the criteria name
  the logs, metrics and alerts that show the change works, and the check proves they fire.
- **Launch-readiness gate** before the first production release of a service or a major
  capability. It sits inside the release phase, before the release gate. It checks:
  - a rollback plan, written and tried at least once in a non-production environment;
  - on-call named, with access and a runbook for the new service;
  - monitoring and alerts live and routed to on-call;
  - staged rollout where possible, applying a change "to small fractions of traffic and capacity
    at one time" [SRE-BP].
- Later releases skip it unless the rollback, on-call or monitoring changed.

Change is where outages come from: "roughly 70% of outages are due to changes in a live system"
[SRE]. That is why the release gate and this check sit before the action, not after it.

## Cost

Parallel agents spend money in parallel. (untested proposal)

- **Budget as an invariant from stage 0.** The AI stance names the budget (per month, per item or
  both) and the context file repeats it as an invariant. See [03-method.md](03-method.md).
- **Cost per item.** Where the tools expose cost or token use, record it with the item's evidence
  when it reaches `done`. Where they don't, record the agent time or number of runs instead and
  say so.
- **Overrun is a stop rule.** When an item's spend passes its estimate by a set margin (twice the
  estimate is a default to tune), the agent stops and asks the plan approver whether to continue,
  change the plan or drop the item. When the project budget is reached, all agent work stops
  until a human raises the budget, and that decision is recorded.
- Spending money in the target environment is an irreversible action regardless of budget.

## Stop rule for agent loops

Every agent loop, in the build phase or in setting up the method, follows these rules.
(untested proposal)

1. **Machine-checkable done condition.** Before the loop starts, write down the exact command and
   the expected result (for example an exit code of 0). No check, no loop. "Looks done" is not a
   stop condition. A Stop hook that "sends Claude back to work" [Anthropic BP] is one way to
   enforce it.
2. **Iteration cap.** Set a maximum number of iterations before starting. Five is a reasonable
   default; three when one agent does and another judges.
3. **Same failure twice means stop.** If the same check fails the same way twice, the loop stops.
   The agent writes a short root-cause note in the item: what failed, what was tried, what it
   thinks the cause is, and what it needs from a human. It does not try a third variation.
4. **Recoverable steps.** Each iteration runs in the item's own workspace under version control,
   so every iteration is a checkpoint that can be undone. Loops never run against live
   configuration.

Hitting the cap or the repeat-failure rule moves the item to `blocked`, with the root-cause note
as the blocker and the date.
