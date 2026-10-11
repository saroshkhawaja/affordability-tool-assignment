# Modeling

## Why clustering, and why K-Means

This project's core comparison (side-by-side GNI, price level, and
inflation for any two countries) doesn't need a model at all — it's just
a lookup. The modeling component was added on top of that, at the
instructor's request, to also group every country into an
**affordability tier** (Budget-Friendly / Mid-Range / Premium) a student
can scan without picking two specific countries first.

This is an **unsupervised** problem: there is no labeled "correct"
affordability tier for any country to train against, so a classification
or regression model doesn't apply. **K-Means** was chosen over other
clustering approaches (e.g. hierarchical clustering, DBSCAN) because:

- It's well suited to a small number of continuous, roughly comparable
  features (3, after scaling) and a dataset of this size (191 rows).
- It produces a fixed, easy-to-explain number of groups, which matches
  the "3 affordability tiers" framing the tool is built around.
- DBSCAN would have required picking a density threshold with no clear
  basis here, and would risk leaving outlier countries unclustered
  entirely rather than assigning them a tier (every country needs an
  answer for this tool to be useful).

## Features used

Three features, each standardized (`StandardScaler`, mean 0, std 1)
before clustering so that no single feature dominates purely because of
its raw numeric scale:

- `gni_per_capita_ppp` — purchasing power
- `price_level_ratio` — relative cost of living vs. the US
- `inflation_capped` — inflation, with extreme values capped at 40% (see
  CLEANING.md Entry 7) so a handful of hyperinflation countries don't
  dominate the distance calculation; the true, uncapped inflation value
  is kept separately for display and is not used by the model

`education_spend_pct_gdp` was deliberately **not** included as a
clustering feature — it has more missing data than the other three (see
CLEANING.md Entry 5), and it measures government investment in education
rather than a student's personal cost of living, so it doesn't belong in
an *affordability* grouping even where it is available.

## Choosing k (number of clusters)

The instructor's framing called for 3 tiers, but this was checked rather
than just assumed. Silhouette score (higher is better; measures how well
each point fits its own cluster vs. the next-nearest one) was computed
for k = 2 through 5 on the same standardized features:

| k | Silhouette score | Cluster sizes |
|---|---|---|
| 2 | 0.444 | 59 / 132 |
| **3** | **0.495** | **10 / 52 / 129** |
| 4 | 0.509 | 2 / 11 / 52 / 126 |
| 5 | 0.370 | 2 / 11 / 30 / 50 / 98 |

k=4 scores marginally higher than k=3 (0.509 vs 0.495), but it does so by
splitting off a 2-country cluster — not a meaningfully different fourth
tier, just an artifact of a couple of extreme outliers getting isolated.
k=3 was kept both because it matches the instructor's requested framing
and because its silhouette score is close to the best achievable without
producing a near-empty group.

## What the three clusters actually look like

Cluster means (unscaled) for k=3, from the actual run:

| Group | Mean GNI/capita (PPP) | Mean price level ratio | Mean inflation (capped) |
|---|---|---|---|
| Mid-Range (129 countries) | $15,990 | 0.41 | 4.17% |
| Premium (52 countries) | $71,151 | 0.73 | 2.24% |
| Budget-Friendly (10 countries) | $13,285 | 0.89 | 36.60% |

This is worth reading carefully: **"Budget-Friendly" does not have the
lowest average GNI or price level ratio** — Mid-Range does. What actually
separates Budget-Friendly as its own cluster is the capped inflation
feature (36.60% average, vs. ~2-4% for the other two groups) — i.e. this
group is really "countries whose defining feature is high-but-capped
inflation," not "countries that are cheapest to live in." This is an
important nuance the tool's labeling doesn't fully convey on its own —
see LIMITATIONS.md and EDA.md's confounder check for more on this.

## Evaluation

There's no ground-truth affordability label to score predictive accuracy
against, so evaluation here is diagnostic rather than a single accuracy
number:

- **Silhouette score** (above) — used to justify k=3 over alternatives.
- **Confounder check** (see EDA.md) — checked whether the grouping is
  really being driven by income/price level, or just by a few
  hyperinflation outliers. Conclusion: for the axes actually used to
  cluster, the grouping holds up; but the Budget-Friendly group's
  defining feature turned out to be inflation, not affordability, which
  is now stated plainly here and in LIMITATIONS.md rather than hidden
  behind the group's name.
- **Group size sanity check** — k=3 doesn't produce one giant group and
  two near-empty ones (the stated bare-minimum check in PROPOSAL_V2.md's
  Metric section).

## What was tried and rejected

- **Clustering on raw (uncapped) inflation** — rejected after it produced
  a "Budget-Friendly" cluster with 161.96% average true inflation,
  grouping active hyperinflation economies with what was supposed to be
  the cheapest, most attractive tier (see CLEANING.md Entry 7).
- **k=4 or k=5** — rejected per the silhouette/cluster-size analysis
  above; they split off outlier-sized clusters rather than adding a
  meaningfully distinct tier.
- **Including `education_spend_pct_gdp` as a clustering feature** —
  rejected due to missing data and because it measures something
  different from personal cost of living (see Features section above).
