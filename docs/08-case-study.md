# Case study: where the method came from

The method in this guidebook was not designed first and applied later. It was extracted from
one project, after the fact, by looking at what was built, when, and why. This page tells that
story. It is the main source for writing about the method. The client, product, people and
vendors are deliberately not named, and the numbers are rounded.

## The project

The evidence comes before the method, and this project is the clearest example of the process
working. The conditions were hard. It started from a client handover archive, and the external
approvers had little time. Many AI sessions shared one code checkout across three different AI
tools, and there were only five and a half weeks. One engineer directing AI agents rebuilt the
cloud foundation anyway. The backlog of about 100 work items covered both the work in scope and
the roadmap after it. Everything in scope was done, each item with evidence from the live
system, plus about 300 commits and over 100 single-use git worktrees.

- **Starting point:** a client handover archive with three applications, one external
  integration, an early infrastructure template, and loose notes.
- **Goal:** rebuild the cloud foundation with no stored secrets, and get the applications
  running in development, test and production while the client's own developers kept working.

The project called its backlog the **runbook**. Each row was a small work item with its own
acceptance check and, once done, a link to the evidence. The runbook is what people saw from the
outside. The process that produced it is what this guidebook describes.

## How each stage appeared

Stage numbers follow [the method reference](03-method.md). Stage 0 (AI stance) did not exist as
a separate artifact on this project; the client's rules on secrets and data were written into
the context file as invariants.

| Stage | What happened | What triggered it |
|---|---|---|
| 1 Situation analysis | On day 1 the archive was unpacked and compared with what the client had described. The "infrastructure" was a generic template, not a design, and the plan changed because of it. | Inputs of unknown quality |
| 2 Context file | One context file, linked under the file name each of the three AI tools reads. Invariants included "no stored secrets" and "done means verified by a command". | Repeating the same instructions to every session |
| 3 Roles | About 20 agent roles and a dozen skills, grown over several weeks. Reviewers received the change and the acceptance criteria, never the author's reasoning. | Authors approving their own work |
| 4 Phased plan | A seven-phase gated plan, and one bundled request pack for the external administrators, sent on day 5. | Slow external approvals |
| 5 Backlog | The runbook grew from about 30 rows to about 100. | "Mostly done" work nobody could account for |
| 6 Work isolation | One new git worktree per work item. | Several AI sessions switched branches in the same shared checkout |
| 7 Standard procedure | For the first week every item was run by hand. On day 9 the cleanest end-to-end run (around row 40 of the backlog) was written down as the procedure, and refined after every incident. | The same twenty small decisions on every item |
| 8 Status verification | An audit on day 10 found rows marked done that weren't. A verification script existed a day later. The same approach was later applied to the release process, with each release milestone checked against the live system. | False "done" |
| 9 Retrospective | An audit on day 19 found about three dozen problems in the method's own instructions, a third of them high severity, such as instructions that pointed at deleted components. | Instructions describing a project that had moved on |

## Timeline (relative days)

| Day | Event |
|---|---|
| 1 | Handover archive received; gap analysis |
| 3 to 4 | Skills, roles and the context file written |
| 4 to 5 | Phased plan, first backlog, request pack for external approvers |
| 5 to 8 | One worktree per item and the single-owner rule, after collisions |
| 9 | Standard procedure written down from the best hand-run item |
| 10 to 11 | Audit of false "done" rows, then the status verification script |
| 12 | Backlog moved into the repository and shared with all AI tools |
| 15 to 30 | Same method applied to the release process, with its own verification script |
| 19 | Audit of the method itself, run during the release work |
| 39 | About 100 items planned; all in-scope work done with evidence, the rest the roadmap |

## What the case shows

The runbook (stage 5) only started producing results after stage 7. Until each row had a
standard procedure behind it, the backlog was just a plan.

From stage 3 on, each stage was added within days of a concrete failure. Stages 1 and 2 were
done up front because the project started from an archive and several AI tools. Nothing was
built for a failure that had not happened yet, which kept the overhead low. Because the method
was extracted while the project ran, each stage arrived right after its trigger. The
[anticipated triggers](03-method.md) let a new project start those stages earlier (untested
proposal).

The rules that mattered most were short and came from incidents:

- Measure a baseline before you change anything.
- A system reporting its own success is not evidence.
- Count the expected changes again before release instead of trusting an estimate.
- Write the done entry before the work item is closed, or it can get lost.
- If a human refuses a permission, the answer stands.

## Limits of the evidence

The case is a strong example of the method. What it cannot show is how far the method
generalizes:

- **One case.** One engineer, one client, one kind of work (rebuilding an existing system). The
  method has not been run on a new product, by a team, or under a regulated audit. The parts of
  this guidebook that cover those situations are design proposals, tested only as thought
  experiments ([gap report](../research/gap-report.md)).
- **Self-reported.** The history was reconstructed from the engineer's own files, commits and
  session logs. Nobody outside the project measured it.
- **No baseline.** There is no measurement of how the same project would have gone without the
  method. The numbers show what was delivered and verified, not how much faster the method made it.
