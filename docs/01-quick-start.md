# Quick start

This page is for one person adopting the method on a project that already exists. It covers the
first hour and the first week, using the templates and their default paths. It gets you to
maturity level 1 in the first hour and level 2 by the end of the week (levels are defined in
[adoption and measurement](06-adoption-and-measurement.md)).

Starting from nothing, joining a running team project, or working with other people: read the
matching section in [variants](04-variants.md) first. It changes the order of the steps below.

The commands assume two folders. Set them once per shell:

```bash
GUIDE=/path/to/process-is-the-product   # this guidebook
PROJECT=/path/to/your/project           # the project you are adopting it on
```

## Before you start

Write one sentence: the failure you are seeing and where you saw it. For example "every agent
session starts from zero and I explain the same setup each time". That sentence is your trigger.
If you cannot write it, you probably do not need the method yet.

Copy only the files for the stages you are using. Copying the whole folder with
`cp -r "$GUIDE/templates/." "$PROJECT/"` works, but it brings files for stages you have no
trigger for, and it puts the gate checklists at the project root instead of next to the
standard procedure.

## The first hour

1. Copy the level 1 files. `cp -n` refuses to overwrite a file you already have; if `AGENTS.md`
   exists, merge the template into it by hand.

   ```bash
   mkdir -p "$PROJECT/docs"
   cp -n "$GUIDE/templates/AGENTS.md" "$PROJECT/AGENTS.md"
   cp -n "$GUIDE/templates/docs/ai-stance.md" "$PROJECT/docs/ai-stance.md"
   cp -n "$GUIDE/templates/docs/situation.md" "$PROJECT/docs/situation.md"
   ```

2. Fill in `docs/ai-stance.md` (stage 0). List the approved tools, the data classes and which of
   them may enter agent context, production access (none for agents by default), and the budget
   owner. You may skip this file only if you work alone on public data. Once a second person or
   any non-public data is involved, it is required.

3. Fill in `docs/situation.md` (stage 1). On an existing project this is a gap analysis: as-is
   with a pointer to evidence, to-be, and the gap, in separate sections. Delete the assumption
   register section. Limit it to the one workstream where your trigger sits. Start the decision
   log at the bottom.

4. Fill in `AGENTS.md` (stage 2). Remove the layout rows for files that do not exist yet. Keep the
   invariants short and checkable. Link `docs/ai-stance.md`. Name yourself as owner.

5. Test the context file. Start a fresh agent session, give it only `AGENTS.md`, and ask it to
   describe the project and the next piece of work. Fix whatever it gets wrong.

6. Check that no template comments are left:

   ```bash
   grep -c '<!--' "$PROJECT/AGENTS.md" "$PROJECT/docs/ai-stance.md" "$PROJECT/docs/situation.md"
   ```

   Every count should be 0.

That is level 1. Stop here if the work will take less than a week and nobody outside your
control is involved.

## The first week

### Day 2: plan and long-lead requests

If the work runs longer than a week or depends on someone outside your control, add the plan
(stage 4):

```bash
cp -n "$GUIDE/templates/docs/plan.md" "$PROJECT/docs/plan.md"
```

Write each phase with entry criteria, an owner and exit criteria. Make the first phase a walking
skeleton if the project cannot yet deploy to a test environment. List every request with a long
lead time (access, approvals, procurement) and bundle the ones for each external party into one
request pack ([template](../templates/request-pack.md)). Sending it is an irreversible action, so
record the approval first.

### Days 2 and 3: backlog and approval log

Add the backlog (stage 5) and the approval log that goes with its Approvals column:

```bash
cp -n "$GUIDE/templates/docs/backlog.md" "$PROJECT/docs/backlog.md"
cp -n "$GUIDE/templates/docs/approvals.md" "$PROJECT/docs/approvals.md"
```

Delete the example rows and the comments. If the project already has a tracker, do not keep a
second backlog: the backlog is a view of the tracker, and you add the missing fields there (see
[one system of record](04-variants.md#one-system-of-record-a4)).

Pull three to five items into the backlog, the ones you will work on this week. Do not convert
the whole inherited backlog. For each item, write acceptance criteria as a check with an
expected result and the environment it runs in, set the Evidence kind, and set the risk tier
with the three questions in [how to classify an item](05-work-item-procedure.md#how-to-classify-an-item).
When unsure, go up one tier.

When a choice comes up that nobody has made, open a `decision` item and an ADR:

```bash
mkdir -p "$PROJECT/docs/decisions"
cp -n "$GUIDE/templates/docs/decisions/0000-template.md" "$PROJECT/docs/decisions/0001-short-title.md"
```

### Days 3 to 5: run items by hand

Run each item through the three phases in the [work item procedure](05-work-item-procedure.md):
review (read-only), build, release. Do it by hand, with the agent, and note every decision and
check. Those notes become the standard procedure later.

- Record every gate approval twice: one line in `docs/approvals.md`, and a `gate:who@YYYY-MM-DD`
  entry in the item's Approvals cell. A `shared` or `irreversible` item needs a plan approval before it moves to
  `in-progress`, and every item needs a change approval before `merged`.
- Working alone, you approve the agent's plan and change; the agent is the author. An agent
  never approves. For an
  `irreversible` item, name a second human in the plan before the item reaches `ready`; you
  cannot be your own second human.
- Give each item its own branch. When a second session or agent runs alongside the first, switch
  to one git worktree per item (stage 6).
- When you want a review, send the [reviewer brief](../templates/reviewer-brief.md): the change and
  the acceptance criteria, never your reasoning.
- `merged` is not `done`. An item is `done` when its acceptance check has passed in the target
  environment and the evidence is linked.

[The worked example](02-worked-example.md) shows one item going through all of this.

### End of the week: check and decide

Run the guidebook's status script against your backlog. You do not need to install it yet:

```bash
python3 "$GUIDE/tools/verify_status.py" "$PROJECT/docs/backlog.md"
```

Fix the items it flags, not the script. Then look at your trigger sentence again. Did the
failure stop? Did a new one show up? Write the answer in the decision log. Record a baseline for
anything you want to measure later; [measuring whether the method helps](06-adoption-and-measurement.md#measuring-whether-the-method-helps)
lists candidates.

## What not to set up yet

Each of these has a trigger. Add it the day the trigger fires, not on day 1.

| Do not add yet | Add it when | Then copy |
|---|---|---|
| `docs/roles.md` (stage 3) | Two agents change the same thing, or an author reviews their own work | `cp -n "$GUIDE/templates/docs/roles.md" "$PROJECT/docs/"` |
| `.agents/skills/work-item/SKILL.md` (stage 7) | You have run several items by hand and the steps repeat. Write it from your cleanest run. | see below |
| `tools/verify_status.py` in the project (stage 8) | Other people rely on your status, or an item was reported done when it was not | `mkdir -p "$PROJECT/tools" && cp "$GUIDE/tools/verify_status.py" "$PROJECT/tools/"` |
| Audit checklist (stage 9) | Your instructions start describing a project that has moved on | `cp -n "$GUIDE/templates/audit-checklist.md" "$PROJECT/docs/"` |
| Twenty roles, a dozen skills, a hundred items | Never as a goal. These are what one project grew into. | |

The standard procedure and its gate checklists live in the same skill folder:

```bash
mkdir -p "$PROJECT/.agents/skills/work-item"
cp -n "$GUIDE/templates/.agents/skills/work-item/"*.md "$PROJECT/.agents/skills/work-item/"
```

Once the standard procedure exists, "run item B-001" is enough instruction for an agent. If you
direct agents to set up the method for you, give them [the agent rules](../agent/METHOD.agent.md),
which hold them to the same lowest-level default.
