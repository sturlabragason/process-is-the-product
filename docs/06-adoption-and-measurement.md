# Adoption and measurement

This part covers how much of the method to use, when to add or remove a stage, how to tell
whether the method helps, and how to bring other people into it. The stages themselves are in
[03-method.md](03-method.md). Gates, risk tiers and evidence rules are in
[05-work-item-procedure.md](05-work-item-procedure.md).

**Read this first.** The method comes from one project: one engineer directing AI agents for
about five and a half weeks (see [08-case-study.md](08-case-study.md)). Everything in this part
that goes beyond that setting is an **(untested proposal)**. That includes the regrouped maturity
levels, the removal rule, the metrics, the review point and all of the change management for
teams. Nobody has run these on a real project yet. Treat them as a starting design and tune them
with your own data.

Gaps closed here: B4, C6, C13, D4 and E12 from the gap report.

## The default: as little method as solves your current failures

Each stage exists because of a specific failure. If you do not have that failure, you do not need
the stage. Three rules follow.

1. **Start at the lowest level that solves the failures you have today.** For most new work that
   is level 1 or 2. An agent setting up the method follows the same rule (see
   [../agent/METHOD.agent.md](../agent/METHOD.agent.md)).
2. **Name the trigger before you add a stage.** Write one line in the decision log: the failure
   you saw, when, and which stage answers it. "It might be useful" is not a trigger.
3. **Example numbers are outcomes, not targets.** The case ended with about 20 agent roles, a
   dozen skills and about 100 work items. Those numbers describe what one project grew into over
   several weeks. A new project that starts with 20 roles is over-built.

The level is a bundle of stages that usually arrive together. The stage triggers still decide. If
a false "done" shows up while you are at level 2, add stage 8 then. You do not have to take all
of level 3 first.

## Maturity levels

This is a regrouping of the levels in the original method (untested proposal). The original
put stage 3 (roles and separation of duties) at level 2, before its trigger, which is parallel
work or an author reviewing their own work. Here it moves to level 3, next to work isolation,
because both answer the same failure. Stage 0 (AI stance) did not exist in the original and is
added at level 1 with a condition.

| Level | Stages | Move here when |
|---|---|---|
| 0 Ad hoc | none | You are exploring an idea alone |
| 1 Briefed | 0 (conditional), 1, 2 | More than one session, agent or person is involved |
| 2 Planned | 4, 5 | The work takes more than a week or has external dependencies |
| 3 Factory | 3, 6, 7 | Work runs in parallel, items repeat, or someone reviews their own work |
| 4 Self-verifying | 8, 9 | Other people rely on your status |

### Level 0: ad hoc

- **What you have:** chat sessions with an AI tool, results copied by hand. No files that
  belong to the method.
- **Trigger to move up:** a second session, agent or person needs to pick up the work, or you
  catch yourself explaining the same background twice.
- **Signs you are over-built:** not applicable. The risk at level 0 is staying too long, not
  building too much.

### Level 1: briefed

- **What you have:** a situation analysis (`docs/situation.md`) and a context file
  (`AGENTS.md`). On existing work the analysis is a gap analysis; on new work it is an
  assumption register. Stage 0, a written AI stance (`docs/ai-stance.md`), is **required** as
  soon as more than one person is involved or any non-public data is in reach of an agent. Solo
  work on public data can skip it.
- **Trigger to move up:** the work will take more than a week, or depends on someone outside
  your control, such as an approver, a vendor or another team.
- **Signs you are over-built:** the context file is longer than a new agent can use, or lists
  roles nobody plays. The situation analysis covers areas no current item touches. You wrote a
  plan with phases for a few days of work.

### Level 2: planned

- **What you have:** a phased plan with gates (`docs/plan.md`) and a backlog of small items with
  acceptance criteria (`docs/backlog.md`, or a view of the tracker you already use). Long-lead
  requests go out early.
- **Trigger to move up:** two agents or people change the same thing, the same kind of item
  keeps coming back, or an author starts approving their own work.
- **Signs you are over-built:** the plan has more phases than the project has dependencies.
  Backlog items carry fields nobody fills in or reads. Items are split so small that writing the
  acceptance criteria takes longer than the work.

### Level 3: factory

- **What you have:** a role list with one owner per area and independent reviewers
  (`docs/roles.md`), one isolated workspace per item, and a standard procedure written down
  from the best run done by hand (`.agents/skills/work-item/SKILL.md`).
- **Trigger to move up:** someone other than you reads your status to make a decision, or an
  item is reported done when it is not.
- **Signs you are over-built:** roles with no items assigned in the last few weeks. Skills that
  no item has loaded. A standard procedure written before any item was run by hand. Every item,
  however small, goes through all three phases of the procedure.

### Level 4: self-verifying

- **What you have:** fixed status values, a status verification script (`tools/verify_status.py`)
  that runs before any status is published, and a regular audit of the method's own documents.
- **Trigger to move up:** none. From here you tune and remove, you do not add levels.
- **Signs you are over-built:** the verification script checks fields no decision depends on.
  The method audit runs so often that it finds nothing. Status reports are produced that nobody
  reads.

## Removing process

Process tends to grow. Every incident adds a rule, and no rule leaves on its own. The method
needs a way out as well as a way in (untested proposal).

- **Review every rule and stage at the fixed review point** (see below) and at each stage 9
  audit. For each one, ask: did it fire, and did it catch anything?
- **Remove or simplify a rule that has not fired or caught anything in an agreed period.** The
  default is four to six weeks of active work. Tune it: a rule guarding a rare, costly event
  (a production deploy, a payment, personal data) may fire once a quarter and still earn its
  place. Write the removal in the decision log with the reason, so it can come back if the
  failure does.
- **Keep small, reversible changes light.** A change in the *local* risk tier (reversible,
  affects only its own workspace) already has one gate, the change gate, not three. Optionally set
  a size limit, for example a number of changed lines or files, above which a local change is
  treated as `shared`, and write it in the context file. The tiers and their gates are defined in
  [05-work-item-procedure.md](05-work-item-procedure.md).
- **Prefer simplifying to deleting when a rule has caught something.** Merge two overlapping
  checks into one, or move a manual check into the verification script so it costs nothing to
  run.
- **Never remove these to save time:** humans start irreversible actions, done needs evidence,
  and reviewers get the acceptance criteria rather than the author's reasoning. These held up in
  all three simulated reviews of the method. If they feel slow, fix the gate, not the rule.

## Measuring whether the method helps

The method tells you to measure a baseline before you change anything. That applies to adopting
the method itself (untested proposal). Without a baseline, the review after six weeks is an
opinion.

### Baseline first

Before you add any stage, collect two sprints or two to four weeks of the measures below for the
work as it runs today. Much of it can be pulled from version control, the CI system and the
tracker history, so it does not have to delay the start by much. Record where each number came
from, so the same query can run again at review time.

### DORA's software delivery metrics

Use the software delivery metrics as DORA names them:

- **Change lead time**
- **Deployment frequency**
- **Failed deployment recovery time**
- **Change fail rate**
- **Deployment rework rate**

Measure them per application or service, the same way before and after. If the work does not
deploy software (see [07-beyond-software.md](07-beyond-software.md)), skip these and keep the
method measures.

### Method measures

These measure the things the method claims to fix.

| Measure | How to count it | What the method should do to it |
|---|---|---|
| False-done rate | Share of items marked `done` in the period that fail status verification. For the baseline, check a sample of done items by hand for linked evidence from the target environment. | Fall sharply once stage 8 is in place |
| Gate wait time | Time from an item asking for approval at a gate to the approval being recorded. Report the median and the worst case. | Stay flat or fall. If it grows, gates have become the bottleneck |
| Rework rate | Share of done items reopened, or needing a follow-up fix for the same acceptance criteria, within a set window such as two weeks | Fall |
| Items done with evidence per week | Count of items that reached `done` and pass the verification script | Rise, or stay flat while rework falls |
| Cost per item | Agent spend (tokens or bill) plus human hours, divided by items done with evidence | Stay within the budget in the context file |

Keep the measures at team or workstream level. Do not rank people by them. Once a number is used
to judge a person, it stops telling you about the process.

### Review at a fixed point

Pick the review date before the pilot starts: after two sprints or six weeks, whichever comes
first. At the review, compare against the baseline and decide one of three things.

- **Keep and extend.** False-done rate and rework are down, items done with evidence are flat or
  up, and DORA's metrics have not got worse. Keep the stages that fired and consider a second
  team.
- **Simplify.** The method measures improved, but gate wait time grew, or cost per item rose
  more than the rework it saved. Move more items into the local tier, raise the size limit, or remove
  the stage added last and watch whether its failure returns.
- **Stop.** After six weeks, false-done rate and rework have not improved, throughput fell, and
  people spend noticeable time on the method's own files. Go back to the lowest level that still
  helped, or drop the method. Write down why. That is a useful result too.

Two cautions. Six weeks is short, and the first weeks include the cost of learning, so a small
dip in throughput is expected. And one team's numbers are a case, not a proof, the same limit
that applies to the original project.

## Bringing people in

Everything in this section is an (untested proposal). The original project had one engineer, so
there were no people to convince. The gap review found this was a high-severity gap for any
team.

### Start with a pilot

- **One team or one workstream.** Pick one where a trigger is clearly firing, such as false
  status or collisions between parallel work, so the method has a failure to fix.
- **Opt in.** People in the pilot chose to be there. Nobody outside it is asked to change how
  they work until the review.
- **Show the baseline at the start and the results at the review.** Share both with the pilot
  team and with the teams watching. If the results are poor, share those too.
- **Adopt from your own level.** A second team starts at the level its own failures call for,
  not at the level the pilot reached.

### Personal prompt files

In a team that already uses AI, people usually have their own instruction files, and some of them
contradict each other. Merge them into the shared context file through review, not by decree.

1. Collect the personal files the pilot members are willing to share.
2. Sort each instruction into one of two kinds. **Invariants** are rules about the project: what
   must never happen, how done is proved, which data an agent may see. **Style** is personal: tone,
   verbosity, preferred editor commands.
3. Propose the invariants as a change to the context file. It goes through the normal review,
   with the context file owner approving. Conflicts between people are settled there, in the
   open.
4. Style can stay in a personal overlay file. An overlay may add style. It may never weaken or
   override an invariant from the context file. If it does, the shared file wins.

The context file is treated as code: it has an owner and every change is reviewed (see
[03-method.md](03-method.md), stage 2).

### Skeptics

Some people will think the method is overhead. Some of them will be right about parts of it.

- **Ask for their failure, not their agreement.** If they cannot name a failure the method would
  fix for them, they may not need it yet.
- **Answer with the baseline and the review, not a mandate.** "We will measure it for six weeks
  and stop if it does not help" is a better argument than a rule from above.
- **Give them a reviewer role.** A skeptic is a good independent reviewer at a gate, and a good
  person to run the removal review.
- **Let them propose removals.** If a rule has not fired, they should be able to cut it through
  the decision log.

### The method owner

One person owns the method in a team, separate from owning the work items. The role is part
time. The method owner:

- keeps the baseline and runs the review at the agreed date;
- owns the decision log for adding and removing stages and rules, and checks that each addition
  names its trigger;
- runs or schedules the stage 9 audit of the method's documents;
- is the default owner of the context file, or names one;
- collects incidents and turns the repeated ones into rules in the standard procedure;
- watches gate wait time and raises it when human review becomes the bottleneck.

The method owner does not approve every gate. Gate owners are set per gate type in
[05-work-item-procedure.md](05-work-item-procedure.md), and team variants are in
[04-variants.md](04-variants.md).

## When the method is not worth it

Some work is too small for any of this. Stay at level 0, or level 1 at most, when the work is:

- **Tiny:** a change you can make, check and undo in under an hour.
- **Short:** a few days in total, with no external approvals and no dependencies on other
  people.
- **Solo on public data:** one person, no shared code or environment, nothing an agent could
  leak.
- **Throwaway:** a spike, prototype or experiment that will be deleted, not shipped.

Two habits are cheap enough to keep even then. Do not call something done until you have seen
it work. And if the throwaway work turns out not to be throwaway, that is a trigger: start at
level 1 with a situation analysis of what you built.
