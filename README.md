# AI-native engineering: the process is the product

A guidebook for running projects with AI agents. When agents make producing work cheap, what
stays expensive is knowing the current state, deciding what comes next and proving that work is
done. The method answers that with ten stages, each added only when a named failure (its
trigger) shows up, so the lasting product is the system that produces and verifies the work.

## Who it is for and where to start

| You are | Start with | Then |
|---|---|---|
| A person learning the method | [Quick start](docs/01-quick-start.md) | [Worked example](docs/02-worked-example.md), [method reference](docs/03-method.md) |
| An agent taking instructions | [agent/METHOD.agent.md](agent/METHOD.agent.md): copy it into the project you work on | [Templates](templates/) for the files it names |
| Writing about the method | [Case study](docs/08-case-study.md) | [Why it works](docs/09-why-it-works.md), [references](docs/11-references.md) |

Joining a running project, starting from nothing, working in a team or under audit: read
[variants](docs/04-variants.md) after the quick start.

## The ten stages

Add a stage when its trigger fires, not before. Most projects start with stages 0 to 2. The
[maturity levels](docs/06-adoption-and-measurement.md) group the stages and say when to move up.

| Stage | Purpose | Output |
|---|---|---|
| 0 AI stance | Decide which tools, data and access agents get, and the budget | `docs/ai-stance.md` |
| 1 Situation analysis | Find out what is true before planning: gap analysis or assumption register | `docs/situation.md` |
| 2 Context file | Give every agent and person the same starting point | `AGENTS.md` |
| 3 Roles and separation of duties | One writer per area; nobody approves their own work | `docs/roles.md` |
| 4 Phased plan with stage gates | Nothing starts before its dependencies; slow requests leave early | `docs/plan.md` |
| 5 Backlog | Small work items, each with a check that proves it done | `docs/backlog.md` |
| 6 Work isolation | One workspace and one owner per item | one git worktree per item |
| 7 Standard procedure | Every item follows the same steps, with human gates | `.agents/skills/work-item/SKILL.md` |
| 8 Status verification | Reported status matches reality, checked by a script | `tools/verify_status.py` |
| 9 Retrospective and harness maintenance | Keep the method's own documents true | dated audit findings as `ops` items |

The work item procedure behind stage 7 (phases, gates, risk tiers, evidence rules) is in
[docs/05-work-item-procedure.md](docs/05-work-item-procedure.md).

## Repository map

| Path | What is there |
|---|---|
| [docs/01-quick-start.md](docs/01-quick-start.md) | The first hour and the first week on an existing project |
| [docs/02-worked-example.md](docs/02-worked-example.md) | One synthetic work item from `proposed` to `done`, every artifact shown |
| [docs/03-method.md](docs/03-method.md) | Stages 0 to 9: purpose, trigger, output, exit criteria, how-to |
| [docs/04-variants.md](docs/04-variants.md) | Greenfield, joining mid-flight, teams, regulated work |
| [docs/05-work-item-procedure.md](docs/05-work-item-procedure.md) | Phases, gates, risk tiers, irreversible actions, expedite path, evidence |
| [docs/06-adoption-and-measurement.md](docs/06-adoption-and-measurement.md) | Maturity levels, removing process, metrics, bringing people in |
| [docs/07-beyond-software.md](docs/07-beyond-software.md) | The method on non-software projects |
| [docs/08-case-study.md](docs/08-case-study.md) | The anonymized project the method came from, with its limits |
| [docs/09-why-it-works.md](docs/09-why-it-works.md) | The argument and the crosswalk to established practice |
| [docs/10-glossary.md](docs/10-glossary.md) | One term per concept |
| [docs/11-references.md](docs/11-references.md) | Every source cited |
| [templates/](templates/) | Files a project copies in: context file, stage outputs, backlog, approval log, standard procedure, checklists |
| [tools/](tools/) | The reference status verification script and its tests |
| [agent/](agent/) | The method as MUST and MUST NOT rules for agents |
| [research/](research/) | Source material: the method as one document, the gap report, source checks |

## Status check and tests

Check a backlog against the status rules. Exit code 0 means no violations, 1 means violations
(one line per problem), 2 means the file could not be read or parsed.

```bash
python3 tools/verify_status.py docs/backlog.md
```

In this repository there is no `docs/backlog.md`; try it on the template instead:

```bash
python3 tools/verify_status.py templates/docs/backlog.md
```

Run the script's tests:

```bash
python3 -m pytest -q tools/
```

Rules and limits of the script: [tools/README.md](tools/README.md).

## Status

The method was extracted from one project: one engineer directing AI agents for about five and a
half weeks on an existing system. About 100 work items were planned; everything in scope was done
with evidence from the live system, and the rest was the planned roadmap.
The case is one engineer's self-report with no measured baseline. The parts for teams, greenfield work, regulated work and
non-software projects are untested proposals, designed from simulated runs and marked as such
where they appear. See [research/gap-report.md](research/gap-report.md) for the gaps and how each
was addressed.
