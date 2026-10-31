---
name: work-item
description: Standard procedure to take one backlog item from ready to verified done, with human approval gates before every irreversible action. Use only when a human asks to run a specific item, for example "run item B-001".
disable-model-invocation: true
---

# Run one work item

<!--
Stage 7. Copy to .agents/skills/work-item/SKILL.md. Write it from the cleanest run you did by hand,
not before. Add each incident as a rule under "Rules from incidents". Editing this file after it
is in use is an irreversible action: it needs a recorded human approval first.
Authoritative rules: see the guidebook, docs/05-work-item-procedure.md (not copied into the project).
-->

Input: an item ID from `docs/backlog.md`. If there is no backlog, stop and say so.

Gates by risk tier: local = change (one gate, always, before the merge); shared = plan, change; irreversible = plan, change, release,
with a second human (not the owner or the author) on the release gate. A first production release
also needs launch-readiness; inferential evidence needs an evidence approval. Record each approval
as one line in `docs/approvals.md` and as `gate:who@YYYY-MM-DD` in the item's Approvals cell.
On the incident path an `expedite` approval stands in for plan, change and release.
Checklists and formats: `gate-checklists.md` next to this file.

## Irreversible actions

Each one needs a recorded human approval for this item before you do it, whatever the risk tier:

- deploy or apply to a shared or production environment;
- delete data or resources;
- merge to a shared branch;
- send anything to an external party;
- spend money;
- change permissions or secrets;
- edit an existing instruction or context file (including `AGENTS.md` and this skill);
- read production data with credentials.

## Phase 1: review (read-only, item is `ready`)

1. Pull the latest state. Read the item and the items it blocks or unblocks.
2. Check every claim in the item against the source of truth. Mark each one confirmed,
   unconfirmed or wrong, with evidence.
3. Record baseline values for everything you will measure afterwards.
4. List the documents and files the change will affect.
5. State the risk tier and why, and list any irreversible actions the item needs. When unsure, go
   up one tier.
6. Write the plan: steps, expected changes, tests, how each criterion is checked, cost estimate.
7. If the item needs a choice a human has not made, stop and propose a decision item with the
   options. Do not pick one.
8. **Plan gate** (shared and irreversible). Ask for approval of the plan and record it. Only then
   set status `in-progress`. A local item moves to `in-progress` when the review is done.

## Phase 2: build (own workspace)

1. Create a new workspace for this item (for example `git worktree add ../wt-<ID> -b item/<ID>`).
   Only you write in it.
2. Write or update the tests that prove the acceptance criteria, then make the change within the
   item's scope.
3. Run the tests and the acceptance checks locally. Keep the commands and their output.
4. Update the affected documents. Open the pull request.
5. Run `python3 tools/verify_status.py docs/backlog.md`. It must exit 0. Set status `in-review`.
6. Send the reviewer brief (change and acceptance criteria, never your reasoning) to an
   independent reviewer. Attach the findings. If the reviewer or approver sends it back, set
   status `in-progress`, record the findings and return to step 2.
7. **Change gate.** Ask for approval of the exact change and pull request description. Record it.
8. Merge only after the change gate approval, which is the record for the merge. Set status
   `merged` (merged, not yet verified in the target environment).

## Phase 3: release (started by a human)

1. Count the expected changes again and compare them with the planned ones, item by item.
2. First production release: pass the launch-readiness gate.
3. **Release gate** (irreversible), before the action: the approver and a second human approve
   the exact action. Record both.
4. A human starts the action, or explicitly lets you start that exact action.
5. Verify the result against the live system, not against a status report. A system reporting its
   own success is not evidence.
6. Write the done entry: Evidence (link or path), Evidence kind, Approvals. Then set status `done`.
7. Run `python3 tools/verify_status.py docs/backlog.md`. It must exit 0 before the status change
   is published. Then close the item.

A shared item that deploys to a non-production environment through an automatic pipeline after
merge needs no release gate if the change gate approval names that deploy.

## Stop rules

Stop, report, and wait for a human when any of these happens:

- a gate is not approved, or the answer is no (a refusal stands);
- the next step is an irreversible action without a recorded approval;
- the item needs a decision nobody has made;
- the same check fails twice for the same reason: write a root-cause note in the item and stop;
- five iterations of the same step without progress (three when one agent builds and another judges);
- the item's cost passes its budget in `docs/ai-stance.md`;
- the change needs to touch something outside the row's scope;
- production personal data would enter your context.

## Status values

`proposed`, `ready`, `in-progress`, `in-review`, `merged`, `done`, `blocked`, `dropped`.

- `blocked` (from any status before `done`) needs Blocked by with the blocker and a date; when
  the blocker is resolved, the item returns to the status it had before.
- `dropped` needs a reason and who decided; anything merged or released is reverted or recorded
  as left in place.
- `done` and `dropped` are final. Reopening means a new item that links to the old one.
- Hitting a stop rule moves the item to `blocked`, with the root-cause note as the blocker.

## Rules from incidents

- Measure a baseline before you change anything.
- A system reporting its own success is not evidence.
- Count the expected changes again before release instead of trusting an estimate.
- Write the done entry before the item is closed.
- If a human refuses a permission, the answer stands.
- <!-- add one line per incident, with the date -->
