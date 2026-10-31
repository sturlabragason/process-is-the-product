# The method, stage by stage

This is the reference for stages 0 to 9. Each stage opens with a table: purpose, trigger (the
failure that shows you need it), anticipated trigger (the sign the failure is coming), output with
its default path, and checkable exit criteria. Then come numbered steps, anti-patterns, and the
established practice it comes from. The long crosswalk is in
[09-why-it-works.md](09-why-it-works.md).

Add a stage when its trigger fires or is anticipated, not before. A small project may need only
stages 0 to 2. Which stages belong together, and when to move up, is in the maturity levels in
[06-adoption-and-measurement.md](06-adoption-and-measurement.md). Variants for greenfield work,
joining a running project, teams and regulated work are in [04-variants.md](04-variants.md). The
procedure for a single work item, with gates and risk tiers, is in
[05-work-item-procedure.md](05-work-item-procedure.md). Files to copy are in
[templates/](../templates/), and agents get the same rules in condensed form in
[agent/METHOD.agent.md](../agent/METHOD.agent.md). Terms follow [10-glossary.md](10-glossary.md).

The original project ran stages 1 to 9. Anything it did not use is marked "(untested proposal)"
where it first appears. Those parts are design, not experience.

## Stage 0. AI stance

| Part | Content |
|---|---|
| Purpose | Decide what agents may use, see and touch before they touch anything. DORA lists a "clear and communicated AI stance" as one of seven AI capabilities [DORA AI]. |
| Trigger | Someone pastes data into a tool nobody approved, an agent reaches production, or an unexpected bill arrives. |
| Anticipated trigger | Any project where agents will read code, data or tickets, from day 1. |
| Output | `docs/ai-stance.md` |
| Exit criteria | The file names the approved tools, the data classes allowed in agent context, who has production access, and the budget owner. The context file links to it. A newcomer can answer "may I put this data into this tool?" from the file alone. |

This whole stage is an untested proposal. The original project had invariants such as "no
stored secrets", but no written stance.

How to:

1. List the AI tools people and agents will use, and mark each approved or not approved. Note
   who approved it.
2. List the data classes the project handles (for example public, internal, confidential,
   personal, regulated). For each, say whether it may enter agent context. Production personal
   data may not, in any tool.
3. State production access: agents get none by default. A human starts every irreversible
   action (see risk tiers in [05-work-item-procedure.md](05-work-item-procedure.md)).
4. Name the budget owner and the spending limit for tokens and agent compute. Say what happens
   when the limit is reached: work stops and the owner decides.
5. Ask the person accountable for security or compliance to approve the file. Record who and
   when.
6. Link the file from the context file (stage 2) so every agent loads it.

Anti-patterns:

- A stance that lives in a chat message or someone's head.
- Giving an agent production credentials "just for this one task".

Established practice: acceptable use policy; data classification; least privilege; budget
ownership.

## Stage 1. Situation analysis

| Part | Content |
|---|---|
| Purpose | Find out what is actually true before planning. On existing work this is a gap analysis. On new work it is an assumption register. |
| Trigger | The inputs are scattered, contradictory or of unknown quality, or the plan rests on facts nobody checked. |
| Anticipated trigger | Day 1 of any project, or the day you inherit one. Run a pre-mortem then. |
| Output | `docs/situation.md`, with a dated decision log. Open choices become `decision` items (stage 5). |
| Exit criteria | Every input (brownfield) or assumption (greenfield) has an owner and a test, and every open question has an owner. |

On existing work (brownfield), write three separate sections: as-is (with evidence), to-be, and
the gap. Keep them apart, or a legacy workaround ends up described as the target. On the original project the handover
archive was compared with what had been described on day 1, and the "infrastructure" turned out
to be a generic template. The plan changed because of it.

On new work (greenfield), there is no as-is, so a gap analysis passes trivially. Use an
assumption register instead (untested proposal). Each row is a belief the plan depends on, with
an owner, a test that would prove it wrong, and a date. Sort it so the riskiest assumption comes
first: the one that is most uncertain and most expensive if wrong. The tests form a discovery
plan, and each test becomes a `discovery` item in the backlog.

How to:

1. Collect every input: archives, repositories, tickets, notes, contracts. List them in
   `docs/situation.md`.
2. Brownfield: for each area, write as-is with a pointer to evidence, then to-be, then the gap.
   Greenfield: write each assumption as one sentence that could be false.
3. Ask the agent to interview you until it "could write the spec" [Anthropic BP]. Mark every
   claim confirmed, unconfirmed or wrong.
4. Run a pre-mortem (untested proposal): assume the project failed, and list the likely causes.
   Each cause becomes an assumption, a risk with an owner, or an early backlog item.
5. If personal or regulated data is in scope, add `compliance` items for a threat model, data
   classification and a DPIA (data protection impact assessment) now (see stage 5).
6. Give every input, assumption and open question an owner and a test. Undecided choices
   become `decision` items.
7. Start the decision log: date, decision, who decided, why.

Anti-patterns:

- Planning from the description of the work instead of the work itself.
- A greenfield register with no tests, which is a wish list.
- Letting the agent fill gaps with plausible guesses.

Established practice: gap analysis [Gap]; requirements analysis; assumption mapping; pre-mortem;
decision log.

## Stage 2. Context file

| Part | Content |
|---|---|
| Purpose | Give every agent and person the same starting point: layout, roles, invariants and links. |
| Trigger | Every new session starts from zero, and you keep repeating yourself. Instructions contradict each other. |
| Anticipated trigger | A second session, agent, tool or person joins the work. |
| Output | `AGENTS.md`, linked under the file name each AI tool reads. |
| Exit criteria | A new agent can start useful work from the file alone. The file has an owner, and changes to it go through review. |

Context engineering "treats the context window as a design surface" [TW-CE]. On the original project one file was linked under the name
each of three AI tools reads. Its invariants included "no stored secrets" and "done means
verified by a command".

The context file is code (untested proposal for teams; the original project had one engineer).
It has an owner, it lives in version control, and every change goes through review like any
other change. Personal overlays (a person's own instruction file) are allowed for style, such as
tone or editor habits. They never add, weaken or override an invariant.

How to:

1. Write the repository layout and the invariants (rules that are never negotiated). Keep the
   invariants short and checkable.
2. Link `docs/ai-stance.md` and the other stage outputs once they exist. Link, do not copy.
3. Name the owner of the file and add it to the code owners or equivalent review rule.
4. Test it: start a fresh agent with only the file and ask it to describe the next work item.
   Fix what it gets wrong.
5. Keep it tool-neutral so any agent can load it [agents.md].

Anti-patterns:

- Invariants hidden in personal prompt files, where nobody else sees them.
- Editing the context file directly, without review, because "it is only docs".

Established practice: project charter; README and contributing guide; coding standards;
architecture decision records [Nygard].

## Stage 3. Roles and separation of duties

| Part | Content |
|---|---|
| Purpose | Make sure every area has one writer and that nobody approves their own work. |
| Trigger | Two agents change the same thing, or whoever did the work also reviews it. |
| Anticipated trigger | You plan to run work in parallel, or a change needs review by someone other than its author. |
| Output | `docs/roles.md`, plus skills that roles load when needed. |
| Exit criteria | For every area you can name its one owner and its reviewer. |

How to:

1. List the areas (repositories, environments, documents) and give each one owner, the single
   writer. Everyone else is read-only there.
2. Give each area a reviewer who is not the owner. Reviewer agents get read-only access.
3. Reviewers get the change and the acceptance criteria, never the author's reasoning. Use a
   reviewer that "never saw your conversation" [Anthropic BP].
4. Package repeated knowledge as skills, so a role loads only what it needs.
5. Name the human owner of each gate. Gate owners per risk tier are in
   [05-work-item-procedure.md](05-work-item-procedure.md); team-level four-eyes rules are in
   [04-variants.md](04-variants.md).

On the original project this grew to about 20 agent roles and a dozen skills over several weeks.
That is an outcome, not a target. Start with one owner and one reviewer.

Anti-patterns:

- A reviewer briefed with the author's plan, who then agrees with it.
- Twenty roles on day 1.
- An area with two owners "for speed".

Established practice: separation of duties [SoD]; maker-checker (four-eyes principle); code
owners; RACI.

## Stage 4. Phased plan with stage gates

| Part | Content |
|---|---|
| Purpose | Order the work so nothing starts before its dependencies, and slow requests leave early. |
| Trigger | Work starts before its dependencies are ready, or slow external approvals block you late. |
| Anticipated trigger | Anything with a lead time over one week: external approvals, access, vendor choice, procurement, legal review. Start this stage for those on day 1, even if the rest of the plan waits. |
| Output | `docs/plan.md` |
| Exit criteria | Every phase has entry criteria, an owner and exit criteria. Nothing can start before its dependencies are done. Every long-lead request has been sent. |

How to:

1. List the phases. For each, write entry criteria, an owner and exit criteria.
2. Make the first phase the walking skeleton (item 0, stage 5), so later phases can be verified
   in a real environment.
3. List every request that depends on someone outside your control. Note the expected lead
   time.
4. Bundle long-lead requests into one pack and send it as early as possible. On the original
   project one request pack for the external administrators went out on day 5.
5. Put `decision` items that block a phase before that phase, each with a deadline.
6. Treat each gate as a decision against stated criteria. Gates are "tough decision meetings"
   [Cooper], not status updates.

Anti-patterns:

- A plan with dates but no entry or exit criteria.
- Waiting until the build phase to ask for access.

Established practice: work breakdown structure [WBS]; critical path; stage-gate [Cooper];
long-lead items; release planning.

## Stage 5. Backlog

| Part | Content |
|---|---|
| Purpose | Turn the plan into small work items, each with a check that proves it done. |
| Trigger | "Mostly done" work piles up and nobody can say what is finished. |
| Anticipated trigger | The work will take more than a week, or more than one owner will pick items. |
| Output | `docs/backlog.md`, or a view of an existing tracker (one system of record, see [04-variants.md](04-variants.md)). |
| Exit criteria | Every item has acceptance criteria that a check can prove true or false, an owner, a Type and a risk tier. |

Each item has the fields ID, Title, Type, Status, Owner, Risk tier, Priority, Workstream, Scope,
Specification, Acceptance criteria, Evidence kind, Unblocks, Blocked by (with date), Evidence and
Approvals. Status values are listed in stage 8. Keep items "Small, Testable" [Wake]. On the
original project the backlog grew from about 30 items to about 100.

### Item types

- `build`: changes code, configuration or documents.
- `decision`: a choice a human must make, linked to an ADR in `docs/decisions/NNNN-title.md`.
- `discovery`: a question answered by evidence from users or experiments.
- `compliance`: work a law, standard or policy requires, such as a threat model or a DPIA.
- `ops`: running, auditing or maintaining the system and the method itself.

The types other than `build` are untested proposals. The original project kept decisions in a
log and had no separate types.

### Item 0: the walking skeleton

Item 0 is a walking skeleton (untested proposal): CI, the target environments and a deploy
path, with no features. Without it, nothing can be verified in a target environment until late,
and every item stops at `merged`. Define done per environment: each item's acceptance criteria names the environment it must be verified in, for
example "done in test" or "done in production".

### Decision items

When a choice is open (a vendor, an architecture, a data model), write a `decision` item with an
owner and a deadline, and link it to an ADR in Nygard's form: context, decision, status,
consequences [Nygard]. Agents must not choose an option a human has not decided. An agent may
research the options and draft the ADR with status "proposed". The human owner accepts it, and
only then can `build` items that depend on it become `ready`.

### Discovery loop

Findings from users change the backlog only through a gate owned by the product owner (untested
proposal). A `discovery` item states a question, a method (interview, prototype test, usage
data) and what answer would change the plan. The product owner decides what the finding changes
(add, change, drop, or nothing), recorded as a `plan` approval on each changed item. Agents do not edit the
acceptance criteria of a `ready` or `in-progress` item based on a finding.

### Security and privacy items

When personal or regulated data is in scope, add three `compliance` items early (untested
proposal): a threat model, a data classification, and a DPIA where the law requires one. Any
`build` item that touches that data lists them in Blocked by until they are `done`. These items
take the irreversible risk tier.

How to:

1. Break each phase into items small enough to verify in one sitting, with acceptance criteria
   written as a check, its expected result and the target environment.
2. Set Evidence kind: `computational` if a command can prove it, `inferential` if a human must
   judge it (rules in [05-work-item-procedure.md](05-work-item-procedure.md)).
3. Set the risk tier: `local`, `shared` or `irreversible`.
4. Fill Unblocks and Blocked by, so the order follows from the data.
5. Put a status summary at the top.

Anti-patterns:

- Acceptance criteria like "works well" with no check.
- Converting an inherited tracker in bulk. Apply the fields when an item is pulled into work
  ([04-variants.md](04-variants.md)).
- An agent picking a default where a `decision` item is still open.

Established practice: product backlog; work packages; acceptance criteria; Definition of Done
[Scrum]; INVEST [Wake]; working in small batches [DORA SB]; walking skeleton; ADRs [Nygard].

## Stage 6. Work isolation

| Part | Content |
|---|---|
| Purpose | Let items run in parallel without leaking into each other. |
| Trigger | Parallel work collides, or changes leak between tasks. |
| Anticipated trigger | A second item, agent or session will run at the same time as the first. |
| Output | One workspace per item with one owner, named after the item ID. For code, a git worktree on a short-lived branch. |
| Exit criteria | Nobody edits a shared workspace or someone else's. |

On the original project the rule came after several AI sessions switched branches in the same
shared checkout. From then on, every item got a new worktree.

How to:

1. When an item moves to `in-progress`, create a new worktree and branch for it. Only its owner
   writes there.
2. Keep the branch short. The established guidance is that "the branch should only last a couple
   of days" [TBD].
3. Remove the worktree after merge.
4. For collisions between people (schemas, migrations, contracts), see the team rules in
   [04-variants.md](04-variants.md).

Anti-patterns:

- Several sessions in one checkout.
- Reusing a worktree for a second item.

Established practice: short-lived feature branches; trunk-based development [TBD]; ephemeral
environments; permit to work.

## Stage 7. Standard procedure

| Part | Content |
|---|---|
| Purpose | Make every item follow the same steps, with human gates, so quality does not depend on who runs it. |
| Trigger | Every item repeats the same small decisions, and the same mistake happens twice. |
| Anticipated trigger | You have run a few items by hand and the steps are the same each time. |
| Output | `.agents/skills/work-item/SKILL.md` |
| Exit criteria | "Do item N" is enough instruction for a new agent to take an item from review to verified done. |

Run it by hand first, then codify the best run. "There can be no kaizen without a standard"
(Ohno, via [LEI]), and you cannot write a good standard before you have done the work. On the
original project every item was run by hand for the first week. On day 9 the cleanest end-to-end
run, around item 40, was written down as the procedure, and it was refined after every incident.

The procedure has three phases (review, build, release) with gates. The full text, including
risk tiers, the expedite path and evidence rules, is in
[05-work-item-procedure.md](05-work-item-procedure.md).

How to:

1. Run items by hand. Note every decision you make and every check you run.
2. Pick the cleanest complete run and write it down step by step.
3. Put the gates where a human must decide, and say what the human sees at each one.
4. Make it a skill that runs only when invoked, not on the agent's own initiative.
5. After each incident, add a rule. The rules so far:
   - Measure a baseline before you change anything.
   - A system reporting its own success is not evidence.
   - Count the expected changes again before release instead of trusting an estimate.
   - Write the done entry before the item is closed, or it can get lost.
   - If a human refuses a permission, the answer stands.
   - Humans start irreversible actions.
   - Reviewers get criteria, not reasoning.

Anti-patterns:

- Writing the procedure before running a single item.
- A procedure an agent can start on its own for irreversible work.

Established practice: standard work [LEI-SW]; checklists [Gawande]; CI/CD pipeline [Fowler CI];
PDSA [Deming]; poka-yoke [Poka]; blameless postmortems [SRE-PM]; after-action reviews [AAR].

## Stage 8. Status verification

| Part | Content |
|---|---|
| Purpose | Make reported status match reality, by checking evidence with a script. |
| Trigger | An item is marked done when it isn't, for example merged but never deployed, or "verified" by a cancelled pipeline run. |
| Anticipated trigger | Other people start relying on your status, or an agent updates status on its own. |
| Output | `tools/verify_status.py`, the fixed status values, and a map from each kind of change to the documents it affects. |
| Exit criteria | The script passes before any status change is published. |

The status values are exactly: `proposed`, `ready`, `in-progress`, `in-review`, `merged`,
`done`, `blocked`, `dropped`. `merged` means merged but not yet verified in the target
environment. `done` requires evidence from that environment.

Ask for "evidence: the command it ran and its output" [Anthropic BP]. A system reporting its own
success is not evidence: a green pipeline badge, an agent's summary or a status field is a claim.
Evidence is the check in the acceptance criteria, run against the target environment, with its
output.

On the original project an audit on day 10 found items marked done that weren't. The
verification script existed a day later.

How to:

1. Fix the status values in the backlog header and the context file.
2. Write the map: for each kind of change, which documents must change with it.
3. Install the script from [tools/verify_status.py](../tools/verify_status.py). It fails if a
   `done` item has no evidence link, or if a status is not one of the values above.
4. Run it before publishing any status change, and in CI. When it fails, fix the item, not the
   script.

Anti-patterns:

- "Done" meaning "I believe it works".
- A re-run that goes green with no code change, counted as success.

Established practice: Definition of Done enforced by automation; CI quality gates; deployment
verification; evidence-based auditing [ISO 19011]; eliminating toil [SRE-Toil].

## Stage 9. Retrospective and harness maintenance

| Part | Content |
|---|---|
| Purpose | Keep the method's own documents true as the project changes. |
| Trigger | The context file, roles or procedures describe a situation that has since changed. |
| Anticipated trigger | A phase ends, a system is replaced, or a fixed interval passes. Put the next audit date in the plan. |
| Output | Dated audit findings, each one filed as an `ops` item. |
| Exit criteria | An audit finds no high-severity stale instructions. |

How to:

1. Read the context file, roles, skills and procedure against the current state.
2. Flag instructions that "point at files that no longer exist, or contradict each other"
   [Anthropic BP].
3. Rate each finding by severity and file it as an `ops` item.
4. Remove rules that no longer earn their place. The removal rule is in
   [06-adoption-and-measurement.md](06-adoption-and-measurement.md).
5. Set the next audit date.

On the original project an audit on day 19 found about three dozen problems, a third of them
high severity, such as instructions that pointed at deleted components.

Anti-patterns:

- Audits that only add rules.
- Letting the agent that wrote the instructions audit them alone.

Established practice: retrospective [Scrum]; the Act step of PDSA [Deming]; document control;
docs as code.

## Failures each stage prevents

| Failure | Stage that prevents it |
|---|---|
| Data in an unapproved tool; agents with production access; an unowned bill | 0 AI stance |
| Planning on assumptions nobody checked; greenfield risks found late | 1 Situation analysis |
| Each agent re-learns the project; personal prompt files override invariants | 2 Context file |
| Authors approve their own work; two agents overwrite each other | 3 Roles and separation of duties |
| Work starts before its dependencies; long-lead requests sent too late | 4 Phased plan |
| Items stay "90% done"; agents pick options nobody decided; user findings change scope unseen | 5 Backlog |
| Parallel work collides; changes leak between tasks | 6 Work isolation |
| Quality depends on who runs the item; the same mistake happens twice | 7 Standard procedure |
| Optimistic or false status; `merged` reported as deployed | 8 Status verification |
| Instructions that describe last month's project | 9 Retrospective |
| No target environment to verify in until late | Item 0, walking skeleton (5) |
| An agent loop with no stopping rule | Machine-checkable acceptance criteria (5, 8) |
