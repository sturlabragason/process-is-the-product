# Deck notes

Running notes for the slide deck, so the thread survives across sessions. Newest decisions win.

## Goal

A talk that presents this repo's method ("the process is the product"). It works as a live talk and
as something people can read on their own afterwards.

- Audience: mixed conference audience.
- Length: 20 to 30 minutes, about 25 slides (the mockup has 28).
- Delivery: live with speaker notes, and self-paced from a URL or PDF. PowerPoint is not needed.

## Sources and ownership

- Material: `docs/`, `templates/`, `agent/`, `tools/`. Another agent is still writing these. The deck
  only reads them and never edits them.
- Brand: `../claude-for-small-business/business/brand/` (`README.md` and `tokens.css`, the Sturla
  Bragason identity). Another agent is updating it. The deck uses it as it is and does not fork it.
- Deck work lives only in `deck/`.

## Format and tools

- Slidev (Markdown slides, presenter mode, PDF export). Reveal.js is the fallback.
- Motion through the HyperFrames skills, kept light. The user said "don't overdo it".
- Brand limits: black and white, IBM Plex Mono and Sans, 3 px and 5 px rules, square corners. No
  gradients, glow, shadows or imagery. Signal red only for blocked or failed.

## Decisions so far

1. Slide 1 is the talk summary: one line per part on screen, the full text in the notes.
2. (Superseded by draft 6: no case study.) The case study is the example of the method working. The conditions were hard: a handover
   archive, busy approvers, one shared checkout used by three AI tools, five and a half weeks.
   Everything in scope was done with evidence. The open half of the backlog was the planned
   roadmap, not unfinished work.
3. There is no "limits" slide.
4. Commit and worktree counts are side detail. They stay off the slides.
5. The user likes the statement layout: one large plain sentence on a mostly empty slide (mockup
   slide 02).

## Feedback on mockup v1 (2026-10-31)

- The general format and the black and white look are good.
- The wording reads as AI. The titles are slogans ("Three things stay expensive", "Loop,
  harness, factory"). Every slide's text goes through the humanizer skill.
- From the frames alone it is not clear what would be said. Each slide needs its actual sentence
  and the fact behind it, not a topic label and grey placeholder bars.
- Add some motion, but keep it light.

## How to present the facts

- Tell the case as a story by day number, where each stage arrived after a specific failure (day 1
  gap analysis, days 5 to 8 collisions in the shared checkout, day 10 false "done" rows, day 19
  the audit of the method itself). The method is explained inside that story and not as a
  separate catalogue of stages.
- Each slide shows one plain sentence that the presenter would say out loud, plus at most one
  supporting fact taken from the docs.
- Write the way a person talks: no slogans, no aphorisms, no runs of three, no punchline after
  every line, no em or en dashes.
- Put specifics (day numbers, the five rules that came from incidents) ahead of abstractions.

## Open

- Talk title, venue and date.
- `docs/08-case-study.md` "The project" still lists commit and worktree counts. That is the other
  agent's file, so this is a note for them.

## Draft 2 of the mockup (2026-10-31)

- `mockup/skeletons.src.html` holds the storyline: the text on each slide, the fact behind it, the
  speaker note and the source section. `python3 mockup/build.py` writes `mockup/skeletons.html`
  with the brand files copied in. The browser is a Flatpak and cannot follow relative paths out
  of the file's folder.
- 27 slides: summary, why (3), the project told by day number (10), the method (7), starting (4),
  close (2).
- Every statement on a slide was checked against the docs, and invented claims were removed from
  the speaker notes. The risk tier slide carries an "untested proposal" tag, as the docs do.
- Motion is one small move per slide: a text wipe, boxes snapping in, rules drawing, gates filling,
  or "done" flipping to "not done" in signal red on day 10. There is no bounce. It respects
  reduced motion and replays on click. Add `?static` to the URL to see every slide's end state.

## Feedback on draft 2 (2026-10-31)

- The summary slide used a label and a short fragment per row ("The method: ten stages, each added
  after a failure"). That is the inline-header list pattern, and you can spot it as AI writing straight away. The summary slide
  is now three short paragraphs of full sentences, as first agreed.
- "Checking did not get cheaper" was wrong. In this method agents do review, and a script checks
  status. What stays with a person is deciding what done means and building the checks. Slide 2
  now says that.
- "Each stage added after a failure" was not true. Stage 0 was not a separate step in the case.
  Slide 15 now says nine of the ten came in because a problem made them necessary.
- Rule for all slide text: full sentences with a subject. No label and fragment rows, and no short
  punchline captions.

## Draft 3 (2026-10-31): short lines, mixed layouts

- Text on slides got worse with each draft and turned into walls of text. Slides now carry one short line, as
  "Producing work is cheap now" did in the first skeleton. The fact behind the line and the
  speaker note sit under the frame, not on the slide.
- The first skeleton's minimalist diagram slides are back between the statements: three
  boxes, loop to harness to factory, in scope against roadmap, two kinds of evidence, and old
  practice against the agent form. Not every slide is a statement.
- The opening slide is the title and one line. The spoken summary lives in the speaker note.
- 32 slides. Trim during rehearsal if the talk runs over 30 minutes.
- Frame the middle part as a case study I walk through, not as "one project". Part name: "The case
  study".
- The case study opens with what was handed over and what had to be delivered, not with "the
  conditions were hard" or "busy approvers". The difficulties come out in the day slides.

## Draft 4 (2026-10-31): brand v1.1 "Untangle"

- The mockup now follows the brand's slide templates (`applications/slide-title.html` and
  `slide-content.html`): IBM Plex Sans Light headlines, a hairline frame, and a footer with the
  icon, my name and the page number.
- The title slide has the lockup and the title motif. The first slide of each part has the band
  motif, and the closing slide has the close band. The motifs come from the brand's
  `build_motif.py` presets. Nobody draws them by hand.
- The motif lines draw in when a slide appears. That is the only new motion.
- Lane blue appears at most once per slide: the "in scope" box, "+ 2nd human" and the "done" status.
  Signal red is still only for "not done" and the sessions that overwrote each other.
- `build.py` inlines the fonts, logos and motifs, so the HTML still opens from the Flatpak portal.
- The title slide has no venue, date or contact line. There is no fixed venue.

## Polish decisions (2026-10-31, after draft 4)

- The case study read as cheesy and some slides repeat each other or have no visual.
- Case study: show real artifacts from the repo (template, status table, check output), not a week
  count. Do not mention weeks.
- Case study headlines: the problem, then the fix, as two short lines.
- Merge the overlapping groups: the problem part, the evidence slides and the starting slides.
- Visuals: minimalist diagrams on most slides, a stage strip (0 to 9) that recurs and fills in, and
  more motion on the diagrams, with nothing bouncy.
- Quote slides stay, each with a visual.
- Target about 25 slides.

## Draft 5 (2026-10-31): artifacts, stage strip, merges

- 25 slides. The problem part is three slides: cheap work against the three expensive things, the
  DORA amplifier quote with bars, and judgment at the gates drawn as a factory of harnessed loops.
- Case study slides show the problem, then the fix, then an artifact: the situation file, the
  context file invariants, the request pack, a before and after diagram of worktrees, the three
  procedure phases, real output from `tools/verify_status.py`, and the audit checklist. Captions
  say when an artifact is the repo's template rather than a file from the case.
- A stage strip in the corner fills in as each stage appears. Stage 0 is dashed, because it was
  never its own step in the case.
- Merged: "ten stages" with "skip the stages you don't need yet", "done needs evidence" with
  "merged is not done", "should work" with the two kinds of evidence, and the three starting
  slides into "write one sentence" and the maturity levels. The office move moved to a note.
- Kent Beck's quote is quoted exactly. The slide shows what changed (who types) and what did not.

## Draft 6 (2026-10-31): no case study

- Decision: the deck does not present the case study. That project is where I bootstrapped the
  method, not a good example of applying it. This replaces decision 2 above and the case-framing
  entries in drafts 3 to 5.
- One line says where it came from: the stages part opens with "Bootstrapped on one real
  project" over the stage grid. Nothing else from the case: no days, no outcome slide, no role
  counts.
- The case part is now "The stages". Each slide takes the stage's general trigger from
  `docs/03-method.md` as the headline, the fix under it, and the template artifact on the
  right. Stages shown: 0 (tagged untested proposal), 1, 2, 4, 6, 7, 8, 9. Stage 3 is covered by
  the review slide, stage 5 by the status slides.
- The stage strip now marks the current stage in blue and earlier stages in ink.
- "Five rules" stays, captioned as learned while bootstrapping the method.
- The opening summary no longer promises a case study walk-through.
- 24 slides.
- Slide 2: the cheap box says "making code". "Still expensive" is one frame around the three
  boxes. "Knowing the state" is now just "Knowing the context" (it covers current state,
  boundaries and what must not break, said aloud). This widens doc 09 to cover stages 0 to 2.
- Slide 4: redrawn as one work item through review, build and release, with the plan, change
  and release gates between, each approved by a person before the action (doc 05).
- Stages opener: was "Skip the stages you don't need yet" over a bare grid, which did not explain
  the stages. Now "The method is ten stages": ten cards with number, name, purpose in a few words
  and the output (from doc 03), plus one grey line "Written down after bootstrapping them on one
  real project." The skip rule moved to the maturity slide, which now shows which stages each
  level adds.
- Stage 0 reframed: "Agents get access nobody would give a person" / "Give them the same rules
  as people". Most of it is existing practice (no secrets in code, least privilege, data
  classification, no production access by default). Only the approved tool list and the budget
  owner are new. Stage 0 is not Anthropic guidance; doc 03 sources it to DORA and marks it an
  untested proposal. A note for the docs agent asks for doc 03 to say the same.
- Ten-stage slide simplified to number, name and output per stage. The purposes are spoken.

## Draft 7: the talk as one blog post

- The skeleton is now one page, `deck/post/index.html`, built by `deck/post/build.py` from `post.src.html` and `prose/*.md`. It has an index at the top, then each slide followed by its context and source. Every slide must work without the prose.
- Prose: one `## <slide id>` section per slide in `prose/1-opening.md`, `2-stages.md` and `3-method.md`. These are facts from the docs only, and they pass style-lint.
- Kickers are removed (brand v1.1). The quotes carry a `by:` attribution, and the stage strip carries the stage name.
- Content slides have no bands; the band ran into the kaizen staircase. Only the title and end slides keep the motif.
- "Learned the hard way" became "Five rules from incidents".
- Slide 20 became "Start from a failure you can name". It uses the quick start's example trigger and points to the stage it calls for, replacing the blank form.

## Draft 8: plain prose, readable layout, publishing

- Humanizer pass over all three prose files. "Trigger" now reads "you need stage N when", and each method term is explained the first time a section uses it.
- The source line became "More in the guide": doc titles linked to GitHub, set in a left rail on a 5:7 split with the prose on the right.
- Slide captions, strip and footer text are larger, and the index part headings are ink rather than blue (one blue element per view).
- Deep links such as `#s8` scroll to the slide after the page renders.
- To publish, the repo goes public as sturlabragason/process-is-the-product with GitHub Pages turned on, and the main site links to it.
- On phones the slides shrink to thumbnails, and the prose carries the content.
