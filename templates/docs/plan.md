# Plan

<!--
Stage 4. Copy to docs/plan.md. Add it when work starts before its dependencies are ready, or when
slow external approvals could block you late. Anticipated trigger: anything with a lead time over
a week goes in the plan on day 1.
Exit criteria: nothing can start before its dependencies are done, and every external request has
been sent. Delete these comments when you fill the file in.
-->

Owner: <!-- alice -->
Last updated: <!-- YYYY-MM-DD -->

## Phases

<!-- Start with as few phases as the work needs. Phase 0 is often a walking skeleton:
build, test and deploy an empty service to every environment, so "verified" has a target. -->

| # | Phase | Owner | Entry criteria | Exit criteria (checkable) | Gate owner | Status |
|---|---|---|---|---|---|---|
| 0 | Walking skeleton | | Repository and dev environment exist | Pipeline deploys to dev; health check returns 200 | | <!-- not started, open, closed --> |
| 1 | | | Phase 0 exit criteria met | | | |

A phase gate is a decision against the exit criteria, not a status update. Record it in the
approval log, `docs/approvals.md`.

## Long-lead items

<!-- External approvals, access requests, procurement, legal reviews. Bundle them in one request
pack (see request-pack.md) and send it as early as possible. -->

| Item | From whom | Lead time | Needed by phase | Sent on | Status |
|---|---|---|---|---|---|
| | | <!-- days --> | | YYYY-MM-DD | <!-- not sent, sent, granted, refused --> |

## Pre-mortem

<!-- Day 1: imagine the project has failed. List the reasons. Each one gets a mitigation and an
owner, and the costly ones become backlog items now instead of waiting for the trigger. -->

| It failed because | Likelihood | Mitigation | Owner | Backlog item |
|---|---|---|---|---|
| | <!-- low, medium, high --> | | | |

## Dependencies

<!-- Optional: which phases or items unblock which. Keep it in the backlog Unblocks field if that
is enough. -->
