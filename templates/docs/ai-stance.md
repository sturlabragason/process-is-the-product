# AI stance

<!--
Stage 0. Copy to docs/ai-stance.md. A short, clear and communicated statement of how this
project uses AI. Agree it with the people who own security, data and budget before agents start.
Link it from AGENTS.md. Delete these comments when you fill the file in.
-->

Owner: <!-- alice -->
Approved by: <!-- bob, YYYY-MM-DD -->
Review date: <!-- YYYY-MM-DD -->

## Approved tools

<!-- Tools and models people and agents may use on this project, and where they may run. -->

| Tool or model | Allowed for | Not allowed for | Where it runs |
|---|---|---|---|
| <!-- coding agent --> | <!-- code in this repo --> | <!-- production consoles --> | <!-- local workstation --> |

## Data classes allowed in agent context

<!-- Use the organization's data classification if one exists. -->

| Data class | Allowed in agent context | Notes |
|---|---|---|
| Public | yes | |
| Internal (code, docs) | yes | Approved tools only |
| Confidential | <!-- yes or no --> | <!-- e.g. only with a tool that does not retain data --> |
| Personal data from production | no | Use synthetic or masked data |
| Secrets and credentials | no | Never paste them into a prompt or a file |

## Production access

<!-- Default: agents have no production credentials. Reading production data with credentials is
an irreversible action and needs a recorded human approval first. -->

- Agents may: <!-- read dashboards with a read-only account, or nothing -->
- Agents may not: <!-- apply, deploy, delete, change permissions or secrets -->
- Who starts actions in production: <!-- a named human -->

## Budget

| Item | Limit | Owner | What happens on overrun |
|---|---|---|---|
| Model and token cost per month | <!-- amount --> | <!-- alice --> | Stop and ask the owner |
| Cost per work item | <!-- amount --> | <!-- alice --> | Stop rule: pause the item, record it |

## Questions and exceptions

<!-- Who to ask, and how an exception is recorded (for example as an ADR in docs/decisions/). -->
