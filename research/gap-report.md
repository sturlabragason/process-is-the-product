# Gap report: stress-testing the method

Date: 2026-10-31. Input: [method-v5.md](method-v5.md). Three independent reviewers (Opus) applied the
method on paper and reported where it broke. These were thought experiments, not real projects.

- **G, greenfield simulation:** 3 people plus agents build a new booking product for small
  clinics in 8 weeks, with payments, health data, and the cloud and auth vendors not yet chosen.
- **M, mid-project simulation:** an 18-month-old product, 8 engineers in 2 squads, a tracker
  with about 400 tickets, flaky CI, ad hoc AI use with conflicting personal prompt files, a
  regulated audit in 6 weeks, a half-finished migration, and weekly incidents.
- **U, usability review:** the doc read by an agent told to "set this up and run item 1", by a
  mid-level engineer new to agents, and checked for structure, consistency and anonymity.

## Summary

The core held up in all three runs. These parts should stay as they are:
- trigger, output and exit criteria per stage;
- "done needs an evidence link", checked by a script;
- reviewers get the acceptance criteria, not the author's reasoning;
- humans start irreversible actions;
- the rules learned from incidents;
- hand-run first, then codify;
- the crosswalk to established practice.

The gaps fall into five groups:

1. The method assumes one engineer on a brownfield project, started on day 1.
2. The gates have a single weight and a single owner.
3. Whole disciplines are missing.
4. An agent can't execute it as written.
5. It reads as an essay, not a guidebook.

All 39 gaps are now closed in the guidebook; the Status column links to where. A fourth Opus
review checked the guidebook against this list and its findings were fixed before the first
commit.

## Gaps

Severity: H high, M medium, L low. Status: **closed**, with a link to the file and section that closes the gap in the guidebook. Parts that go beyond the original project are marked there as untested proposals.

### A. Starting conditions

| # | Gap | Sev | Source | Proposed fix | Status |
|---|---|---|---|---|---|
| A1 | Assumes stage 1 on day 1 and levels adopted in order. No way to join a running project. | H | M | Add "Joining mid-flight": list which triggers are already firing, start at the stage with the costliest current failure, and limit the gap analysis to one workstream. | closed: [04-variants.md#joining-mid-flight](../docs/04-variants.md#joining-mid-flight) |
| A2 | Gap analysis needs an as-is state. In greenfield it is empty, so the exit criteria pass trivially. | H | G | Rename to situation analysis. Greenfield variant: assumptions and risk register, riskiest assumption first, discovery plan. Exit when each assumption has an owner and a test. | closed: [03-method.md#stage-1-situation-analysis](../docs/03-method.md#stage-1-situation-analysis) |
| A3 | Triggers are reactive, so long-lead work starts too late. | H | G | Add anticipated triggers: run a pre-mortem on day 1 and start the phased plan early for anything with a lead time over a week. | closed: [03-method.md#stage-1-situation-analysis](../docs/03-method.md#stage-1-situation-analysis) |
| A4 | The runbook as a file duplicates an existing tracker. | H | M | One system of record. The backlog schema is a set of fields, not a file. If a tracker exists, the runbook is a view of it. | closed: [04-variants.md#one-system-of-record-a4](../docs/04-variants.md#one-system-of-record-a4) |
| A5 | No triage for an inherited backlog; an agent would rewrite all 400 tickets. | H | M | Apply the schema when an item is pulled into work. Close stale, ownerless items. Never convert in bulk. | closed: [04-variants.md#inherited-backlog-triage-a5](../docs/04-variants.md#inherited-backlog-triage-a5) |
| A6 | Old and new systems running side by side are not modelled. | M | M | The context file names the authoritative system per capability. The migration is its own workstream with dated cut-over criteria. | closed: [04-variants.md#old-and-new-systems-side-by-side-a6](../docs/04-variants.md#old-and-new-systems-side-by-side-a6) |

### B. Teams and gates

| # | Gap | Sev | Source | Proposed fix | Status |
|---|---|---|---|---|---|
| B1 | Written for one engineer. Nobody owns the gates in a team, and gate load grows with headcount. | H | G, M | Gate owner matrix (RACI per gate type). Treat human review capacity as a work-in-progress limit. Map existing PR review and code owners onto gate 2. | closed: [05-work-item-procedure.md#gate-owners](../docs/05-work-item-procedure.md#gate-owners) |
| B2 | One gate weight for every change: too heavy for scaffolding, too light for payments and personal data. | H | G, M | Risk tiers. Reversible local changes: 1 gate. Changes to shared code or environments: 2 gates. Irreversible or regulated changes: 3 gates plus a second human. | closed: [05-work-item-procedure.md#risk-tiers](../docs/05-work-item-procedure.md#risk-tiers) |
| B3 | No expedite path for incidents. | H | M | Mitigate first, then open the item, then backfill the baseline, evidence and postmortem rule within 48 hours. | closed: [05-work-item-procedure.md#expedite-path-for-incidents](../docs/05-work-item-procedure.md#expedite-path-for-incidents) |
| B4 | No change management for people: skeptics, personal prompt files. | H | M | Pilot one squad, opt in, review after two sprints against metrics. Personal overlays allowed for style, never for invariants. | closed: [06-adoption-and-measurement.md#bringing-people-in](../docs/06-adoption-and-measurement.md#bringing-people-in) |
| B5 | Context file has no owner in a team. | M | M | The context file is code: it has a code owner and changes go through review. | closed: [03-method.md#stage-2-context-file](../docs/03-method.md#stage-2-context-file) |
| B6 | Unclear whether an agent reviewer satisfies four-eyes rules. | M | M | An agent reviewer adds to human sign-off. Where regulation requires a human, it does not replace one. | closed: [04-variants.md#agent-reviewers-and-four-eyes-rules-b6](../docs/04-variants.md#agent-reviewers-and-four-eyes-rules-b6) |
| B7 | Isolation is local only; human-to-human collisions (schema, migrations, API contracts) are not covered. | M | G | Branch policy, CI merge gate, and contract tests between components. | closed: [04-variants.md#team-level-isolation-b7](../docs/04-variants.md#team-level-isolation-b7) |

### C. Missing disciplines

| # | Gap | Sev | Source | Proposed fix | Status |
|---|---|---|---|---|---|
| C1 | No AI usage policy: approved tools, data classes, production access. | H | M, G | Stage 0: a clear and communicated AI stance (already in the DORA reference). No production personal data in agent context. | closed: [03-method.md#stage-0-ai-stance](../docs/03-method.md#stage-0-ai-stance) |
| C2 | Security, privacy and compliance appear only as invariants. | H | G | Threat model, data classification and a DPIA (data protection impact assessment) as early backlog items. | closed: [03-method.md#security-and-privacy-items](../docs/03-method.md#security-and-privacy-items) |
| C3 | No testing strategy; the script checks evidence links, not regressions. | H | G | An automated regression suite is a required sensor. Reviewers check that tests exist, not only that they pass. | closed: [05-work-item-procedure.md#testing-as-a-required-sensor](../docs/05-work-item-procedure.md#testing-as-a-required-sensor) |
| C4 | CI evidence is assumed trustworthy. | H | M | Evidence-quality rules: quarantine flaky tests. A green re-run with no code change is evidence of flakiness, not success. | closed: [05-work-item-procedure.md#evidence-quality](../docs/05-work-item-procedure.md#evidence-quality) |
| C5 | Evidence is not attributable or durable enough for an audit. | H | M | Evidence must be immutable, dated and attributed, with retention covering the audit window. Record who approved each gate and when. | closed: [05-work-item-procedure.md#audit-grade-evidence](../docs/05-work-item-procedure.md#audit-grade-evidence) |
| C6 | No way to measure whether the method helps. This breaks its own "baseline first" rule. | H | M | Baseline the DORA four keys plus false-done rate, gate wait time and rework for two sprints before adopting; review after six weeks. | closed: [06-adoption-and-measurement.md#measuring-whether-the-method-helps](../docs/06-adoption-and-measurement.md#measuring-whether-the-method-helps) |
| C7 | No product discovery or requirement-change loop. | H | G | User findings become backlog changes through a gate owned by the product owner. | closed: [03-method.md#discovery-loop](../docs/03-method.md#discovery-loop) |
| C8 | Decisions made before any code exists are not modelled; agents choose defaults. | H | G | A "decision" item type linked to an ADR, with an owner and deadline. Agents never choose an option a human hasn't decided. | closed: [03-method.md#decision-items](../docs/03-method.md#decision-items) |
| C9 | No observability or launch readiness. | M | G | Logs, metrics and alerts are acceptance criteria for user-facing items. Add a launch-readiness gate. | closed: [05-work-item-procedure.md#observability-and-launch-readiness](../docs/05-work-item-procedure.md#observability-and-launch-readiness) |
| C10 | No cost or token budget. | M | G | Budget as an invariant, cost per item, overrun as a stop rule. | closed: [05-work-item-procedure.md#cost](../docs/05-work-item-procedure.md#cost) |
| C11 | Some acceptance criteria can't be machine-checked (usability, value). | M | G | Allow human-judged evidence, labelled as inferential. | closed: [05-work-item-procedure.md#inferential-evidence](../docs/05-work-item-procedure.md#inferential-evidence) |
| C12 | "Verify against live" fails before production exists. | M | G | Item 0 is a walking skeleton (CI, environments, deploy). Define done per environment. | closed: [03-method.md#item-0-the-walking-skeleton](../docs/03-method.md#item-0-the-walking-skeleton) |
| C13 | Process only grows; there is no rule for removing it. | M | G, M | Remove a rule unused for N weeks. Skip the procedure for reversible changes below a size limit. | closed: [06-adoption-and-measurement.md#removing-process](../docs/06-adoption-and-measurement.md#removing-process) |

### D. Agent executability

| # | Gap | Sev | Source | Proposed fix | Status |
|---|---|---|---|---|---|
| D1 | No file names, paths or formats for the context file, backlog, decision log or roles. | H | U | Templates appendix with fixed default paths. | closed: [01-quick-start.md](../docs/01-quick-start.md) |
| D2 | The status verification script has no spec. | H | U | Spec plus a short reference script; exact status values. | closed: [README.md](../tools/README.md) |
| D3 | Gates don't say how to ask, how to record approval, or what counts as irreversible. | H | U | Gate checklists, a list of irreversible actions (deploy, apply, delete, external message, merge to shared branch, edit an existing instruction file), and an approval record format. | closed: [05-work-item-procedure.md#irreversible-actions](../docs/05-work-item-procedure.md#irreversible-actions) |
| D4 | Over-building risk: an agent would generate all nine stages and 20 roles. | H | U, G | MUST NOT rule: default to level 1 or 2 and name the trigger before adding a stage. Example numbers are outcomes, not targets. | closed: [06-adoption-and-measurement.md#maturity-levels](../docs/06-adoption-and-measurement.md#maturity-levels) |
| D5 | Narrative and rules are mixed. | H | G, U | A separate agent instruction file with MUST and MUST NOT rules, paths, gates and stop conditions. | closed: [METHOD.agent.md](../agent/METHOD.agent.md) |
| D6 | No stopping rule for setup itself. | M | U | Setup has a done condition (a command and its expected result), an iteration cap, and "same failure twice, stop". | closed: [05-work-item-procedure.md#stop-rule-for-agent-loops](../docs/05-work-item-procedure.md#stop-rule-for-agent-loops) |

### E. Teaching, consistency and claims

| # | Gap | Sev | Source | Proposed fix | Status |
|---|---|---|---|---|---|
| E1 | No quick start, no worked example of one item end to end, no glossary. | H | U | Add all three (see the proposed structure below). | closed: [02-worked-example.md](../docs/02-worked-example.md) |
| E2 | Thesis and citations come before any how-to; about 40% of the doc is evidence. | M | U | How-to first, evidence last. | closed: [README.md](../README.md) |
| E3 | "Runbook", "standard procedure", "skill" and "loop" are used loosely. | M | U | One term per concept, defined in the glossary. | closed: [10-glossary.md](../docs/10-glossary.md) |
| E4 | "About forty items run by hand" against 49 done by day 39 read as a contradiction. | H | U | Reworded: the procedure came from the run of about row 40. | closed: [08-case-study.md#how-each-stage-appeared](../docs/08-case-study.md#how-each-stage-appeared) |
| E5 | Request pack "on day 1" against day 5 in the timeline. | M | U | Stage says "as early as possible"; example says day 5. | closed: [03-method.md#stage-4-phased-plan-with-stage-gates](../docs/03-method.md#stage-4-phased-plan-with-stage-gates) |
| E6 | "Every stage was added after a failure" is not true for stages 1 and 2. | M | U | Now "from stage 3 on". | closed: [08-case-study.md#what-the-case-shows](../docs/08-case-study.md#what-the-case-shows) |
| E7 | Principle 3 (finish before starting the next) contradicted parallel worktrees. | M | U | Now per owner. | closed: [09-why-it-works.md#principles](../docs/09-why-it-works.md#principles) |
| E8 | Uncited references, a reference without a URL, and "every quote checked" overstated. | M | U | Uncited ones removed, URL added, wording is now "every linked quote". | closed: [11-references.md](../docs/11-references.md) |
| E9 | Unverified claim that roadmap.sh is among the most-starred projects. | M | U | Reworded neutrally. | closed: [09-why-it-works.md#parallel-with-the-community-roadmaps](../docs/09-why-it-works.md#parallel-with-the-community-roadmaps) |
| E10 | The case could be identified from its stack description and exact counts. | M | U | Stack generalized, numbers rounded and marked as outcome, not target. | closed: [08-case-study.md](../docs/08-case-study.md) |
| E11 | No limits section; results are a self-report of one case. | M | U | Add "Limits and what didn't work". The n=1 note is now in the status line. | closed: [08-case-study.md#limits-of-the-evidence](../docs/08-case-study.md#limits-of-the-evidence) |
| E12 | Maturity level grouping puts stage 3 (separation of duties) before its trigger (parallel work). | L | U | Move stage 3 to level 3 or split it. | closed: [06-adoption-and-measurement.md#maturity-levels](../docs/06-adoption-and-measurement.md#maturity-levels) |
| E13 | The release gate sits after the irreversible action; the status list lacks "in review". | L | U | Put the gate before the action and align the status values. | closed: [05-work-item-procedure.md#gates-come-before-the-action](../docs/05-work-item-procedure.md#gates-come-before-the-action) |

## Proposed guidebook structure

The three reviewers converged on splitting the single document into parts for three readers:
agents, people learning the method, and the author writing about it.

| Part | Content | Main reader |
|---|---|---|
| 0 README | One page: the thesis in three lines, the stages in one table, the maturity ladder, who reads what | Everyone |
| 1 Quick start | The minimum version (levels 1 and 2) and a first-day and first-week checklist | People |
| 2 Worked example | One synthetic item from proposed to done, with every artifact and gate | People, agents |
| 3 Method reference | Stages with trigger, output, exit criteria, how-to and anti-patterns; variants for greenfield, joining mid-flight, teams and regulated work | People, agents |
| 4 Work-item procedure | Phases, gate checklists, risk tiers, irreversible-action list, expedite path, rules from incidents | People, agents |
| 5 Maturity and scaling | When to add a stage, when to remove one, how to measure | People |
| 6 Beyond software | The existing table plus one non-software walkthrough | People, blog |
| 7 Templates | Context file, backlog fields, status values, verification script spec, reviewer brief, skill skeleton, request pack, audit checklist | Agents |
| 8 Agent instruction file | At most 150 lines of MUST and MUST NOT rules, paths, gates and stop conditions; defaults to the lowest level | Agents |
| 9 Case study | The anonymized project, timeline, results, limits | Blog |
| 10 Why it works | Established practice crosswalk, roadmap parallel, principles, sources | Blog, skeptics |
| 11 Glossary and references | One term per concept; every reference cited | Everyone |
