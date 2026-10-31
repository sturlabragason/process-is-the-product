# Source verification

How the quotes in this guidebook were checked, and what was corrected or left out.

## Method

1. A first research pass collected candidate quotes and URLs for each claim in the method.
2. A second, independent pass (an Opus-class model, not the one that collected them) fetched
   each source and compared every quoted sentence word for word with the live page. It reported
   pass, corrected, or excluded for each quote.
3. Only quotes that passed, or passed after correction, are used. Each is cited by key in
   [the references](../docs/11-references.md).

The checks were run in late 2026. Web pages change; recheck any quote before publishing it.

## Results

- 14 of 15 quotes in the software engineering practice section passed, some after correction.
- Corrections were wording only: punctuation, a missing word, or a phrase that the page words
  slightly differently. The corrected wording is the one used.
- Fowler's continuous integration article (revised January 2024) uses a spaced hyphen where an
  earlier draft had an em dash; the quote follows the page.

## Excluded

- A small-batch line attributed to the SRE book and to *Accelerate*: the exact wording could not
  be found in either source.
- The phrase "self-testing build" attributed to Fowler: not found in the cited article in that
  form.

## Kept although it cuts against the method

- Böckeler's 2026 experiment on test-driven development in the agent loop found "no clearly
  discernable difference" from telling agents to follow TDD. It is cited where the method relies
  on tests as sensors.
- The trunk-based development site added its wording about agents only in October 2026. It is
  cited for the long-standing short-lived branch guidance, not as early evidence for agents.
