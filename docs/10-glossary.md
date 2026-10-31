# Glossary

One term per concept. Where the field uses several names, the one used in this guidebook comes
first and the others are listed as synonyms.

| Term | Meaning | Synonyms or related terms |
|---|---|---|
| Acceptance criteria | The check an item must pass, and the result it must give, before it can be done | Definition of Done (team-wide), exit criteria (for a stage or phase) |
| Agent | An AI model running in a loop with tools, able to read, change and run things | Coding agent, AI assistant |
| Agentic engineering | Directing agents and overseeing their work, rather than doing every step yourself [Karpathy 2026] | Loop engineering [Osmani 2026b], vibe engineering [Willison 2025c] |
| AI stance | The agreed rules on which AI tools may be used, which data they may see, what access they get, and the budget (stage 0) | AI usage policy, acceptable use policy |
| ADR | Architecture decision record: a short file that records one significant decision, its context and its consequences [Nygard] | Decision record |
| Approval | A recorded human decision at a gate: gate, item, who, when, and exactly what was approved | Sign-off |
| Approval log | `docs/approvals.md`: one line per approval with gate, item, who, when, what exactly was approved and a link. The backlog's Approvals field is the index to it | Change log, decision log |
| Assumption register | A list of what a new project believes but has not checked, each with an owner and a test; the greenfield form of situation analysis | Risk register, hypothesis list |
| Backlog | The list of work items, each with the fields in [the template](../templates/docs/backlog.md) (stage 5). If a tracker already exists, the backlog is a view of it | Product backlog, work packages. The case study project called it the runbook |
| Context file | The one file every agent and new person loads first: layout, roles, invariants, links (stage 2). Default path `AGENTS.md` | `CLAUDE.md`, project charter, contributing guide |
| Decision item | A backlog item of type `decision`, for a choice a human has not made yet. Agents must not choose for them | Open decision |
| Evidence | A link or path to proof that an item meets its acceptance criteria. *Computational* evidence comes from a command or test; *inferential* evidence is a judged result such as interview notes, labelled as such and approved by a named human | Proof |
| Gap analysis | Comparing the current state (as-is) with the target state (to-be) to find the gap; the brownfield form of situation analysis [Gap] | Current-state assessment |
| Expedite | The incident path: the incident lead approves each action as it happens, and the paperwork is backfilled within an agreed window (default 48 hours). See [the procedure](05-work-item-procedure.md) | Emergency change |
| Gate | A decision point before an action, with stated criteria and a named human owner. Not a status update [Cooper] | Approval gate, stage gate, quality gate |
| Guides and sensors | Parts of the harness: guides steer an agent before it acts (instructions, context); sensors check after it acts (tests, scripts, reviews) [Böckeler] | Feedforward and feedback controls |
| Harness | Everything around an agent loop that steers and checks it: context, tools, skills, hooks, tests, scripts [Böckeler] | |
| Hook | A script the agent tool runs automatically at a set moment, for example before a command or when the agent tries to stop | |
| Invariant | A rule in the context file that is never negotiated, for example "no stored secrets" | Non-negotiable, constraint |
| Irreversible action | An action that cannot be undone or that affects others: deploy to a shared environment, delete, merge to a shared branch, contact an external party, spend money, change permissions or secrets, edit an existing instruction file, read production data | One-way door |
| Launch readiness | The checks before a first production release: monitoring, alerts, rollback and an owner on call. Recorded as a `launch-readiness` approval | Production readiness review |
| Loop | An agent repeating act, check, adjust until a condition is met | Agent loop, Ralph loop [Huntley] |
| Maturity level | How much of the method a project uses, from 0 (ad hoc) to 4 (self-verifying). See [adoption](06-adoption-and-measurement.md) | |
| Owner | The one person or agent role allowed to change an area or item | Single writer, maker, responsible |
| Plan mode | An agent setting that allows reading but not changing anything, used for planning [Anthropic PM] | Read-only mode |
| Pre-mortem | Before starting, imagining the project has failed and listing why, to find long-lead items and risks early | |
| Retrospective | A regular review of the method itself against the current state (stage 9) [Scrum] | Harness maintenance, prompt audit |
| Reviewer | An independent checker who gets the change and the acceptance criteria, never the author's reasoning | Checker, evaluator |
| Risk tier | How risky an item is, which sets how many gates it needs: *local* (1), *shared* (2), *irreversible* (3 and a second human). See [the procedure](05-work-item-procedure.md) | |
| Separation of duties | The person or agent who does the work is not the one who approves it [SoD] | Maker-checker, four-eyes principle |
| Situation analysis | Stage 1: finding out what is true before planning. Gap analysis on existing work, assumption register on new work | Research phase [Horthy 2025] |
| Skill | A packaged instruction set an agent loads when needed, for example the standard procedure [Anthropic Skills] | Agent skill, playbook |
| Software factory | Many harnessed agent loops working together, with humans owning the system from above [Osmani 2026a] | |
| Standard procedure | The written, repeatable way to take one work item from proposed to done, with gates (stage 7). Usually packaged as a skill | Standard work [LEI-SW], SOP, runbook (operations sense) |
| Status values | `proposed`, `ready`, `in-progress`, `in-review`, `merged`, `done`, `blocked`, `dropped`. `merged` means not yet verified in the target environment | |
| Status verification | Checking, by script where possible, that every status claim is backed by evidence (stage 8) | Truth check, Definition of Done enforcement |
| Subagent | An agent started by another agent, with its own context and permissions [Anthropic Sub] | |
| Trigger | The failure that shows a stage is needed. An *anticipated trigger* starts the stage before the failure, when it can be foreseen | |
| Walking skeleton | The thinnest end-to-end version of a system (build, deploy, environments) built first, so later items can be verified in a real environment | |
| Work isolation | Each item gets its own workspace and one owner, so parallel work cannot collide (stage 6) | |
| Work item | One row in the backlog: small enough to verify, with one owner | Item, task, story |
| Worktree | A second working copy of the same git repository on its own branch, used for one work item | git worktree |
