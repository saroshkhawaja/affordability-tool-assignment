# AI Use Disclosure Log

Per the assignment's AI-use policy, this log discloses every way AI
(Claude) was used on this project, and confirms what was deliberately kept
human-written.

## What AI (Claude) was used for (Allowed uses)

- **Code scaffolding and debugging**, including diagnosing and fixing real
  errors encountered while running the pipeline: a Stata `reshape` error
  ("no xij variables found"), a `ReadTimeout` when fetching all countries
  at once (fixed with `mrnev=1`), an archived WDI indicator
  (`PA.NUS.PPPC.RF`) discovered via a direct API error response, and a
  deprecated REST Countries API (confirmed via its own deprecation
  response) that was removed from the pipeline entirely.
- **Explaining concepts** on request (e.g. what PM2.5 is, what precision
  and recall mean, what a price-level ratio represents).
- **Drafting document structure/templates** (this log, the data
  dictionary table layout, the cleaning-log format) which were then filled
  with the project's own, verified facts and figures.
- **Reviewing a real clustering result** (the mislabeled "Budget-Friendly"
  cluster with 161.96% average inflation) and proposing the inflation-cap
  fix, which was then run and verified by the student.
- **Building the live comparison tool** (published interactive page) from
  real, API-sourced data.

## What AI was explicitly NOT used for (Not Allowed, per policy)

- The Engagement Journal's "Before I looked," "what surprised me," and
  confidence self-assessments are the student's own first-hand account,
  not AI-generated.
- Cleaning rules were not decided by AI unilaterally — each rule in
  CLEANING.md reflects a real issue the student encountered and confirmed
  by running the scripts themselves; the student reviewed and approved the
  reasoning before it was written down.
- No unverified AI-supplied facts were inserted — every number in
  CLEANING.md, DATA_DICTIONARY.md, and FIVE_QUESTIONS.md comes from the
  real, printed output of the student's own pipeline runs, not from AI
  recall or estimation.
- No code was included that the student cannot explain; every script is
  commented to explain what each step does and why.

## Tools used

- Claude (Anthropic), via chat, for the uses listed above.

## Verification

All data figures and script outputs quoted throughout this repo were
produced by the student running `fetch_data.py` and `clean_data.py`
themselves and pasting back the real console output, which is reproduced
verbatim in CLEANING.md.
