# Why it works

This page is the argument behind the method: what changed with AI agents, why the stages are
mostly established practice, and how the method relates to what the field already teaches.
Read it to understand or explain the method. To use it, start with the
[quick start](01-quick-start.md). Sources are in the [references](11-references.md).

## What changed

With AI agents, producing work is cheap. Several agents can draft, build and review in parallel.
Three things stay expensive: knowing the current state, deciding what comes next, and proving
that a piece of work is done. The engineer's job therefore moves from writing the code to
designing the system that produces and verifies it.

The field has settled on names for this. An agent runs in a **loop**. The tooling, instructions
and checks around the loop are the **harness**. Many harnessed loops working together are a
**software factory**, with humans "owning the whole thing from above" [Osmani 2026a]. Karpathy
calls the practice **agentic engineering**: "you are orchestrating agents who do and acting as
oversight" [Karpathy 2026].

## Thesis

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
   is that agents now carry out much of the work, so skipping these practices costs more (see below).

## Established software engineering practice, new executor

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
| 1 Situation analysis | Requirements analysis; current-state assessment | Research phase before the agent plans |
| 2 Context file | README, contributing guide, coding standards; architecture decision records, "a collection of records for 'architecturally significant' decisions" [Nygard] | `AGENTS.md` / `CLAUDE.md` that every agent loads |
| 3 Roles and separation of duties | Code review; code owners; four-eyes approval | Reviewer subagents with read-only access and no access to the author's reasoning |
| 4 Phased plan | Release planning; dependency management; change management, since "roughly 70% of outages are due to changes in a live system" [SRE] | Plan mode; spec, plan, tasks |
| 5 Backlog | Product backlog; user stories with acceptance criteria; working in small batches, which "amplifies the positive impact of AI adoption on product performance" [DORA SB] | Feature list or `tasks.md` the agent works through |
| 6 Work isolation | Short-lived feature branches: "the branch should only last a couple of days" [TBD]; ephemeral environments | One git worktree per agent and work item |
| 7 Standard procedure | Continuous integration: "should the integration build fail, then it needs to be fixed right away" [Fowler CI]; scripted runbooks; infrastructure as code | Skills, loops and hooks that encode the procedure |
| 8 Status verification | Definition of Done; CI quality gates; staged rollouts that apply a change "to small fractions of traffic and capacity at one time" [SRE-BP]; deployment verification | Stop hooks, computational sensors, a script that checks every "done" has evidence |
| 9 Retrospective and harness maintenance | Retrospectives; blameless postmortems; docs as code | Prompt audits; harness maintenance |
| Whole method | Version control as the record of change. DORA: strong version control practices "amplify the positive impact of AI adoption" [DORA VC], one of the seven DORA AI capabilities [DORA AI] | Every agent action lands as a reviewable commit |

Two points need care.

1. **The scale changes, not the practice.** Trunk-based development now counts "one developer
   and their coding agents" as one unit on a branch [TBD]. That wording was added in October
   2026, which shows the established practices are being restated for agents right now rather
   than replaced.
2. **Not every practice transfers unchanged.** In a 2026 experiment, Böckeler found "no clearly
   discernable difference" between agents told to follow a TDD workflow and agents that weren't
   [Böckeler TDD]. Applying practices to agents still needs measurement, the same as any other
   process change. That is what stage 9 and the [measurement guidance](06-adoption-and-measurement.md) are for.

So the claim of this document is narrower than "AI changes everything". The practices that
worked for human teams still work, and they matter more because agents produce changes faster
than people can check them by hand. The new skill is building those practices into the harness
so that they run every time without a person having to remember them. "Software engineering is
programming integrated over time" [SWE@Google]. AI-native engineering applies the same idea to a
team made largely of agents.

## Terms crosswalk

| This method | AI-era term | Established term |
|---|---|---|
| The whole system | Harness; software factory [Osmani 2026a; Böckeler] | Production system; quality management system |
| AI stance | Clear and communicated AI stance [DORA AI] | Acceptable use policy; data classification |
| The engineer's role | Agentic engineering [Karpathy 2026]; loop engineering [Osmani 2026b] | Process owner |
| Situation analysis | Research phase [Horthy 2025] | Gap analysis; requirements analysis; assumption register |
| Context file | Context engineering [Anthropic CE]; AGENTS.md; curated shared instructions [TW-CSI] | Project charter; README; ADRs; SECI externalization [SECI] |
| Roles and separation of duties | Subagents; orchestrator-workers; evaluator-optimizer [Anthropic BEA]; skills | Maker-checker; code owners; RACI |
| Phased plan | Prompt chaining with gates [Anthropic BEA]; plan mode; spec, plan, tasks [Spec Kit; Kiro] | WBS; critical path; stage-gate |
| Backlog | Feature list; progress file [Anthropic LRA]; tasks.md | Product backlog; work packages; Definition of Done |
| Work isolation | Git worktrees [Anthropic BP-2025]; sandboxes | Short-lived feature branches; ephemeral environments |
| Standard procedure | Skill; loop [Willison 2025a]; Ralph loop [TW-Ralph] | Standard work; checklist; SOP; CI/CD pipeline |
| Incident to rule | Signs added to the prompt [Huntley] | Blameless postmortem; after-action review; poka-yoke |
| Status verification | Sensors; Stop hook; `/goal` | Automated Definition of Done; CI quality gates; evidence-based audit |
| Retrospective and harness maintenance | Prompt audit | Retrospective; PDSA "Act"; document control |

## Parallel with the community roadmaps

roadmap.sh, a widely used community site for developer learning paths, now has a Claude Code roadmap and a Vibe
Coding best-practice roadmap (the repository was last updated in late October 2026). The workflow they
describe for a single agent session follows the same arc at a smaller scale: "Explore, Plan,
Implement, and Verify" [RM-CC workflow].

| Stage | roadmap.sh node | What the node says |
|---|---|---|
| 1 Situation analysis | Explore phase [RM-CC workflow]; Plan before you code [RM-VC] | "Little planning at the start saves many hours of fixing later." |
| 2 Context file | CLAUDE.md [RM-CC]; Regularly update your context document [RM-VC]; Spec-driven development [RM-VC] | "Every time you make an important decision about your project, add it to your context document." |
| 3 Roles and separation of duties | Subagents; Code review [RM-CC] | Each subagent "starts with a clean slate"; a reviewer can be written "as a subagent or skill". |
| 4 Phased plan | Plan mode [RM-CC] | "A strictly read-only permission state" for drafting a "step-by-step implementation strategy". |
| 5 Backlog | Work step by step [RM-VC]; agent teams with "a shared task list" [RM-CC scaling] | "Build one feature at a time. Ask the AI to do it, test it, make sure it works." |
| 6 Work isolation | Git worktrees; Scaling Claude [RM-CC] | Worktrees "give each parallel session its own git checkout so they never edit the same files." |
| 7 Standard procedure | Creating skills [RM-CC] | `disable-model-invocation: true` runs a skill "as a manual, deterministic workflow". |
| 8 Status verification | Hooks; Loops [RM-CC]; Verify phase [RM-CC workflow] | Hooks "enforce project standards ... without manual intervention". |
| 9 Retrospective | Regularly update your context document [RM-VC]; Doctor [RM-CC] | Keep the context document current as decisions change. |

The roadmaps teach the tool, one session at a time. They have no node for the project layer that
made the example work: the situation analysis, a backlog with evidence links, fixed status values, a
status verification script, human gates on irreversible actions, and audits of the method itself.
The roadmaps cover one loop and its harness. This method covers the factory around them.

## Principles

1. Invest in how the work gets done, and the results follow. [Osmani 2026a]
2. Analyse the situation before you plan. On existing work keep as-is, to-be and the gap separate; on new work write the assumptions down and test the riskiest first. [Gap]
3. Keep work items small enough to verify. Each owner finishes and verifies one item before
   starting the next. [Wake; Scrum; DORA SB]
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
