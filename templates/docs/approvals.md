# Approval log

<!--
Copy to docs/approvals.md. One line per approval, appended, never edited. A correction is a new
line that refers to the old one. The backlog Approvals cell (gate:who@YYYY-MM-DD) is the index;
this log is the record.
Rules: docs/05-work-item-procedure.md in the guidebook, sections "Approval record format" and
"Gate owners".

Fields:
gate: plan, change, release, launch-readiness, expedite or evidence.
item: the backlog ID.
who: a named human and their role. Never an agent, never "the team".
when: date and time with time zone, ISO 8601, before the action it approves (expedite: as it
  happens).
what exactly was approved: the action, target and version, as precise as the request. An
  approval covers exactly this and nothing else; a later commit or a different count needs a
  new approval.
link: where the decision is recorded and cannot be edited (pull request approval, signed
  comment, ticket).

Where the hosting tool already keeps the record (for example a pull request approval for the
change gate), the line here can be short, but the link is required.
Delete these comments and the example lines when you start.
-->

```
gate | item | who | when | what exactly was approved | link
plan | B-001 | carol, tech lead | 2026-10-02T09:40+02:00 | plan in B-001: pipeline in .ci/pipeline.yml, deploy to dev only, 2 new resources, 0 deletions | https://git.example.com/project/issues/12#note-3
change | B-001 | bob, code owner | 2026-10-03T16:05+02:00 | commit 3f2c1a9 and pull request 42 description, merge to main | https://git.example.com/project/pulls/42#review-7
```
