# Reviewer brief

<!--
What an independent reviewer gets for one work item. The reviewer can be an agent with its own
context and read-only access, or a person. It gets the change and the acceptance criteria and
NEVER the author's reasoning, chat history or self-assessment: a reviewer who reads the author's
argument tends to agree with it. Rules: see the guidebook, docs/05-work-item-procedure.md (not copied into the project).
Fill in the brackets, send the brief, attach the output to the item.
-->

## Brief (sent to the reviewer)

Item: <!-- B-001, title -->
Risk tier: <!-- local, shared, irreversible -->
Your access: read-only. Do not change anything.

### The change

<!-- One of: a diff, a commit range, a pull request link, a plan of changes. Nothing else. -->

### Acceptance criteria

<!-- Copied word for word from the backlog row. -->

### Scope

<!-- The files, resources or settings the item may change, from the row. Anything outside this is a
finding. -->

### What to check

1. Does the change meet each acceptance criterion? Run the check where you can.
2. Do tests exist for the new behaviour, and would they fail without the change?
3. Does the change touch anything outside the scope?
4. Is any irreversible action hidden in it (deploy, apply, delete, merge to a shared branch,
   external message, spend, permission or secret change, instruction file edit, production data
   read)?
5. Is any claimed evidence a system's own report of success rather than an independent check?
6. Secrets or production personal data in the change or its logs?

### Not included on purpose

The author's reasoning, chat history and opinion of the change.

## Output format (returned by the reviewer)

```
Item: B-001
Reviewer: <!-- name or agent role -->
Date: YYYY-MM-DD
Verdict: approve | changes needed | cannot judge

Criteria:
- <criterion 1>: met | not met | not checkable, <evidence: command and result, or file:line>
- <criterion 2>: ...

Findings (most severe first):
- [high|medium|low] <file:line or resource>: <problem>, <why it matters>

Out of scope changes: none | <list>
Checks run: <commands and exit codes>
```

A verdict of "approve" from a reviewer is input to the change gate, not the gate itself. The gate
owner decides.
