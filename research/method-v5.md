# The process is the product

A method for running projects with AI agents. It was taken from one project and written so it
applies to others.

Status: working draft v5, 2026-10-31. The purpose is to formalize and record the method. A blog
post may follow. Every linked quote was fetched and checked on 2026-10-31. This is one case
(n=1); see the gap report in this folder for what it has not yet been tested against.

## 1. Abstract

With AI agents, producing work is cheap. Several agents can draft, build and review in parallel.
Three things stay expensive: knowing the current state, deciding what comes next, and proving
that a piece of work is done. The engineer's job therefore moves from writing the code to
designing the system that produces and verifies it.

The field has settled on names for this. An agent runs in a **loop**. The tooling, instructions
and checks around the loop are the **harness**. Many harnessed loops working together are a
**software factory**, with humans "owning the whole thing from above" [Osmani 2026a]. Karpathy
calls the practice **agentic engineering**: "you are orchestrating agents who do and acting as
oversight" [Karpathy 2026].

This document records how one such factory was built on a real project. Nobody designed it up
front. It grew in nine stages, and each stage was added after a specific failure. The visible end
result was a **runbook**: a backlog of small work items, each with its own acceptance check, and
a standard procedure that takes any item from proposed to verified done. The runbook is the
output. The nine stages are the method.

Almost every stage is an established practice under a new name. Section 11 maps each one to the
software engineering practice it comes from, and section 9 shows the same stages on projects that
have nothing to do with software.

## 2. Thesis

1. **The process is the product.** What lasts is the system that produces and verifies the work,
   more than any single piece of work. Boris Cherny: "My job is to write loops" [Osmani 2026b].
2. **Human judgment moves to the gates.** People stop doing every step. They set the standards,
   approve the gates and decide what counts as evidence. "Human judgment doesn't leave the
   software factory. It relocates." [Osmani 2026c, title]
3. **Standardize first, then improve.** A process that isn't written down can't be improved.
   "There can be no kaizen without a standard" (Ohno, via [LEI]). A sequence that works becomes
   a standard procedure. A mistake that repeats becomes a rule in it.
4. **Verification matters more than generation.** Agent output is only as good as the check that
   judges it. Anthropic's advice is to ask the agent for "evidence: the command it ran and its
   output" [Anthropic BP]. Or in SRE terms, "hope is not a strategy" [SRE].
5. **The practices are old; the executor is new.** Gap analysis, code review, small batches,
   short-lived branches, Definition of Done and retrospectives all predate AI agents. What changed
   is that agents now carry out much of the work, so skipping these practices costs more (section
   11).

## 3. The example project (scope only)

- **Starting point:** a client handover archive with three applications, one external
  integration, an early infrastructure template, and loose notes.
- **Goal:** rebuild the cloud foundation with no stored secrets, and get the applications running
  in development, test and production while the client's own developers kept working.
- **Constraints:** busy external approvers in the client's IT department, one shared
  code checkout used by many AI sessions, and three different AI tools.
- **Team and duration:** one engineer directing AI agents for about five and a half weeks.
- **Outcome:** a runbook of about 100 work items covering the work and the roadmap after it,
  with everything in scope done with linked evidence from the live system, about 300 commits, and over 100 single-use git worktrees. These numbers
  describe one outcome. They are not targets.

## 4. The method: nine stages

For each stage: the **trigger** (the failure that shows you need it), the **output**, the **exit
criteria**, the AI-era terms, the established terms, and what happened on the example project.
Add a stage when its trigger occurs, not before.

### Stage 1. Gap analysis
- **Trigger:** the inputs are scattered, contradictory or of unknown quality.
- **Output:** a gap analysis with current state (as-is), target state (to-be) and the gap, plus
  a dated decision log.
- **Exit criteria:** every input is accounted for, and every open question has an owner.
- **AI-era terms:** a research phase before planning, as in research, plan, implement [Horthy
  2025]; having the agent interview you until it "could write the spec" [Anthropic BP].
- **Established terms:** gap analysis [Gap]; requirements analysis; decision log.
- **Example:** on day 1 the archive was unpacked and compared with what the client had described.
  The "infrastructure" was a generic template, not a design, and the plan changed because of it.

### Stage 2. Shared context file
- **Trigger:** every new agent or person starts from zero and you keep repeating yourself.
- **Output:** one context file that every agent loads, with the repository layout, the roles, and
  the **invariants** (rules that are never negotiated).
- **Exit criteria:** a new agent can start useful work from the file alone.
- **AI-era terms:** context engineering, which "treats the context window as a design surface"
  [TW-CE; Anthropic CE]; `AGENTS.md` and `CLAUDE.md` [agents.md; Anthropic BP]; curated shared instructions
  [TW-CSI]; feedforward **guides** [Böckeler].
- **Established terms:** project charter; README and contributing guide; coding standards;
  architecture decision records [Nygard].
- **Example:** one context file, linked under the file name each of the three AI tools reads.
  Invariants included "no stored secrets" and "done means verified by a command".

### Stage 3. Roles and separation of duties
- **Trigger:** two agents change the same thing, or whoever did the work also reviews it.
- **Output:** a role list with one owner per area (a single writer), independent reviewers with
  read-only access, and **skills** (packaged domain knowledge) that roles load when needed.
- **Exit criteria:** for every area you can name its one owner and its reviewer.
- **AI-era terms:** subagents, each with "its own context window ... and independent
  permissions" [Anthropic Sub]; the orchestrator-workers and evaluator-optimizer patterns
  [Anthropic BEA]; Agent Skills loaded by progressive disclosure [Anthropic Skills]; a reviewer
  that "never saw your conversation" [Anthropic BP].
- **Established terms:** separation of duties [SoD]; maker-checker (four-eyes principle); code
  owners; RACI.
- **Example:** about 20 agent roles and a dozen skills, grown over several weeks. Reviewers received the change and the
  acceptance criteria, never the author's reasoning.

### Stage 4. Phased plan with stage gates
- **Trigger:** work starts before its dependencies are ready, or slow external approvals block
  you late in the project.
- **Output:** a plan in phases, each with entry criteria, an owner and exit criteria. Requests
  that take a long time to approve are bundled and sent as early as possible.
- **Exit criteria:** nothing can start before its dependencies are done, and every external
  request has been sent.
- **AI-era terms:** prompt chaining with gates [Anthropic BEA]; plan mode [Anthropic PM]; spec,
  plan, tasks [Spec Kit]; dependency "waves" [Kiro].
- **Established terms:** work breakdown structure [WBS]; critical path; stage-gate, where gates
  are "tough decision meetings" [Cooper]; long-lead items; release planning.
- **Example:** a seven-phase gated plan and one bundled request pack for the external
  administrators, sent on day 5.

### Stage 5. Backlog of small, verifiable work items (the runbook)
- **Trigger:** "mostly done" work piles up and nobody can say what is finished.
- **Output:** a backlog with one row per work item (schema in section 5).
- **Exit criteria:** every row has acceptance criteria that a check can prove true or false.
- **AI-era terms:** a feature list where every item starts "marked as 'failing'", plus a
  progress file [Anthropic LRA]; `tasks.md` [Spec Kit; Kiro].
- **Established terms:** product backlog; work packages; acceptance criteria; Definition of Done
  [Scrum]; INVEST, "Small, Testable" [Wake]; working in small batches [DORA].
- **Example:** the master runbook grew from about 30 rows to about 100.

### Stage 6. Work isolation
- **Trigger:** parallel work collides and changes leak between tasks.
- **Output:** each work item gets its own workspace and a single owner, so items can run in
  parallel.
- **Exit criteria:** nobody edits a shared workspace or someone else's.
- **AI-era terms:** git worktrees for "multiple Claude sessions simultaneously" [Anthropic
  BP-2025]; the "parallel coding agent lifestyle" [Willison 2025b]; sandboxing [Willison 2025a].
- **Established terms:** short-lived feature branches and trunk-based development [TBD];
  ephemeral environments; a permit to work (outside software).
- **Example:** one new git worktree per work item. The rule came after several AI sessions
  switched branches in the same shared checkout.

### Stage 7. Standard work: run it by hand, then codify the best run
- **Trigger:** every item repeats the same twenty small decisions, and quality depends on who runs
  it.
- **Output:** a **standard procedure** for one work item, with human approval gates (section 6).
  Each past incident is written into it as a rule.
- **Exit criteria:** "do item N" is enough instruction for a new agent to take an item from
  review to verified done.
- **AI-era terms:** a skill that runs only "when you type `/release` yourself" [Anthropic BP];
  loop engineering [Osmani 2026b]; the Ralph loop, tuned by adding "signs" [Huntley; TW-Ralph].
- **Established terms:** standard work [LEI-SW]; checklists [Gawande]; runbook automation; the
  CI/CD pipeline as codified procedure [Fowler CI]; PDSA [Deming]; poka-yoke [Poka]; blameless
  postmortems [SRE-PM] and after-action reviews [AAR]; making tacit knowledge explicit
  ("externalization" [SECI]).
- **Example:** for the first week every item was run by hand. On day 9 the cleanest
  end-to-end run (around row 40 of the backlog) was written down as the procedure, and it was
  refined after every incident.

### Stage 8. Status verification
- **Trigger:** an item is marked done when it isn't, for example merged but never deployed, or
  "verified" by a pipeline run that was cancelled.
- **Output:** a fixed set of status values, a map from each kind of change to the documents it
  affects, and a **script** that checks every "done" row links to real evidence.
- **Exit criteria:** the script passes before any status change is published.
- **AI-era terms:** computational feedback **sensors**, as opposed to inferential ones [Böckeler];
  a Stop hook that "sends Claude back to work" [Anthropic BP]; a machine-checkable `/goal`
  [Anthropic BP].
- **Established terms:** Definition of Done enforced by automation; CI quality gates; deployment
  verification; evidence-based auditing [ISO 19011]; eliminating toil [SRE-Toil].
- **Example:** an audit on day 10 found rows marked done that weren't. The verification script
  existed a day later. The same approach was later applied to the release process, with each
  release milestone checked against the live system.

### Stage 9. Retrospective and harness maintenance
- **Trigger:** the context file, roles or procedures describe a situation that has since changed.
- **Output:** regular audits of the method's own documents against the current state.
- **Exit criteria:** an audit finds no high-severity stale instructions.
- **AI-era terms:** a prompt audit that flags instructions that "point at files that no longer
  exist, or contradict each other" [Anthropic BP]; harness engineering as ongoing work [Böckeler].
- **Established terms:** retrospective [Scrum]; the Act step of PDSA [Deming]; document control;
  docs as code.
- **Example:** an audit on day 19 found about three dozen problems, a third of them high severity, such as
  instructions that pointed at deleted components.

The runbook is stage 5, but it only produced results after stage 7. Until each row had a
standard procedure behind it, the backlog was just a plan. And from stage 3 on, each stage was added within days
of a concrete failure, so the factory was built in response to need rather than from a design.

## 5. Backlog item schema

| Field | Meaning |
|---|---|
| ID | A stable number or code |
| Status | proposed, in progress, merged but not deployed, done (verified), or blocked |
| Owner | The single owner |
| Workstream | The area or track |
| Scope | The exact files, resources or settings the item changes |
| Specification | What to do, precise enough to hand to a new agent |
| Acceptance criteria | The check and the result it must give |
| Unblocks | The later items that depend on this one |
| Evidence | A link to the proof, once done |

A status summary sits at the top. A row can only say "done" if it has an evidence link.

## 6. Standard procedure for one work item (three phases, three approval gates)

1. **Review (read-only).**
   - Pull the latest state.
   - Read the row and its neighbours.
   - Check every claim in the row against the source of truth and mark it confirmed, unconfirmed
     or wrong, with evidence.
   - Record baseline values for everything you will measure afterwards.
   - List the documents the change will affect.
   - Ask the human only about real decisions.
   - **Gate: the plan is approved.**
2. **Build (in an isolated worktree).**
   - Create a new worktree with one owner.
   - Verify the change locally.
   - Independent reviewers check it in parallel, with the acceptance criteria but without the
     author's reasoning.
   - Update the affected documents and run the status verification script.
   - **Gate: the change and the pull request description are approved.**
3. **Release (started by a human).**
   - A human starts any action that can't be undone.
   - Compare the planned changes with the expected ones, item by item.
   - Verify the result against the live system, not against a status report.
   - Record the done entry with its evidence.
   - **Gate: the release is approved.**

Rules added after incidents:

- Measure a baseline before you change anything.
- A system reporting its own success is not evidence.
- Count the expected changes again before release instead of trusting an estimate.
- Write the done entry before the work item is closed, or it can get lost.
- If a human refuses a permission, the answer stands.

Each gate is a decision against stated criteria, as in stage-gate [Cooper], not a status update.

## 7. Failures each stage prevents

| Failure | Stage that prevents it |
|---|---|
| Planning on assumptions nobody checked | 1 Gap analysis |
| Each agent re-learns the project; instructions contradict each other | 2 Context file |
| Authors approve their own work; two agents overwrite each other | 3 Separation of duties |
| Work starts before its dependencies; late surprises from external approvers | 4 Phased plan |
| Items stay "90% done"; nobody knows what is finished | 5 Backlog |
| Parallel work collides; changes leak between tasks | 6 Work isolation |
| Quality depends on who runs the item; the same mistake happens twice | 7 Standard work |
| Optimistic or false status; "merged" reported as "deployed" | 8 Status verification |
| Instructions that describe last month's project | 9 Retrospective |
| An agent loop with no stopping rule | Machine-checkable acceptance criteria (5, 8) |

## 8. Maturity levels for a new project

| Level | What you have | Move here when |
|---|---|---|
| 0 Ad hoc | Chat with an AI and copy results by hand | You are exploring an idea |
| 1 Briefed | Gap analysis and context file (stages 1 and 2) | More than one session or agent is involved |
| 2 Planned | Roles, phased plan and backlog (stages 3 to 5) | The work takes more than a week or has external dependencies |
| 3 Factory | Work isolation and standard procedure (stages 6 and 7) | Items repeat, or work runs in parallel |
| 4 Self-verifying | Status verification and retrospectives (stages 8 and 9) | Other people rely on your status |

Move up a level when you hit its trigger, not before.

## 9. Beyond software

| Stage | House renovation | Compliance audit | Event or office move |
|---|---|---|---|
| Gap analysis | Survey the house as it is against the drawings | Current controls against the standard | Inventory of people, assets and contracts |
| Context file | Budget, style, what must not change | Scope, framework, evidence rules | One brief for all suppliers |
| Separation of duties | One trade per room; an inspector who doesn't build | Control owner and independent tester | One owner per workstream, a separate reviewer |
| Phased plan | Permits and long-lead materials first | Requests to other departments first | Venue, permits and catering first |
| Backlog | One job per row, with its test | One control per row, with evidence | One deliverable per row, with acceptance criteria |
| Work isolation | Seal off each room | One evidence folder per control | One channel per workstream |
| Standard procedure | Inspect, plan, sign off, do, test, photograph, tick | Review, test, check, file, mark | Confirm, book, get written confirmation, mark |
| Status verification | Done only with a certificate or photo | Done only with dated evidence | Done only with written confirmation |
| Retrospective | Update the brief when the client changes their mind | Re-baseline when the standard changes | Review the checklist after each event |

AI sits in the same place in every column: it drafts, does and reviews work in parallel, while
people approve the gates and decide what counts as evidence.

## 10. Terms crosswalk

| This method | AI-era term | Established term |
|---|---|---|
| The whole system | Harness; software factory [Osmani 2026a; Böckeler] | Production system; quality management system |
| The engineer's role | Agentic engineering [Karpathy 2026]; loop engineering [Osmani 2026b] | Process owner |
| Gap analysis | Research phase [Horthy 2025] | Gap analysis; requirements analysis |
| Context file | Context engineering; AGENTS.md; guides | Project charter; README; ADRs |
| Separation of duties | Subagents; orchestrator-workers; evaluator-optimizer; skills | Maker-checker; code owners; RACI |
| Phased plan | Prompt chaining with gates; plan mode; spec, plan, tasks | WBS; critical path; stage-gate |
| Backlog (runbook) | Feature list; progress file; tasks.md | Product backlog; work packages; Definition of Done |
| Work isolation | Git worktrees; sandboxes | Short-lived feature branches; ephemeral environments |
| Standard procedure | Skill; loop; Ralph loop | Standard work; checklist; SOP; CI/CD pipeline |
| Incident to rule | Signs added to the prompt [Huntley] | Blameless postmortem; after-action review; poka-yoke |
| Status verification | Sensors; Stop hook; `/goal` | Automated Definition of Done; CI quality gates; evidence-based audit |
| Method audit | Prompt audit | Retrospective; PDSA "Act"; document control |

## 11. Established software engineering practice, new executor

Most of this method is established software engineering practice. What changed is who does the
work. Agents now write, test and review much of the code, so the practices that keep a team of
humans honest now have to keep a team of agents honest. Practitioners and researchers say the
same thing in different words:

- DORA's 2025 report: "AI's primary role is as an amplifier, magnifying an organization's
  existing strengths and weaknesses" [DORA 2025].
- Simon Willison: "LLMs actively reward existing top tier software engineering practices",
  naming automated testing, planning in advance, comprehensive documentation, good version
  control habits, effective automation and a culture of code review [Willison 2025c].
- Kent Beck: "The value system in augmented coding is similar to hand coding--tidy code that
  works. It's just that I don't type much of that code." [Beck 2025]
- Fred Brooks separated the "essence" of software difficulty from its "accidents, those
  difficulties that today attend its production but are not inherent" [Brooks 1987]. Agents
  remove many accidents. The essence remains: deciding what to build, and knowing whether it
  works. Stages 1, 5 and 8 deal with that essence.

| Stage | Established practice | Form with AI agents |
|---|---|---|
| 1 Gap analysis | Requirements analysis; current-state assessment | Research phase before the agent plans |
| 2 Context file | README, contributing guide, coding standards; architecture decision records, "a collection of records for 'architecturally significant' decisions" [Nygard] | `AGENTS.md` / `CLAUDE.md` that every agent loads |
| 3 Separation of duties | Code review; code owners; four-eyes approval | Reviewer subagents with read-only access and no access to the author's reasoning |
| 4 Phased plan | Release planning; dependency management; change management, since "roughly 70% of outages are due to changes in a live system" [SRE] | Plan mode; spec, plan, tasks |
| 5 Backlog | Product backlog; user stories with acceptance criteria; working in small batches, which "amplifies the positive impact of AI adoption on product performance" [DORA SB] | Feature list or `tasks.md` the agent works through |
| 6 Work isolation | Short-lived feature branches: "the branch should only last a couple of days" [TBD]; ephemeral environments | One git worktree per agent and work item |
| 7 Standard procedure | Continuous integration: "should the integration build fail, then it needs to be fixed right away" [Fowler CI]; scripted runbooks; infrastructure as code | Skills, loops and hooks that encode the procedure |
| 8 Status verification | Definition of Done; CI quality gates; staged rollouts that apply a change "to small fractions of traffic and capacity at one time" [SRE-BP]; deployment verification | Stop hooks, computational sensors, a script that checks every "done" has evidence |
| 9 Retrospective | Retrospectives; blameless postmortems; docs as code | Prompt audits; harness maintenance |
| Whole method | Version control as the record of change. DORA: strong version control practices "amplify the positive impact of AI adoption" [DORA VC], one of the seven DORA AI capabilities [DORA AI] | Every agent action lands as a reviewable commit |

Two points need care.

1. **The scale changes, not the practice.** Trunk-based development now counts "one developer
   and their coding agents" as one unit on a branch [TBD]. That wording was added in October
   2026, which shows the established practices are being restated for agents right now rather
   than replaced.
2. **Not every practice transfers unchanged.** In a 2026 experiment, Böckeler found "no clearly
   discernable difference" between agents told to follow a TDD workflow and agents that weren't
   [Böckeler TDD]. Applying practices to agents still needs measurement, the same as any other
   process change. That is what stage 9 is for.

So the claim of this document is narrower than "AI changes everything". The practices that
worked for human teams still work, and they matter more because agents produce changes faster
than people can check them by hand. The new skill is building those practices into the harness
so that they run every time without a person having to remember them. "Software engineering is
programming integrated over time" [SWE@Google]. AI-native engineering applies the same idea to a
team made largely of agents.


## 12. Parallel with the community roadmaps

roadmap.sh, a widely used community site for developer learning paths, now has a Claude Code roadmap and a Vibe
Coding best-practice roadmap (the repository was last updated 2026-10-30). The workflow they
describe for a single agent session follows the same arc at a smaller scale: "Explore, Plan,
Implement, and Verify" [RM-CC workflow].

| Stage | roadmap.sh node | What the node says |
|---|---|---|
| 1 Gap analysis | Explore phase [RM-CC workflow]; Plan before you code [RM-VC] | "Little planning at the start saves many hours of fixing later." |
| 2 Context file | CLAUDE.md [RM-CC]; Regularly update your context document [RM-VC]; Spec-driven development [RM-VC] | "Every time you make an important decision about your project, add it to your context document." |
| 3 Separation of duties | Subagents; Code review [RM-CC] | Each subagent "starts with a clean slate"; a reviewer can be written "as a subagent or skill". |
| 4 Phased plan | Plan mode [RM-CC] | "A strictly read-only permission state" for drafting a "step-by-step implementation strategy". |
| 5 Backlog | Work step by step [RM-VC]; agent teams with "a shared task list" [RM-CC scaling] | "Build one feature at a time. Ask the AI to do it, test it, make sure it works." |
| 6 Work isolation | Git worktrees; Scaling Claude [RM-CC] | Worktrees "give each parallel session its own git checkout so they never edit the same files." |
| 7 Standard procedure | Creating skills [RM-CC] | `disable-model-invocation: true` runs a skill "as a manual, deterministic workflow". |
| 8 Status verification | Hooks; Loops [RM-CC]; Verify phase [RM-CC workflow] | Hooks "enforce project standards ... without manual intervention". |
| 9 Retrospective | Regularly update your context document [RM-VC]; Doctor [RM-CC] | Keep the context document current as decisions change. |

The roadmaps teach the tool, one session at a time. They have no node for the project layer that
made the example work: the gap analysis, a backlog with evidence links, fixed status values, a
status verification script, human gates on irreversible actions, and audits of the method itself.
The roadmaps cover one loop and its harness. This method covers the factory around them.

## 13. Principles

1. Invest in how the work gets done, and the results follow. [Osmani 2026a]
2. Do the gap analysis before you plan, and keep as-is, to-be and the gap separate. [Gap]
3. Keep work items small enough to verify. Each owner finishes and verifies one item before
   starting the next. [Wake; Scrum; DORA]
4. Done means verified against the live system. "I believe" means unconfirmed. [ISO 19011;
   Anthropic BP]
5. One owner per area and one worktree per item make parallel work safe. [SoD; Willison 2025b]
6. Reviewers are independent and get the acceptance criteria, not the author's reasoning.
   [Anthropic BP]
7. Humans approve the gates on actions that can't be undone. [Cooper; Karpathy 2026]
8. A sequence that repeats becomes a standard procedure, and a mistake that repeats becomes a
   rule. [LEI; SRE-PM]
9. Status comes from evidence and is checked by a script where possible. [Böckeler; SRE-Toil]
10. The method drifts too, so audit it. [Scrum; Anthropic BP]
11. Keep the context file tool-neutral so any agent can pick up the work. [agents.md]

## 14. Timeline of the example (relative days)

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

## 15. References

All checked by fetch on 2026-10-31.

**Anthropic**
- [Anthropic BEA] Building effective agents, Dec 2024. https://www.anthropic.com/research/building-effective-agents
- [Anthropic BP] Best practices for Claude Code (current docs). https://code.claude.com/docs/en/best-practices
- [Anthropic BP-2025] Claude Code: Best practices for agentic coding, 2025 (archived; contains the worktrees section). https://web.archive.org/web/20251229110153/https://www.anthropic.com/engineering/claude-code-best-practices
- [Anthropic LRA] Effective harnesses for long-running agents. https://www.anthropic.com/research/effective-harnesses-for-long-running-agents
- [Anthropic CE] Effective context engineering for AI agents. https://www.anthropic.com/research/effective-context-engineering-for-ai-agents
- [Anthropic Skills] Equipping agents for the real world with Agent Skills. https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills
- [Anthropic Sub] Subagents (docs). https://code.claude.com/docs/en/sub-agents
- [Anthropic PM] Permission modes (docs). https://code.claude.com/docs/en/permission-modes

**AI engineering practice**
- [Karpathy 2026] "Agentic engineering" post. https://x.com/karpathy/status/2019137879310836075
- [Osmani 2026a] Addy Osmani, Software Factories, Light and Dark, Jul 2026. https://addyosmani.com/blog/software-factories/
- [Osmani 2026b] Addy Osmani, Loop engineering, Jun 2026. https://addyosmani.com/blog/loop-engineering/
- [Osmani 2026c] Addy Osmani, Human judgment doesn't leave the software factory, Aug 2026 (title only). https://addyosmani.com/blog/human-judgment-doesnt-leave-the-software/
- [Böckeler] Birgitta Böckeler, Harness engineering, martinfowler.com, 2026. https://martinfowler.com/articles/harness-engineering.html
- [Willison 2025a] Simon Willison, Designing agentic loops, 30 Sep 2025. https://simonwillison.net/2025/Sep/30/designing-agentic-loops/
- [Willison 2025b] Simon Willison, Embracing the parallel coding agent lifestyle, 5 Oct 2025. https://simonwillison.net/2025/Oct/5/parallel-coding-agents/
- [Willison 2025c] Simon Willison, Vibe engineering, 7 Oct 2025. https://simonwillison.net/2025/Oct/7/vibe-engineering/
- [Huntley] Geoffrey Huntley, Ralph Wiggum as a software engineer. https://ghuntley.com/ralph/
- [Horthy 2025] Dex Horthy, Advanced context engineering for coding agents, Aug 2025. https://www.humanlayer.dev/blog/advanced-context-engineering
- [Spec Kit] GitHub Spec Kit. https://github.com/github/spec-kit
- [Kiro] Kiro specs documentation. https://kiro.dev/docs/specs/
- [agents.md] AGENTS.md open format. https://agents.md/
- [TW-CE] Thoughtworks Radar Vol. 34, Context engineering. https://www.thoughtworks.com/radar/techniques/summary/context-engineering
- [TW-CSI] Thoughtworks Radar Vol. 34, Curated shared instructions. https://www.thoughtworks.com/radar/techniques/summary/curated-shared-instructions-for-software-teams
- [TW-Ralph] Thoughtworks Radar Vol. 34, Ralph loop. https://www.thoughtworks.com/radar/techniques/summary/ralph-loop

**Software engineering practice**
- [DORA 2025] DORA (Google Cloud), State of AI-assisted Software Development, 2025. https://dora.dev/research/2025/dora-report/
- [DORA SB] DORA, Working in small batches (capability, updated 8 Dec 2025). https://dora.dev/capabilities/working-in-small-batches/
- [DORA VC] DORA, Version control (capability, updated 12 Jan 2026). https://dora.dev/capabilities/version-control/
- [DORA AI] DORA AI Capabilities Model (seven capabilities: clear and communicated AI stance, healthy data ecosystems, AI-accessible internal data, strong version control practices, working in small batches, user-centric focus, quality internal platform). https://dora.dev/ai/capabilities-model/questions/
- [Fowler CI] Martin Fowler, Continuous Integration, revised 18 Jan 2024. https://martinfowler.com/articles/continuousIntegration.html
- [Nygard] Michael Nygard, Documenting Architecture Decisions, 15 Nov 2011. https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- [Brooks 1987] Fred Brooks, No Silver Bullet, IEEE Computer 20(4), April 1987. https://www.cgl.ucsf.edu/Outreach/pc204/NoSilverBullet.html
- [TBD] Paul Hammant, Short-lived feature branches, trunkbaseddevelopment.com (agentic wording added Oct 2026; recheck before publishing). https://trunkbaseddevelopment.com/short-lived-feature-branches/
- [SWE@Google] Titus Winters, Tom Manshreck, Hyrum Wright, Software Engineering at Google, O'Reilly 2020, ch. 1. https://abseil.io/resources/swe-book/html/ch01.html
- [SRE-BP] Google SRE book, Service best practices. https://sre.google/sre-book/service-best-practices/
- [Beck 2025] Kent Beck, Augmented Coding: Beyond the Vibes, 25 Jun 2025. https://tidyfirst.substack.com/p/augmented-coding-beyond-the-vibes
- [Böckeler TDD] Birgitta Böckeler, TDD inside the agent loop: theater or actual value?, martinfowler.com, Aug 2026. https://martinfowler.com/articles/exploring-gen-ai/tdd-in-the-agent-loop.html

**Community roadmaps**
- [RM-CC] roadmap.sh, Claude Code roadmap (nodes: CLAUDE.md, Plan mode, Subagents, Git worktrees, Creating skills, Hooks, Loops, Code review). https://roadmap.sh/claude-code
- [RM-CC workflow] roadmap.sh, Claude Code roadmap, node "Claude workflow". https://roadmap.sh/claude-code
- [RM-CC scaling] roadmap.sh, Claude Code roadmap, node "Scaling Claude". https://roadmap.sh/claude-code
- [RM-VC] roadmap.sh, Vibe Coding roadmap (nodes: Plan before you code, Spec-driven development, Regularly update your context document, Work step by step). https://roadmap.sh/vibe-coding
- Source text for both: https://github.com/kamranahmedse/developer-roadmap (src: roadmaps/claude-code, roadmaps/vibe-coding)

**Classic disciplines**
- [Gap] Gap analysis. https://en.wikipedia.org/wiki/Gap_analysis
- [SoD] Segregation of duties. https://en.wikipedia.org/wiki/Separation_of_duties
- [WBS] Work breakdown structure (PMBOK definition). https://en.wikipedia.org/wiki/Work_breakdown_structure
- [Cooper] Phase–gate model (Robert G. Cooper). https://en.wikipedia.org/wiki/Phase%E2%80%93gate_model
- [Scrum] Scrum Guide 2020. https://scrumguides.org/scrum-guide.html
- [Wake] Bill Wake, INVEST in Good Stories. https://xp123.com/articles/invest-in-good-stories-and-smart-tasks/
- [LEI] Lean Enterprise Institute, Kaizen. https://www.lean.org/lexicon-terms/kaizen/
- [LEI-SW] Lean Enterprise Institute, Standardized work. https://www.lean.org/lexicon-terms/standardized-work/
- [Deming] The Deming Institute, PDSA cycle. https://deming.org/explore/pdsa/
- [Poka] Poka-yoke (Shigeo Shingo). https://en.wikipedia.org/wiki/Poka-yoke
- [Gawande] Atul Gawande, The Checklist Manifesto, 2009 (book; no quote used).
- [SRE] Google SRE book, Introduction. https://sre.google/sre-book/introduction/
- [SRE-Toil] Google SRE book, Eliminating toil. https://sre.google/sre-book/eliminating-toil/
- [SRE-PM] Google SRE book, Postmortem culture. https://sre.google/sre-book/postmortem-culture/
- [AAR] After-action review (U.S. Army). https://en.wikipedia.org/wiki/After-action_review
- [ISO 19011] ISO 19011 auditing principles. https://en.wikipedia.org/wiki/ISO_19011
- [SECI] SECI model (Nonaka and Takeuchi). https://en.wikipedia.org/wiki/SECI_model_of_knowledge_dimensions

Left out because they could not be verified: Karpathy's "Software 3.0" and "autonomy slider"
wording, the Shopify memo, Gawande's read-do/do-confirm wording, and RAID log as a PMBOK term.
