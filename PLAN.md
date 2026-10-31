# Plan: from method doc to guidebook

Date: 2026-10-31. Inputs: `research/method-v5.md` (the method as one document) and
`research/gap-report.md` (39 gaps found by three simulated runs). Goal: a guidebook for
AI-native engineering that serves three readers (agents, people learning the method, and the
author writing about it) and closes the open gaps.

## Repository layout

```
README.md                    one-page overview, who reads what
PLAN.md                      this file
docs/
  01-quick-start.md          minimum version (levels 1 and 2), first day, first week
  02-worked-example.md       one synthetic item from proposed to done, every artifact shown
  03-method.md               stages 0 to 9: trigger, output, exit criteria, how-to, anti-patterns
  04-variants.md             greenfield, joining mid-flight, teams, regulated work
  05-work-item-procedure.md  phases, gates, risk tiers, irreversible actions, expedite path, evidence rules
  06-adoption-and-measurement.md  maturity levels, adding and removing process, change management, metrics
  07-beyond-software.md      non-software projects, with one walkthrough
  08-case-study.md           the anonymized project, timeline, results, limits
  09-why-it-works.md         established practice crosswalk, roadmap parallel, principles
  10-glossary.md             one term per concept
  11-references.md           every reference cited somewhere, every quote verified
templates/                   files a project copies in
agent/METHOD.agent.md        condensed MUST / MUST NOT rules for agents (at most 150 lines)
tools/verify_status.py       reference status verification script, with tests
research/                    source material: method v5, gap report, source verification notes
```

## Who closes which gaps

Five parallel authoring agents (Opus), each owning separate files so nothing collides. Then
a sequential pass for the parts that depend on them, then an independent review.

| Wave | Agent | Files | Gaps closed |
|---|---|---|---|
| 1 | method | `docs/03-method.md` | A2 situation analysis, A3 anticipated triggers, C7 discovery loop, C8 decision items, C2 security and privacy items, C1 stage 0 AI stance, C12 walking skeleton, B5 context file ownership, E3 terms |
| 1 | variants | `docs/04-variants.md` | A1 joining mid-flight, A4 one system of record, A5 backlog triage, A6 parallel systems, B7 team-level isolation, B6 agent reviewers and four-eyes |
| 1 | procedure | `docs/05-work-item-procedure.md` | B1 gate owners, B2 risk tiers, B3 expedite path, C3 testing as a sensor, C4 evidence quality, C5 audit-grade evidence, C9 observability, C10 cost budget, C11 inferential evidence, D3 irreversible actions, E13 gate order |
| 1 | adoption | `docs/06-adoption-and-measurement.md` | B4 change management, C6 measurement, C13 removing process, E12 maturity grouping, D4 over-building |
| 1 | tooling | `templates/*`, `tools/verify_status.py`, `tools/test_verify_status.py`, `agent/METHOD.agent.md` | D1 templates and paths, D2 script spec, D5 agent rules, D6 setup stop rule, D4 MUST NOT over-build |
| 2 | lead (me) | `docs/07`, `docs/08`, `docs/09`, `docs/10`, `docs/11` | moved from method v5; E2 how-to first, E11 limits section |
| 2 | onboarding | `README.md`, `docs/01-quick-start.md`, `docs/02-worked-example.md` | E1 quick start, worked example; reads wave 1 output |
| 3 | reviewer | read-only | consistency across files, terms, links, claims, anonymity |

## Shared contract (all agents follow this)

**Stages.** 0 AI stance. 1 Situation analysis (gap analysis on existing work, assumption
register on new work). 2 Context file. 3 Roles and separation of duties. 4 Phased plan with stage
gates. 5 Backlog. 6 Work isolation. 7 Standard procedure. 8 Status verification. 9 Retrospective
and harness maintenance.

**Terms.** Use these and no synonyms: *context file*, *backlog*, *work item* (or *item*),
*standard procedure*, *skill* (the packaged form of a procedure or knowledge for an agent),
*gate*, *owner*, *reviewer*, *acceptance criteria*, *evidence*, *status verification*,
*risk tier*. "Runbook" appears only in the case study, as the name the project used for its
backlog.

**Status values** (exact, lower case): `proposed`, `ready`, `in-progress`, `in-review`,
`merged`, `done`, `blocked`, `dropped`. `merged` means merged but not yet verified in the target
environment. `done` requires evidence.

**Backlog fields:** ID, Title, Type (`build`, `decision`, `discovery`, `compliance`, `ops`),
Status, Owner, Risk tier, Priority, Workstream, Scope, Specification, Acceptance criteria,
Evidence kind (`computational` or `inferential`), Unblocks, Blocked by (with date), Evidence,
Approvals (gate, who, when).

**Risk tiers** (names, not codes): *local* (reversible, affects only the item's own workspace:
1 gate), *shared* (affects shared code, environments or other people: 2 gates), *irreversible*
(cannot be undone, touches production, money, personal data, or regulated scope: 3 gates and a
second human).

**Default paths** in a project using the method: `AGENTS.md` (context file),
`docs/ai-stance.md`, `docs/situation.md`, `docs/roles.md`, `docs/plan.md`, `docs/backlog.md`
(or a view of an existing tracker), `docs/decisions/NNNN-title.md` (ADRs),
`.agents/skills/work-item/SKILL.md` (standard procedure), `tools/verify_status.py`.

**Writing rules.**
- Plain language; no em or en dashes; sentence-case headings; `style-lint` must pass.
- No client, product, people or vendor-of-client names.
- Quote only sources listed in `research/method-v5.md` section 15, using the exact wording
  there. No new quotes unless verified by fetching, and recorded in
  `research/source-verification.md`.
- Mark anything not tested on a real project as "untested proposal". The case covers one
  project; the gap fixes are design, not experience.

## Done checks

```bash
for f in README.md docs/*.md agent/*.md templates/*.md; do ~/.agents/skills/style-lint/scripts/style-lint.sh "$f" || exit 1; done
! grep -rIlP '[\x{2013}\x{2014}]' --include='*.md' --exclude-dir=research .
! grep -rIliF -f .names-denylist --exclude-dir=.git --exclude=.names-denylist .   # denylist is local, never committed
python3 -m pytest -q tools/
```

Every gap in `research/gap-report.md` gets a status and a link to the file that closes it.

## Framing rule for the case (from the author)

The case is an exemplary run of the method. Everything in scope was done with evidence;
the rest of the backlog at day 39 was the planned roadmap, not unfinished work. The project's difficulties came from its
conditions (compressed timeline, slow external approvals, inputs of unknown quality), not from
the method. Never present the open roadmap as a weakness. Valid limits: one case, one engineer,
self-reported, no measured baseline.
