## stages
The method has ten stages. Stage 0 decides what agents may use and touch. Stage 1 finds out what is true. Stage 2 gives every session the same start. Stage 3 gives each area one writer, whose work someone else approves. Stage 4 orders the plan so slow requests leave first. Stage 5 turns the plan into small items, each with a check. Stage 6 gives each item its own workspace. Stage 7 makes every item follow the same steps and approvals. Stage 8 makes status match reality. Stage 9 keeps the instructions true as the project changes.

Each stage has a purpose and an output, usually one file. I also name the problem that shows you need it and the early sign of it. The guide calls these the trigger and the anticipated trigger. Add a stage only when you hit or foresee that problem. A small project may need only stages 0 to 2. I wrote them down after they were bootstrapped on one real project, where I found them. The full reference is [the method](../../docs/03-method.md).

Stages 3 and 5 have no slide. Roles come back on the review slide, the backlog on the status slides.

## s0
Picture an agent holding a production credential "just for this one task". You would not give a new colleague that access. Stage 0 holds agents to the same rules as people. You need it when an agent reaches production, data is pasted into an unapproved tool, or an unexpected bill arrives. You can see it coming on any project where agents will read code, data or tickets, so in practice you start it on the first day.

Most of this stage is practice you already have: no secrets in the repository, data classification, and least privilege per identity. Agents get no production access by default, and a human starts every irreversible action. If your identity, access and secret handling are sound, the stage is short. Under zero trust, an agent is one more identity with the least access it needs.

Two parts are new: which AI tools are approved, and who owns the budget for tokens and agent compute, with a limit where work stops. The output is [`docs/ai-stance.md`](../../templates/docs/ai-stance.md), linked from the context file agents read first. DORA lists a "clear and communicated AI stance" as one of its seven AI capabilities. The whole stage is an untested proposal.

## s1
Plans fail quietly when they rest on facts nobody checked. You need stage 1 when the information you start from is scattered, contradictory or of unknown quality. You can see that coming on the first day of any project, or the day you inherit one.

The output is [`docs/situation.md`](../../templates/docs/situation.md). It lists every input you were given or found, rates each one confirmed, unconfirmed or wrong, and records who checked it. On existing work you then write a gap analysis with three columns: the current state with evidence for it, the target state, and the gap between them. Separate columns stop a legacy workaround being written up as the target. New work has no current state, so you keep an assumption register instead. Each row is a belief the plan depends on, with an owner and a test that would prove it wrong. A dated decision log sits underneath.

One wrong input found at the start changes the plan cheaply. Found later, it costs a rewrite. Have the agent interview you until it "could write the spec", and don't let it fill gaps with plausible guesses. The established practices are gap analysis, assumption mapping, the pre-mortem and the decision log.

## s2
Every new agent session starts from zero. You explain the layout and rules again, and soon two sets of instructions contradict each other. Then you need stage 2. You can see it coming as soon as a second session, agent, tool or person joins.

The output is one context file, [`AGENTS.md`](../../templates/AGENTS.md), that every agent loads first. It holds the repository layout, links to the other stage outputs, and a few short, checkable rules that are never negotiated. In the template, the first is "Done means verified by a command or a linked record". Others forbid secrets in the repository and production personal data in agent context, and require recorded human approval before any irreversible action. If you use several AI tools, link the same file under the name each one reads, so there is one copy.

Treat the file as code. It has an owner, it lives in version control, and changes go through review. Personal instruction files can change tone or habits, never those rules. To test it, give a fresh agent only the file and ask for the next work item. The practice behind it is the project charter, the contributing guide and architecture decision records.

## s4
External approvals, access and procurement take weeks. Wait until the build needs them, and they block you late. You need stage 4 when work starts before its dependencies are ready. You can see it coming when anything has a lead time over a week. Then start this stage on day 1, even if the rest of the plan waits.

The output is [`docs/plan.md`](../../templates/docs/plan.md). It has phases, each with entry criteria, an owner and exit criteria, so nothing starts before its dependencies are done. The first phase is a walking skeleton, a bare version of the system in a real environment, so later work can be verified there. Every request to someone outside your control goes into a [request pack](../../templates/request-pack.md), one per external party, with a reply-by date and the backlog item each request blocks. The requests with the longest wait go first. Sending a pack can't be undone, so two people approve it first. If a request is refused, the refusal stands and the plan changes.

A gate is a decision point between phases, made against stated criteria. Cooper calls gates "tough decision meetings". The established practice is the work breakdown structure, the critical path and stage-gate.

## s6
Run two agent sessions in one checkout and they will switch branches under each other and overwrite each other's work. You need stage 6 when parallel work collides, or when changes from one task leak into another.

The fix is one workspace per item, with one owner. For code that means a git worktree, a separate working folder on its own short-lived branch, named after the item ID. When an item moves to `in-progress`, you create a new worktree for it. Only its owner writes there, and you remove it after the merge. Never reuse a worktree for a second item. The established guidance on branches is that "the branch should only last a couple of days".

The fix is cheap, so you don't wait for the first collision. You can see it coming the moment a second item, agent or session runs at the same time as the first, and that is when you add the stage. It is done when nobody edits a shared workspace or someone else's. Your team probably knows the practice already: short-lived feature branches, trunk-based development, ephemeral environments, and the permit to work. See [stage 6](../../docs/03-method.md#stage-6-work-isolation) for the steps.

## s7
After a few items you notice each one repeats the same small decisions, and the same mistake has happened twice. Then you need stage 7. You can see it coming when items you ran by hand keep coming out the same.

So run items by hand first, noting every decision and check. Then write the cleanest end-to-end run down as the procedure. Ohno put it as "There can be no kaizen without a standard", and you can't write a good one before doing the work. The output is a skill, `.agents/skills/work-item/SKILL.md`, an instruction file used only on request. The stage is done when "Do item N" is enough for a new agent to take an item from review to verified done.

The [procedure](../../docs/05-work-item-procedure.md#the-three-phases) has three phases. Each ends at a gate, an approval point. Review is read-only and ends at the plan gate. Build runs in the item's own working folder and ends at the change gate, before the merge. A human starts release, which ends at the release gate. Every gate comes before the action it approves. After each incident you add a rule. The practice behind it is standard work, checklists and PDSA (plan, do, study, act).

## s8
An item gets marked done when it isn't. It was merged but never deployed, or "verified" by a pipeline run that was cancelled. Then you need stage 8. You can see it coming when others start relying on your status, or an agent updates status on its own.

The status values are fixed: `proposed`, `ready`, `in-progress`, `in-review`, `merged`, `done`, `blocked`, `dropped`. `merged` means merged but not yet verified in the target environment. `done` needs evidence from that environment that you can check. A system reporting its own success is not evidence. A green badge, an agent's summary and a status field are all claims.

The output is [`tools/verify_status.py`](../../tools/verify_status.py). It reads the backlog table, checks every status against its evidence and approvals, and exits with code 1 if anything fails. The terminal on the slide is real output from the script. I ran it on a copy of the [backlog template](../../templates/docs/backlog.md) with one `merged` row changed to `done`. It reported "done without evidence" and exited 1. Run it in your CI pipeline and before publishing any status change. When it fails, fix the item, not the script. This is a Definition of Done, the agreed meaning of done, enforced by automation.

## s9
The context file every agent reads first, the roles and the procedures describe the project as it was when someone wrote them. Then the project changes. Agents follow stale instructions just as faithfully as current ones, so an instruction that points at a deleted component does real harm. That is when you need stage 9. You can see it coming when a phase ends, a system is replaced, or a fixed interval passes. Put the next audit date in the plan.

The audit uses an [audit checklist](../../templates/audit-checklist.md) with 15 checks, among them stale paths, stale components, contradictions, duplicates and unused rules. A finding is high severity if an agent following the instruction would do harm or report false status. Each finding gets a date and is filed as an `ops` item. The stage is done when an audit finds no high-severity stale instructions.

Two habits keep the audit honest. Someone other than the main author runs it, or a read-only reviewer agent does. And the audit prefers removing a rule to adding one. This is the retrospective and the act step of PDSA (plan, do, study, act), applied to the instructions themselves, with document control and docs as code.

## rules
Each of these five rules came from something that went wrong while I was bootstrapping the method. They are short, and they are now part of the [work item procedure](../../docs/05-work-item-procedure.md#rules-from-incidents).

Measure a baseline before you change anything. A system reporting its own success is not evidence, so a green pipeline or an agent's summary still needs a check against the live system. Before release, count the expected changes again instead of trusting an estimate, and compare them with the plan item by item. Write the done entry, with its evidence, before the item is closed, because otherwise it can get lost. And if a human refuses a permission, the answer stands. The agent records the refusal and the plan changes around it.

Stage 7, which sets the steps every item follows, adds two more rules that grew the same way. Humans start irreversible actions. Reviewers get the acceptance criteria, never the author's reasoning.
