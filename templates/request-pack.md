# Request pack

<!--
Bundled long-lead external requests (stage 4). One pack per external party: their approvals and
access take longest, so send everything they need at once, as early as possible.
Sending it is an irreversible action (a message to an external party): get a recorded human
release approval first, from two distinct humans, logged in docs/approvals.md in the format from
.agents/skills/work-item/gate-checklists.md. Track each request in docs/plan.md under
long-lead items. Delete these comments before sending.
-->

To: <!-- team or role, not a personal name if a shared queue exists -->
From: <!-- alice -->
Date sent: YYYY-MM-DD
Reply needed by: YYYY-MM-DD
Approved to send by: <!-- release:bob@YYYY-MM-DD; release:carol@YYYY-MM-DD -->

## Context

<!-- Three sentences: what the project is, why these requests, and what is blocked until they are
granted. -->

## Requests

<!-- One row per request. Precise enough to act on without a meeting. -->

| # | Request | Exact detail (names, scopes, roles) | Why | Blocks backlog item | Reversible? |
|---|---|---|---|---|---|
| 1 | <!-- create a service identity --> | <!-- name, scope, permissions --> | | <!-- B-004 --> | |
| 2 | | | | | |

## What we will do with it

<!-- For each permission: what it is used for, who or what holds it, and when it can be removed. -->

## How to reply

<!-- Where to send answers and what to include (for example identifiers, not secrets). Never ask
for secrets by email or chat. -->

## Tracking

| # | Status | Date | Note |
|---|---|---|---|
| 1 | <!-- sent, granted, refused, partly granted --> | YYYY-MM-DD | |

A refusal stands. Record it, update the plan, and open a decision item if the plan needs a new
option.
