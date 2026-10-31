# Method rules for agents

The method: run a project with AI agents by adding process stages only when a named failure
(the trigger) shows up. Work moves through a backlog of small items with checkable acceptance
criteria, a standard procedure with human gates, and a script that refuses "done" without evidence.

Details for people: [docs/03-method.md](../docs/03-method.md) (stages),
[docs/05-work-item-procedure.md](../docs/05-work-item-procedure.md) (gates, risk tiers, evidence),
[docs/04-variants.md](../docs/04-variants.md), [docs/06-adoption-and-measurement.md](../docs/06-adoption-and-measurement.md).
Templates: [templates/](../templates/). This file is the short form; where it is silent, those win.

## Stages and their triggers

| # | Stage | Trigger (add the stage only when this has happened) |
|---|---|---|
| 0 | AI stance | Before any agent touches project data |
| 1 | Situation analysis | Inputs are scattered, contradictory or of unknown quality |
| 2 | Context file | More than one session or agent; you keep repeating yourself |
| 3 | Roles and separation of duties | Two agents change the same thing, or an author reviews own work |
| 4 | Phased plan with stage gates | Work starts before dependencies are ready; slow external approvals |
| 5 | Backlog | "Mostly done" piles up; nobody can say what is finished |
| 6 | Work isolation | Parallel work collides; changes leak between items |
| 7 | Standard procedure | Every item repeats the same small decisions; quality depends on who runs it |
| 8 | Status verification | An item was marked done when it was not; others rely on your status |
| 9 | Retrospective and harness maintenance | Instructions describe a situation that has changed |

## MUST

1. Default to the lowest maturity level that covers the work (level 1: stages 0 to 2; level 2 adds
   stages 4 and 5). Before adding any stage, name its trigger and where you saw it, in one sentence.
2. Treat numbers in examples (role counts, backlog sizes, days) as outcomes of one project, not
   targets.
3. Use the exact status values below and the backlog fields in `docs/backlog.md`.
4. Record a human approval before every irreversible action (list below), in the approval format.
5. Turn every choice a human has not made into a `decision` item with options, owner and deadline.
6. Give reviewers the change and the acceptance criteria only.
7. Verify against the live system or an independent check. Link the evidence.
8. If the project has `tools/verify_status.py`, run it on docs/backlog.md before publishing any
   status change; it must exit 0. Without it, check the evidence link by hand.
9. Work on one item per workspace; write only in your own workspace and your own area.
10. Ask the human only about real decisions; answer everything else from the files.
11. Record a baseline before changing anything you will measure.

## MUST NOT

1. Create artifacts, files, roles or skills for a stage whose trigger has not fired.
2. Generate all stages, all templates or a large role set up front.
3. Choose an option a human has not decided, or fill in the Decision section of an ADR.
4. Put production personal data, secrets or credentials in your context, prompts or files.
5. Pass your reasoning, chat history or self-assessment to a reviewer.
6. Count a system's report of its own success as evidence (a green pipeline badge, a "deployed"
   message, a re-run that passed with no code change).
7. Mark an item `done` without evidence and the approvals its risk tier needs.
8. Ask again in other words after a human refuses. A refusal stands.
9. Convert an inherited backlog in bulk; apply the fields when an item is pulled into work.
10. Keep a second backlog when a tracker exists; the file is a view of it.

## Irreversible actions

Each needs a recorded human approval for this item first, whatever the risk tier:

- deploy or apply to a shared or production environment;
- delete data or resources;
- merge to a shared branch;
- send anything to an external party;
- spend money;
- change permissions or secrets;
- edit an existing instruction or context file (including `AGENTS.md`, skills and this file);
- read production data with credentials.

## Risk tiers and gates

Phases: review ends at the plan gate, build at the change gate, release at the release gate.

| Risk tier | Meaning | Gates before done |
|---|---|---|
| local | Reversible, only the item's own workspace | change (always, before merge) |
| shared | Shared code, environments or other people | plan, change |
| irreversible | Cannot be undone; production, money, personal data, regulated scope | plan, change, release from two distinct humans (the second not the owner or author) |

When unsure, go up one tier. Every gate comes before the action it approves. An agent reviewer
adds findings and never replaces the human approval. Also: `launch-readiness` before a first
production release, `evidence` for inferential evidence, `expedite` on the incident path (stands
in for plan, change and release; the backfill adds a second human's release approval within 48
hours).

Approvals cell (index): `plan:alice@2026-10-01; change:bob@2026-10-02`. Full record: one line
`gate | item | who | when | what exactly was approved | link` in `docs/approvals.md`.

## Status values and transitions

`proposed`, `ready`, `in-progress`, `in-review`, `merged`, `done`, `blocked`, `dropped`.

- `ready` to `in-progress`: review done; shared or irreversible need a `plan` approval first.
- `in-review` to `merged`: a `change` approval dated before the merge, every tier.
- `merged`: merged, not yet verified in the target environment. Never report it as done.
- `merged` to `done`: evidence in the target environment; irreversible needs `release` (or
  `expedite`) approvals from two distinct humans; inferential evidence needs an `evidence` approval; decision items link an ADR.
- `blocked`: Blocked by names the blocker and a date; it returns to its previous status.
- `done` and `dropped` are final; reopening means a new item.

## Default paths

| Artifact | Path | Stage |
|---|---|---|
| AI stance | `docs/ai-stance.md` | 0 |
| Situation analysis, decision log | `docs/situation.md` | 1 |
| Context file | `AGENTS.md` | 2 |
| Roles, gate owners | `docs/roles.md` | 3 |
| Plan | `docs/plan.md` | 4 |
| Backlog (or view of the tracker) | `docs/backlog.md` | 5 |
| Approval log | `docs/approvals.md` | 5 |
| Decisions | `docs/decisions/NNNN-title.md` | any |
| Standard procedure | `.agents/skills/work-item/SKILL.md` | 7 |
| Status verification | `tools/verify_status.py` | 8 |

Copy from `templates/`; create a file only when its stage is in use.

## When asked to "run item N"

- No backlog exists: run stages 0 to 2 (level 1): `docs/ai-stance.md`, `docs/situation.md`,
  `AGENTS.md`. Then stop at the gate: present them and ask which stages to add.
- Backlog exists, no standard procedure: follow the review, build and release phases from
  [docs/05-work-item-procedure.md](../docs/05-work-item-procedure.md) by hand, with the gates.
- Both exist: follow `.agents/skills/work-item/SKILL.md`.

## Setup done condition and stop rules

Setup is done when the files for the chosen stages exist and
`python3 tools/verify_status.py docs/backlog.md` exits 0 (if a backlog is in use).

Stop and report to a human when:

- you reach 5 iterations of the same setup or build loop (3 for a loop where one agent builds and another judges);
- the same failure happens twice: stop, write a root-cause note (what failed, the evidence, the
  cause, the proposed fix) in the item or `docs/situation.md`, and wait;
- the next step is an irreversible action without a recorded approval;
- a decision is needed that nobody has made;
- the cost budget in `docs/ai-stance.md` is reached;
- the work needs a stage whose trigger you cannot name.

"Looks done" is not a stop condition. Done is the check command and its exit code.
