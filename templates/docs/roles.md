# Roles

<!--
Stage 3. Copy to docs/roles.md. Add this file when its trigger fires: two agents change the same
thing, or whoever did the work also reviews it.
Exit criteria: for every area you can name its one owner and its reviewer.
Add roles as needs appear; do not copy a role count from an example. Delete these comments
when you fill the file in.
-->

Owner of this file: <!-- alice -->
Last updated: <!-- YYYY-MM-DD -->

## Areas

<!-- One owner per area (a single writer). Reviewers are independent and read-only. -->

| Area | Paths or resources | Owner (single writer) | Reviewer (read-only) | Skills loaded |
|---|---|---|---|---|
| <!-- application code --> | <!-- src/ --> | <!-- builder agent, run by alice --> | <!-- reviewer agent, then bob --> | <!-- work-item --> |
| Context file | `AGENTS.md` | <!-- alice --> | <!-- bob --> | |
| Backlog | `docs/backlog.md` | <!-- alice --> | <!-- bob --> | |

## Gate owner matrix

<!-- Who approves each gate for each risk tier. Map existing pull request review and code owners
onto the change gate. An agent reviewer adds to human approval; where a rule requires a human, it
does not replace one. Human review capacity is a work-in-progress limit: do not start more items
than the gate owners can approve. Gate rules: docs/05-work-item-procedure.md in the guidebook. -->

| Gate | local | shared | irreversible | Backup approver |
|---|---|---|---|---|
| plan | not required | <!-- alice --> | <!-- alice --> | <!-- bob --> |
| change | <!-- alice --> | <!-- bob, code owner, not the author --> | <!-- bob --> | <!-- carol --> |
| release | not required | not required | <!-- carol, plus a second human who is not the owner or the author --> | <!-- alice --> |
| launch-readiness | not required | not required | <!-- carol, plus the second human --> | <!-- alice --> |
| expedite | <!-- incident lead --> | <!-- incident lead --> | <!-- incident lead --> | <!-- on-call lead --> |
| evidence (inferential) | <!-- product owner --> | <!-- product owner --> | <!-- product owner --> | <!-- alice --> |

Work-in-progress limit per gate owner: <!-- e.g. 3 items waiting -->

## Agent roles

<!-- Only when you use more than one agent role. Each role gets its own context and permissions. -->

| Role | Purpose | Permissions | Gets | Never gets |
|---|---|---|---|---|
| Builder | Makes the change in its own workspace | Write to its workspace | Row, specification, acceptance criteria | Production credentials |
| Reviewer | Checks the change | Read-only | Change and acceptance criteria | The author's reasoning |
