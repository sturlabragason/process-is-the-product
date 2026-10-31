# Tools

## verify_status.py

Reference status verification script for stage 8 of the method. It reads the backlog table and
refuses any row whose status is not backed by the fields that status needs. Python 3, standard
library only. Copy it to `tools/verify_status.py` in your project.

```bash
python3 tools/verify_status.py                       # checks docs/backlog.md
python3 tools/verify_status.py path/to/backlog.md    # another file
python3 tools/verify_status.py docs/backlog.md --check-paths [--root .]
```

Exit codes: `0` no violations, `1` violations (one `ID: problem` line each on stdout), `2` usage
or parse error (file missing, no backlog table, missing columns, ragged rows).

Run it before publishing any status change. A setup or a build step is not done until it exits 0.

### What it reads

The first markdown table whose header has both `ID` and `Status`. A status summary table above it
is ignored. Header names are matched case-insensitively. Required columns: ID, Type, Status,
Risk tier, Blocked by, Evidence, Approvals. The other backlog fields from the shared contract may
be present and are not checked, except Evidence kind (values only).

### Rules

| # | Rule |
|---|---|
| 1 | IDs are present and unique. |
| 2 | Status is exactly one of `proposed`, `ready`, `in-progress`, `in-review`, `merged`, `done`, `blocked`, `dropped`. |
| 3 | Type (if set) is `build`, `decision`, `discovery`, `compliance` or `ops`; Risk tier (if set) is `local`, `shared` or `irreversible`; Evidence kind (if set) is `computational` or `inferential`. |
| 4 | A `done` row has Evidence that is a URL, a markdown link or a path. With `--check-paths`, relative paths must exist relative to the backlog's folder or to `--root`. URLs are not fetched. |
| 5 | A `done` row has a Risk tier. |
| 6 | Approvals match status and tier (see the table below). An `expedite` entry counts as `plan`, `change` and `release`. |
| 7 | A `done` row with Evidence kind `inferential` has an `evidence` approval. |
| 8 | A `blocked` row has Blocked by with a date (`YYYY-MM-DD`). |
| 9 | A `done` row of Type `decision` has an ADR path (`decisions/NNNN-title.md`) in Evidence. |
| 10 | Every Approvals entry, on any row, is well formed and names a known gate. |

Approvals needed, following the status transitions in
[docs/05-work-item-procedure.md](../docs/05-work-item-procedure.md):

| Status | Risk tier | Needs |
|---|---|---|
| `in-progress`, `in-review`, `merged`, `done` | shared, irreversible | `plan` (or `expedite`) |
| `merged`, `done` | every tier | `change` (or `expedite`) |
| `done` | irreversible | `release` (or `expedite`), with at least two distinct approvers across `release` and `expedite` entries |

`proposed`, `ready` and `dropped` need none. `blocked` rows are not checked for approvals, since
the script cannot see the status they had before.

### Approvals format

```
gate:who@YYYY-MM-DD; gate:who@YYYY-MM-DD
plan:alice@2026-10-01; change:bob@2026-10-02; release:carol@2026-10-03; release:dave@2026-10-03
```

`gate` is `plan`, `change`, `release`, `launch-readiness`, `expedite` or `evidence`. `who` is a
handle (letters, digits, `.`, `-`, `_`). The cell is an index; the full record, one line
`gate | item | who | when | what exactly was approved | link`, lives in the approval log
`docs/approvals.md` (template: [templates/docs/approvals.md](../templates/docs/approvals.md)).

### Limits

- It checks the current state of each row, not the history, so it cannot prove that transitions
  happened in order. It does not compare approval dates with merge or release times.
- It accepts `dropped` without checking for a reason or who decided.
- It accepts `expedite` in place of `plan`, `change` and `release` (an irreversible item still
  needs a second human, which the backfill adds) but cannot see whether the rest of the incident
  backfill was completed. The change approver and the stage 9 audit check that.
- It cannot tell whether a release is a first production release, so it does not require
  `launch-readiness`, and it cannot check that the second release approver is not the owner or
  the author.
- It checks that evidence is a link or a path, not that the evidence proves the claim. A reviewer
  or the stage 9 audit does that.
- The gate set per risk tier follows
  [docs/05-work-item-procedure.md](../docs/05-work-item-procedure.md). If your project changes it,
  edit the constants (`REQUIRED_GATES`, `PLAN_STATUSES`, `CHANGE_STATUSES`,
  `MIN_RELEASE_APPROVERS`) at the top of the script and the tests.

## Tests

```bash
python3 -m pytest -q tools/
```

The tests cover each rule with passing and failing cases, the exit codes, and check that the
example in [templates/docs/backlog.md](../templates/docs/backlog.md) passes.
