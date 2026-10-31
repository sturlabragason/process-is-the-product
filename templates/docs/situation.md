# Situation analysis

<!--
Stage 1. Copy to docs/situation.md. Fill in ONE of the two analysis sections and delete the other:
- existing work (brownfield): the gap analysis;
- new work (greenfield): the assumption register.
Joining a running project: limit the analysis to one workstream, the one with the costliest
current failure. Keep the decision log in both cases.
Exit criteria: every input is accounted for, and every open question or assumption has an owner
(and, for assumptions, a test). Delete these comments when you fill the file in.
-->

Owner: <!-- alice -->
Scope: <!-- whole project, or one workstream -->
Last updated: <!-- YYYY-MM-DD -->

## Inputs

<!-- Every input you were given or found. Nothing is left out. -->

| Input | Where it is | Quality | Checked by | Notes |
|---|---|---|---|---|
| <!-- requirements document --> | <!-- path or link --> | <!-- confirmed, unconfirmed, wrong --> | <!-- alice --> | |

## Gap analysis (existing work)

<!-- For each area: what exists, what should exist, and the gap. Check claims against the
source of truth and mark each one confirmed, unconfirmed or wrong, with evidence. -->

| Area | Current state (as-is) | Target state (to-be) | Gap | Evidence | Owner |
|---|---|---|---|---|---|
| | | | | | |

### Triggers already firing

<!-- Which stage triggers from the method are already firing, and what each one costs today.
Start at the stage with the costliest current failure. -->

| Trigger | Where you see it | Cost today | Stage it points to |
|---|---|---|---|
| | | | |

## Assumption register (new work)

<!-- There is no as-is state yet, so list what you are assuming. Riskiest first.
Each assumption gets an owner and a test that would prove it wrong. Tests become discovery
items in the backlog. -->

| # | Assumption | Risk if wrong | Owner | Test | Deadline | Result |
|---|---|---|---|---|---|---|
| 1 | | high | | | YYYY-MM-DD | <!-- open, held, failed --> |

## Open questions

| Question | Owner | Needed by | Decision item |
|---|---|---|---|
| | | YYYY-MM-DD | <!-- backlog ID, if it is a decision --> |

## Decision log

<!-- Dated, one line per decision. Larger decisions get an ADR in docs/decisions/. -->

| Date | Decision | Decided by | ADR |
|---|---|---|---|
| YYYY-MM-DD | | | <!-- docs/decisions/NNNN-title.md or n/a --> |
