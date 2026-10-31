# AGENTS.md

<!--
Context file (stage 2). Every agent and every new person loads this file first.
Copy to AGENTS.md at the repository root. If a tool reads another name (for example CLAUDE.md),
link that name to this file instead of keeping a second copy.
Keep it short: a new agent must be able to start useful work from this file alone.
This file is code: it has an owner and every change goes through review (see "Owner and review").
Editing an existing context or instruction file is an irreversible action: it needs a recorded
human approval first. Delete these comments when you fill the file in.
-->

## What this project is

<!-- Two or three sentences: the goal, who it is for, and the current phase from docs/plan.md. -->

## Repository layout

<!-- Only folders an agent needs. Remove lines for folders that do not exist. -->

| Path | What is there |
|---|---|
| `AGENTS.md` | This context file |
| `docs/ai-stance.md` | Approved AI tools, data classes, production access, budget |
| `docs/situation.md` | Gap analysis or assumption register, and the decision log |
| `docs/roles.md` | Areas, owners, reviewers, gate owners |
| `docs/plan.md` | Phases with entry and exit criteria |
| `docs/backlog.md` | The backlog (or the link to the tracker it is a view of) |
| `docs/approvals.md` | Approval log, one line per gate approval |
| `docs/decisions/` | Architecture decision records, `NNNN-title.md` |
| `.agents/skills/work-item/SKILL.md` | The standard procedure for one work item |
| `tools/verify_status.py` | Status verification script |
| `src/` | <!-- source code --> |

## AI stance

Read [docs/ai-stance.md](docs/ai-stance.md) before using any tool or data. It lists the approved
tools, the data classes allowed in agent context, and production access.

## Roles

<!-- One line per role. Full matrix in docs/roles.md. Add a role only when its trigger has fired:
two agents changed the same thing, or an author reviewed their own work. -->

| Role | Owns (single writer) | Reviewed by |
|---|---|---|
| <!-- e.g. builder --> | <!-- e.g. src/ --> | <!-- e.g. reviewer, read-only --> |

## Invariants

<!-- Rules that are never negotiated. Each one should be checkable. Keep the list short. -->

1. Done means verified by a command or a linked record; a system reporting its own success is not
   evidence.
2. No stored secrets in the repository.
3. No production personal data in agent context.
4. Irreversible actions need a recorded human approval first (list in
   [.agents/skills/work-item/SKILL.md](.agents/skills/work-item/SKILL.md)).
5. Agents never choose an option a human has not decided; they open a decision item.
6. <!-- project specific, for example a cost budget per item -->

## Authoritative system per capability

<!-- Where two systems run side by side (old and new, tracker and file), name the one that wins.
The migration between them is its own workstream with dated cut-over criteria. -->

| Capability | Authoritative system | Other system and its role | Cut-over date |
|---|---|---|---|
| Backlog | <!-- docs/backlog.md or tracker URL --> | <!-- e.g. tracker, read-only view --> | <!-- YYYY-MM-DD or n/a --> |
| <!-- e.g. user login --> | | | |

## How work is done

- Backlog: [docs/backlog.md](docs/backlog.md). Status values: `proposed`, `ready`,
  `in-progress`, `in-review`, `merged`, `done`, `blocked`, `dropped`.
- Standard procedure: [.agents/skills/work-item/SKILL.md](.agents/skills/work-item/SKILL.md).
  "Run item N" means: follow that procedure for row N.
- Before publishing any status change: `python3 tools/verify_status.py docs/backlog.md` exits 0.
- One workspace per item (for example a git worktree), one owner per workspace.

## Owner and review

- Owner of this file: <!-- alice -->
- Changes go through: <!-- pull request reviewed by bob, or the code owners rule for AGENTS.md -->
- Personal overlays (your own prompt files) may change style, never an invariant.
- Last audited: <!-- YYYY-MM-DD, see the stage 9 audit checklist -->
