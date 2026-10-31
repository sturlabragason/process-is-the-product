# Worked example: one item from proposed to done

This page follows one made-up work item through the [work item procedure](05-work-item-procedure.md),
from `proposed` to `done`. Every artifact is shown as it changes: the backlog row, the approval
records, the reviewer brief, the evidence and the output of the status verification script. The
project and the people are invented. The script output is real: it was produced by running
[tools/verify_status.py](../tools/verify_status.py) on the rows shown here.

## The project

A small team runs an internal search API. Three other internal services call it. One of them
sometimes sends bursts of thousands of requests and slows the API down for everyone. The team
wants a rate limit per client key.

| Handle | Role in this example |
|---|---|
| alice | Owner of the item. She directs the agents that do the work. |
| bob | Tech lead. Approves the plan gate. |
| carol | Code owner of `src/middleware/`. Approves the change gate. |
| dave | Security contact. Appears only in the irreversible variant at the end. |

The project uses stages 0 to 8: it has `AGENTS.md`, `docs/backlog.md`, `docs/approvals.md`,
`docs/roles.md`, one git worktree per item, and `tools/verify_status.py`. Staging deploys
automatically from `main` after every merge. Production is deployed by hand.

## Step 1: proposed

alice adds a row. Moving from (new) to `proposed` needs an ID, a title and a type, nothing else.

| ID | Title | Type | Status | Owner | Risk tier | Priority | Workstream | Scope | Specification | Acceptance criteria | Evidence kind | Unblocks | Blocked by | Evidence | Approvals |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B-014 | Rate limit the search endpoint | build | proposed | | | | | | | | | | | | |

## Step 2: ready

`proposed` to `ready` needs an owner, a risk tier, scope, specification, acceptance criteria that
a check can prove true or false, and an evidence kind.

alice classifies the tier with the three questions from
[how to classify an item](05-work-item-procedure.md#how-to-classify-an-item):

1. Does any step reach production, delete, spend, change permissions or touch personal data? No.
   This item stops at staging. Turning the limit on in production is a separate item, B-015.
2. Once merged, does it change code or environments other people depend on? Yes: shared code,
   and a staging environment the three calling teams test against.
3. So the tier is `shared`: plan gate and change gate, no release gate. The automatic deploy to
   staging is covered by the change gate if the change approval names it.

| ID | Title | Type | Status | Owner | Risk tier | Priority | Workstream | Scope | Specification | Acceptance criteria | Evidence kind | Unblocks | Blocked by | Evidence | Approvals |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B-014 | Rate limit the search endpoint | build | ready | alice | shared | 2 | api | `src/middleware/rate_limit.py`, `config/limits.yaml`, `tests/test_rate_limit.py` | Add a per client key limit of 100 requests per 60 seconds to `GET /v1/search`. Over the limit, return 429 with a `Retry-After` header. The limit is set per environment in `config/limits.yaml`. | In staging, requests 1 to 100 within 60 seconds from one client key return 200 and request 101 returns 429 with a `Retry-After` header; `tests/test_rate_limit.py` passes in CI on the merge commit. | computational | B-015 | | | |

## Step 3: review, and the snag

The agent runs the review phase read-only. It checks the claims in the row against the code, and
records a baseline in staging before anything changes:

```
$ for i in $(seq 1 101); do curl -s -o /dev/null -w '%{http_code}\n' \
    -H 'X-Client-Key: test-b014' 'https://search.staging.example.internal/v1/search?q=x'; done | sort | uniq -c
    101 200
```

All 101 requests succeed: there is no limit today. The agent writes the plan into the item's
notes: three files, a fixed window counter in the existing cache, one new test file, no new
resources, no irreversible actions, and an estimate of two agent runs.

Then the snag. alice reads the plan, likes it, and sets the row to `in-progress` so the agent can
start the build. Before any status change is published, the procedure runs the script:

```
$ python3 tools/verify_status.py docs/backlog.md
B-014: in-progress item with shared risk tier needs a 'plan' (or expedite) approval
1 problem(s) in 1 row(s)
```

Exit code 1. `ready` to `in-progress` at tier `shared` requires a `plan` approval record, and
there is none. alice is the owner, so she cannot approve her own plan; in a small team the plan
approver is a peer or the tech lead. The edit was never published and no worktree exists yet, so
nothing has to be undone. alice puts the row back to `ready` and the agent sends bob the request:
the gate, the item, the plan, the expected changes (3 files, 0 new resources, staging only) and
the baseline.

bob approves the next morning in the item's issue thread. alice appends the record to
`docs/approvals.md`:

```
plan | B-014 | bob, tech lead | 2026-11-03T10:15+01:00 | plan in B-014: fixed window limit on GET /v1/search, 3 files, 0 new resources, staging only | https://git.example.com/search-api/issues/14#note-5
```

and adds the index entry to the row. Now the transition is allowed:

| ID | Status | Approvals |
|---|---|---|
| B-014 | in-progress | plan:bob@2026-11-03 |

(Other cells unchanged.)

```
$ python3 tools/verify_status.py docs/backlog.md
ok: 1 row(s) checked
```

The script cannot see the order of events. It would also pass if bob had approved after the
build started. The rule that the approval comes first is kept by the procedure, and checked by
comparing the time in the approval log with the time the worktree was created.

## Step 4: build, then in-review

The agent creates the item's workspace, writes the tests first and then the change:

```
git worktree add ../wt-B-014 -b item/B-014
```

It runs the tests locally, keeps their output, and opens pull request 88. `in-progress` to
`in-review` needs a workspace, passing tests for the acceptance criteria, an open pull request and
a passing status check. All four hold, so alice sets `in-review`. The Approvals cell is unchanged.

## Step 5: independent review

A reviewer agent with read-only access gets the [reviewer brief](../templates/reviewer-brief.md).
It contains the change and the acceptance criteria, and nothing about how the author got there.

```
Item: B-014, Rate limit the search endpoint
Risk tier: shared
Your access: read-only. Do not change anything.

The change: https://git.example.com/search-api/pulls/88 (commits 5b20c11..7e3a9f2)
Acceptance criteria: In staging, requests 1 to 100 within 60 seconds from one client key return
200 and request 101 returns 429 with a Retry-After header; tests/test_rate_limit.py passes in CI
on the merge commit.
Scope: src/middleware/rate_limit.py, config/limits.yaml, tests/test_rate_limit.py
What to check: the six questions from the template.
Not included on purpose: the author's reasoning, chat history and opinion of the change.
```

The reviewer returns:

```
Item: B-014
Reviewer: reviewer agent (read-only)
Date: 2026-11-04
Verdict: changes needed

Criteria:
- 429 on request 101 with Retry-After: met in tests, tests/test_rate_limit.py:22
- 1 to 100 return 200: met in tests, tests/test_rate_limit.py:14
- CI on the merge commit: not checkable before merge

Findings (most severe first):
- [medium] tests/test_rate_limit.py: no test asserts the Retry-After header; the criterion names it.
- [low] src/middleware/rate_limit.py:31: a missing client key falls into one shared bucket; fine for scope, worth a note.

Out of scope changes: none
Checks run: python3 -m pytest -q tests/test_rate_limit.py (exit 0)
```

A reviewer that sends the item back moves it from `in-review` to `in-progress`, with the findings
recorded. The agent adds the missing assertion in the same worktree (commit 9d41e07), reruns the
tests, and alice sets `in-review` again. The low finding becomes a note in the pull request. The
reviewer's verdict is input to the change gate, not the gate.

## Step 6: change gate, then merged

`in-review` to `merged` needs a `change` approval dated before the merge, and a CI result on the
final commit. carol reviews pull request 88 at commit 9d41e07 and approves it in the hosting tool.
Because staging deploys automatically after merge, her approval names that deploy, so no release
gate is needed:

```
change | B-014 | carol, code owner of src/middleware | 2026-11-05T14:30+01:00 | commit 9d41e07 and pull request 88 description, merge to main and the automatic deploy to staging | https://git.example.com/search-api/pulls/88#review-3
```

alice merges at 14:41. The worktree is removed.

| ID | Status | Evidence | Approvals |
|---|---|---|---|
| B-014 | merged | | plan:bob@2026-11-03; change:carol@2026-11-05 |

```
$ python3 tools/verify_status.py docs/backlog.md
ok: 1 row(s) checked
```

`merged` is not `done`. The pipeline reports that the staging deploy succeeded, but a system
reporting its own success is not evidence.

## Step 7: verify in staging, then done

The next morning the agent runs the acceptance check against staging and saves the commands and
their output to `evidence/B-014-staging.txt`:

```
$ curl -s https://search.staging.example.internal/version
9d41e07
$ for i in $(seq 1 101); do curl -s -o /dev/null -w '%{http_code}\n' \
    -H 'X-Client-Key: test-b014' 'https://search.staging.example.internal/v1/search?q=x'; done | sort | uniq -c
    100 200
      1 429
$ curl -s -D - -o /dev/null -H 'X-Client-Key: test-b014' \
    'https://search.staging.example.internal/v1/search?q=x' | grep -i '^retry-after'
retry-after: 41
```

The first command shows staging runs the merged commit. The second matches the baseline from step
3, now with the limit in place. CI run 2210 on commit 9d41e07 passed with the new tests. alice
writes the done entry before closing the item:

| ID | Title | Type | Status | Owner | Risk tier | Priority | Workstream | Scope | Specification | Acceptance criteria | Evidence kind | Unblocks | Blocked by | Evidence | Approvals |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B-014 | Rate limit the search endpoint | build | done | alice | shared | 2 | api | `src/middleware/rate_limit.py`, `config/limits.yaml`, `tests/test_rate_limit.py` | Add a per client key limit of 100 requests per 60 seconds to `GET /v1/search`. Over the limit, return 429 with a `Retry-After` header. The limit is set per environment in `config/limits.yaml`. | In staging, requests 1 to 100 within 60 seconds from one client key return 200 and request 101 returns 429 with a `Retry-After` header; `tests/test_rate_limit.py` passes in CI on the merge commit. | computational | B-015 | | [CI run 2210](https://ci.example.com/runs/2210), `evidence/B-014-staging.txt` | plan:bob@2026-11-03; change:carol@2026-11-05 |

```
$ python3 tools/verify_status.py docs/backlog.md
ok: 1 row(s) checked
```

Exit code 0, so the status change is published. B-015, turning the limit on in production, can
now move to `ready`.

## Summary of transitions

| From | To | What allowed it |
|---|---|---|
| (new) | `proposed` | ID, title, type |
| `proposed` | `ready` | Owner, risk tier, scope, specification, checkable acceptance criteria, evidence kind |
| `ready` | `in-progress` | Review done and a `plan` record (the snag: missing at first) |
| `in-progress` | `in-review` | Worktree, passing tests, open pull request, script passes |
| `in-review` | `in-progress` | Reviewer findings recorded |
| `in-review` | `merged` | `change` record dated before the merge, CI on the final commit |
| `merged` | `done` | Evidence from staging, linked in the row |

## The same item at other risk tiers

At tier `local` the item would have to stay inside its own workspace, for example a throwaway
comparison of two limiter algorithms that nobody else uses. There is no plan gate: it moves from
`ready` to `in-progress` when the review is done, and the snag above cannot happen. The one gate
is the change gate, approved before merge. The Approvals cell would hold at
most `change:carol@2026-11-05`.

At tier `irreversible`, for example if B-014 also switched the limit on in production, it needs a
plan gate, a change gate and a release gate before `done`. The release gate approves the exact
action (the commit, the target, the counted changes and the rollback) before it runs, and needs a
second human who is not the owner or the author. With only bob's release approval the script
refuses the `done` row:

```
$ python3 tools/verify_status.py docs/backlog.md
B-014: irreversible tier needs release approvals from at least 2 distinct approvers, found 1
1 problem(s) in 1 row(s)
```

With `release:bob@2026-11-06; release:dave@2026-11-06` added, and both lines in the approval log,
it passes. A first production release of the service would also need a `launch-readiness` record,
which the script cannot check.
