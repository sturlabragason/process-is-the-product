# Variants: greenfield, joining mid-flight, teams, regulated work

The method was taken from one project: one engineer directing AI agents on a brownfield
project, started on day 1. This file shows how to apply it in four other situations.

**Status of this file.** Everything here that goes beyond that original project is an
**untested proposal**. It comes from three simulated runs recorded in
[the gap report](../research/gap-report.md), not from real projects. Treat it as design, not
experience, and measure it the way [adoption and measurement](06-adoption-and-measurement.md)
describes.

Stage numbers and names follow the [method reference](03-method.md). Gates, risk tiers, the
expedite path and evidence rules live in the
[work item procedure](05-work-item-procedure.md). This file links to them rather than
repeating them.

## Pick your starting point

| Your situation | Start here | Read next |
|---|---|---|
| New product, nothing exists yet | Stage 0 AI stance, then stage 1 as an assumption register, then the walking skeleton as item 0 | [Greenfield](#greenfield), [method reference](03-method.md) |
| A project is already running and you are joining it | The stage that prevents your costliest current failure | [Joining mid-flight](#joining-mid-flight), [adoption and measurement](06-adoption-and-measurement.md) |
| More than one human works on the project | Stage 3 roles, then stage 6 work isolation at team level | [Teams](#teams), [work item procedure](05-work-item-procedure.md) |
| The work is regulated or will be audited | Stage 0 AI stance with data classes, then the evidence rules | [Regulated or audited work](#regulated-or-audited-work), [work item procedure](05-work-item-procedure.md) |
| Several of the above | Combine the sections; the stricter rule wins where they differ | All four sections below |

One rule holds in every variant: add a stage when its trigger occurs, not before. Each variant
changes the order and the starting point. None of them is a reason to build all ten stages on
day 1. The agent rules in [METHOD.agent.md](../agent/METHOD.agent.md) say the same thing in
MUST and MUST NOT form.

## Greenfield

### When this applies

A new product: no code, no environment, no backlog, and often no chosen vendors. A gap analysis
needs a current state; here it is empty, so its exit criteria pass without telling you anything.

### Stages and order

1. **Stage 0 AI stance.** Decide which tools are approved and which data classes may enter
   agent context before any agent touches the work.
2. **Stage 1 as an assumption register** at `docs/situation.md`. List what you believe about
   users, scope, vendors, volumes, budget and rules. Give each assumption an owner and a test.
   Order them by risk, riskiest first.
3. **Stage 4 phased plan, started early** at `docs/plan.md`, for anything with a lead time over a
   week.
4. **Stage 5 backlog** at `docs/backlog.md`, with the walking skeleton as item 0.
5. **Stage 2 context file** at `AGENTS.md`, kept short and grown as decisions land.

Stages 3 and 6 to 9 come later, when their triggers fire.

### What changes from the default

- **An assumption register replaces the gap analysis.** Stage 1 exits when every assumption has an
  owner and a test. The riskiest one is tested first.
- **The walking skeleton is item 0.** Before any feature, build the thinnest path from commit to
  a running environment: version control, CI, one environment, one deploy, one health check.
  "Verify against the live system" cannot work until something live exists. Until then, define
  done per environment, and record which environment each piece of evidence came from.
- **Undecided vendors become decision items.** Each open choice is a backlog item of type
  `decision`, linked to an ADR at `docs/decisions/NNNN-title.md`, with an owner and a deadline.
  Build items that depend on it list it under Blocked by. Nygard describes ADRs as "a collection
  of records for 'architecturally significant' decisions" [Nygard].
- **A discovery loop feeds the backlog.** Items of type `discovery` test an assumption with real
  users or real data. What they find becomes a proposed change to the backlog, and the product
  owner approves it at a gate. Findings never edit the backlog directly.
- **Long-lead items start in week 1.** Accounts, contracts, data agreements, security reviews
  and approvals take weeks. Stage 4's normal trigger (a slow approval blocks you late) fires too
  late here, so treat it as anticipated and send the request pack in week 1.

### First two weeks

| Day | Do this |
|---|---|
| 1 | Write `docs/ai-stance.md`: approved tools, allowed data classes, no production access. Run a short pre-mortem: "it is week 8 and we failed; why?" Each answer becomes an assumption. |
| 2 | Write the assumption register. Order by risk. Give each one an owner and a test. |
| 2 to 3 | List every long-lead item (accounts, contracts, approvals, data agreements). Send the request pack. Record each request as a backlog item with the date sent. |
| 3 | Open a decision item for each undecided vendor, with an owner and a deadline. |
| 3 to 5 | Build the walking skeleton (item 0). Exit when a trivial change goes from commit to a running environment through CI, and a check against that environment passes. |
| 5 | Write the first `AGENTS.md`: layout, invariants, the decisions made so far. |
| 6 to 8 | Run the first discovery items against the riskiest assumptions. |
| 8 to 10 | Write the first backlog rows for the features the discovery did not rule out. Run items by hand. |
| 10 | Review: which assumptions were tested, which decisions are overdue, which requests have no reply. Chase the overdue ones. |

### Pitfalls

- **The agent picks the vendor.** Asked to "set up auth", an agent picks a default provider and
  builds on it. That is a decision nobody made. Rule: agents never choose an option a human has
  not decided. If the decision item is open, the build item is `blocked`.
- **The agent builds features before the skeleton.** It will produce screens and endpoints that
  have never run anywhere. Nothing is `done` until it runs in an environment.
- **The agent writes assumptions as facts** ("users want X"). Each row needs a test and an owner.
- **Over-building.** An agent told "use the method" creates all ten stages on day 1. Stay at
  the lowest level that covers your triggers.

## Joining mid-flight

### When this applies

The project is already running: code, a tracker, CI, a review habit, people busy delivering.
The original method assumed stage 1 on day 1. Here you start where the costliest failure is.

### Stages and order

1. **List the triggers that are already firing.** Go through the trigger of each stage in the
   [method reference](03-method.md) and mark each one as firing, not firing or unknown. A firing
   trigger has a concrete recent example: an item marked done that was not, two people
   overwriting each other, an approval that blocked a release.
2. **Rank them by cost:** time lost, incidents, rework or audit exposure, from numbers you can
   find.
3. **Start at the stage that prevents the costliest failure.** If false status is costing most,
   start at stage 8. If collisions are, start at stage 6. Stages are not adopted in order here.
4. **Scope stage 1 to one workstream.** Do the situation analysis for the workstream where the
   costliest failure sits. A full analysis of an 18-month-old product takes weeks and blocks
   nothing useful.
5. **Write a short context file** for that workstream.

### What changes from the default

- **Delivery does not stop.** The method is adopted alongside the work in progress. No freeze, no
  "process sprint". Each stage is introduced on the next item that passes through it.
- **Retrofit onto existing artifacts.** Map the method onto what is already there before adding
  anything:

  | Method part | Existing artifact it maps onto |
  |---|---|
  | Backlog (stage 5) | The tracker. Add the missing fields there. |
  | Change gate | Existing pull request review and code owners |
  | Status verification (stage 8) | A CI job or a scheduled check that reads the tracker |
  | Context file (stage 2) | The existing README or contributing guide, plus `AGENTS.md` that points to it |
  | Decision log | Existing ADRs or design docs, if any |

  Add a new artifact only where nothing exists to map onto.

- **Personal prompt files** may stay for style. Invariants live only in the shared context
  file.

#### One system of record (A4)

The backlog schema is a set of fields, not a file. The fields are listed in the
[method reference](03-method.md) and the [templates](../templates/). If a tracker exists, the
backlog is a view of it: a saved query, a board or a generated report. `docs/backlog.md` is only
the default when there is no tracker.

Never keep two. A file next to a tracker drifts within days and nobody knows which is true. If
the tracker lacks a field (Evidence, Risk tier, Evidence kind), add a custom field or a fixed
section in the description. If you cannot change the tracker, keep only the extra fields in a
file keyed by tracker ID, and let the tracker own status.

The status verification script then reads the tracker, not a file. See
[verify_status.py](../tools/verify_status.py) for the reference version and adapt its input.

#### Inherited backlog triage (A5)

An inherited tracker may hold hundreds of tickets of mixed quality. Rules:

- **Apply the schema only when an item is pulled into work.** At that moment, add owner, risk
  tier, acceptance criteria and the rest. Untouched tickets stay as they are.
- **Close stale, ownerless items by an agreed rule.** Agree the rule with the team first, for
  example "no owner and no update for 90 days". Close with a comment that says the rule and how
  to reopen. Never close by judgment item by item without a rule.
- **Never mass-convert or mass-rewrite.** A bulk edit destroys history, floods notifications and
  puts words in other people's tickets.

#### Old and new systems side by side (A6)

Mid-flight projects often have a half-finished migration.

- **The context file names the authoritative system per capability.** For example: "user
  accounts: old system is authoritative until cut-over; orders: new system is authoritative
  since cut-over." One line per capability, with the date it last changed.
- **The migration is its own workstream** with its own owner and backlog items. Each cut-over has
  dated criteria: what must be true, measured how, by when. A cut-over is an item at the
  *irreversible* risk tier.
- **Agents never route traffic or change the legacy system without a decision item.** Any change
  to the legacy system, to routing, or to which system is authoritative needs a decision item
  that a human has decided. The agent may prepare the change; a human starts it.

### First two weeks

| Day | Do this |
|---|---|
| 1 | Read the tracker, CI history and recent incidents. List each stage trigger as firing, not firing or unknown, with one example each. |
| 2 | Rank firing triggers by cost. Pick one workstream and one stage to start with. Agree this with the team lead. |
| 2 to 3 | Baseline what you will measure later (see [adoption and measurement](06-adoption-and-measurement.md)) before changing anything. |
| 3 | Write `AGENTS.md` for the chosen workstream: authoritative system per capability, invariants, where the tracker is. |
| 3 to 4 | Map the backlog fields onto the tracker. Add the missing fields. Agree the stale-ticket rule. |
| 4 to 10 | Introduce the chosen stage on the next items pulled into work, one at a time. Run them by hand. |
| 10 | Review against the baseline. Keep, change or drop the stage. Decide whether to add the next one. |

### Pitfalls

- **The agent rewrites the tracker.** Told to "apply the schema", it edits every ticket. Apply
  it only to items pulled into work.
- **The agent creates a second backlog.** It writes `docs/backlog.md` because that is the default
  path. If a tracker exists, the backlog is a view of it.
- **The agent "fixes" the legacy system** or switches a route. Not without a decided decision
  item.
- **The agent analyses the whole product** while delivery waits. Scope stage 1 to one
  workstream.

## Teams

### When this applies

More than one human works on the project, each directing agents. With one engineer, every gate
had one owner and humans could not collide. Now they can.

### Stages and order

1. **Stage 3 roles**, at `docs/roles.md`, before anything else: one owner per area, and who owns
   each gate.
2. **Stage 2 context file** as shared code with its own owner.
3. **Stage 6 work isolation at team level** (below).
4. **Stage 7 standard procedure**, with the gate owner matrix from the
   [work item procedure](05-work-item-procedure.md) written into it.

### What changes from the default

#### Team-level isolation (B7)

One worktree per item protects agents from each other on one machine. It does not stop two
humans from changing the same schema or API on separate machines. Add:

- **Short-lived branches.** One branch per item, merged quickly. Trunk-based development says
  "the branch should only last a couple of days" [TBD], and now counts "one developer and their
  coding agents" as one unit on a branch [TBD].
- **A CI merge gate.** Nothing merges to the shared branch unless CI passes on the merged result.
  Fowler: "should the integration build fail, then it needs to be fixed right away"
  [Fowler CI].
- **Contract tests between components.** Where one person's component calls another's, a test
  owned by the consumer runs in the provider's CI. A breaking change fails before merge, not in
  an environment.
- **Shared schemas and migrations have one owner.** Database schemas, migrations, shared message
  formats and public API definitions each have exactly one owner. Others propose changes as
  items; the owner merges them. Two people writing migrations in parallel is the collision this
  rule exists for.
- **The context file is code.** It has an owner, and changes go through review.

#### Who owns which gate

In a team the gates need named owners per risk tier. The matrix (who is responsible, who
approves, who is consulted) is in the [work item procedure](05-work-item-procedure.md). Map
existing pull request review and code owners onto the change approval gate rather than adding a
second review.

The author of a change never approves its gate. With agents this extends to the author's
agents: a reviewer gets the acceptance criteria, not the author's reasoning, and is a reviewer
that "never saw your conversation" [Anthropic BP].

#### Review capacity as a work-in-progress limit

Agents produce changes faster than people can review them. Human review is the bottleneck, so
treat it as one:

- Limit items in `in-review` per reviewer, for example three (the default in [05](05-work-item-procedure.md#human-review-capacity-is-a-work-in-progress-limit)).
- At the limit, authors stop starting items and help review, or take *local* tier items.
- Track gate wait time. If it grows, the limit is too high or the gate too heavy for the tier.

### First two weeks

| Day | Do this |
|---|---|
| 1 | Write `docs/roles.md`: one owner per area, one owner per shared schema, migration set and API. Name the context file owner. |
| 2 | Map gate owners per risk tier using the matrix in the [work item procedure](05-work-item-procedure.md). Map pull request review onto the change approval gate. |
| 2 to 3 | Turn on branch protection and the CI merge gate on the shared branch. |
| 3 to 5 | Add one contract test at the busiest boundary between two people's components. |
| 5 | Set the review work-in-progress limit. Start tracking gate wait time. |
| 6 to 10 | Run items through the procedure with the new gate owners. Note every gate that waited more than a day. |
| 10 | Review: gate wait time, collisions, review load per person. Adjust the limit and the owners. |

### Pitfalls

- **An agent approves its own author's work.** It is asked to "review and merge" and does both.
  The agent may review; a named human owns the gate.
- **An agent edits a shared schema or migration** because the item needed it. It must open an
  item for the schema owner instead.
- **Agents open pull requests faster than anyone reviews.** Without the limit, reviews become
  rubber stamps.

## Regulated or audited work

### When this applies

The work falls under a regulation, a contract with audit rights, or a control framework:
personal or health data, payments, financial reporting, or a scheduled audit.

### Stages and order

1. **Stage 0 AI stance with data classes.** Before an agent sees anything, decide which data
   classes may enter agent context, which tools are approved for which class, and that agents get
   no production access. The DORA AI Capabilities Model lists "clear and communicated AI stance"
   as one of its seven capabilities [DORA AI].
2. **Stage 1** for the regulated scope, including compliance items (threat model, data
   classification, data protection impact assessment) as early backlog items of type
   `compliance`.
3. **Stage 3 roles** with the human approvals the framework requires.
4. **Stage 8 status verification** with the evidence rules from the
   [work item procedure](05-work-item-procedure.md).

### What changes from the default

#### Agent reviewers and four-eyes rules (B6)

An agent reviewer adds to human approval. Where a regulation, contract or control requires a
human, it never replaces that human. Four-eyes, or maker-checker, means two people [SoD]. An
agent can be a third pair of eyes that shortens the human reviewer's list. It is not one of the
two.

Record the agent review (which reviewer, which version, when) as a finding linked from the pull
request or the Evidence field. The Approvals field holds only the human approval
(`gate:who@YYYY-MM-DD`). Changes that touch regulated scope are at the *irreversible*
risk tier, which already requires a second human.

#### Evidence an auditor can use

Evidence must be attributable, dated, immutable and retained for the audit window. Those rules,
and what counts as each, are in the [work item procedure](05-work-item-procedure.md). In short
for this variant:

- **Attributable:** who produced it and who approved each gate, by name, not "the agent".
- **Dated:** timestamped by the system that produced it, not typed by hand.
- **Immutable:** stored where it cannot be edited later, not a chat or a mutable wiki page.
- **Retained:** kept for the whole audit window, which often outlasts CI defaults.

Done still means verified against the live system. The auditing principle is evidence-based
[ISO 19011]: a status report is not evidence, and a system reporting its own success is not
either.

#### Evidence exists only from adoption onward

The method produces audit-grade evidence only for items run through it after adoption. Tell
auditors plainly: state the adoption date and show what is covered from then. Never backfill
evidence for earlier work. Reconstructed evidence presented as contemporary is worse than a known
gap.

#### AI stance covers data classes

`docs/ai-stance.md` lists each data class (for example public, internal, confidential,
personal, special category) with: may it enter agent context, which tools may process it, and
where output containing it may be stored. Production personal data never enters agent context;
agents use synthetic or masked data.

### First two weeks

| Day | Do this |
|---|---|
| 1 | Write `docs/ai-stance.md` with data classes. Get it approved by whoever owns compliance. |
| 1 to 2 | List the controls in scope and the human approvals each requires. Write them into `docs/roles.md`. |
| 2 | Open compliance items: threat model, data classification, data protection impact assessment. Assign owners. |
| 3 | Decide where evidence is stored, how it is made immutable, and how long it is kept. Check it covers the audit window. |
| 3 to 4 | Set the Approvals field format (gate, who, when). Mark regulated scope as the *irreversible* tier. |
| 5 | Record the adoption date. Tell the audit contact what will and will not have evidence. |
| 6 to 10 | Run items through the procedure. Check each evidence link is attributable, dated, immutable and retained. |
| 10 | Dry run: pick three `done` items and produce their evidence as an auditor would ask for it. |

### Pitfalls

- **The agent counts its own review as the second pair of eyes.** It writes "reviewed and
  approved" and moves the item on. Where a human is required, the item waits for the human.
- **The agent pastes real data into its context** to reproduce a bug. The AI stance forbids it;
  use masked or synthetic data.
- **The agent links mutable evidence**, such as a chat or a CI run that expires in 30 days.
- **The agent backfills evidence.** Asked to "make the audit trail complete", it writes
  approvals and dates for past work. Never. State the adoption date instead.

## Gaps this file closes

A1, A4, A5 and A6 (joining mid-flight), B7 (teams) and B6 (regulated work), from
[the gap report](../research/gap-report.md). The greenfield parts are defined in the
[method reference](03-method.md); this file only sequences them.
