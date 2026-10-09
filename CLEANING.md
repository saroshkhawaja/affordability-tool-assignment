# Cleaning Log

This log describes every change made between the raw, as-fetched data
(`data/raw/`) and the final cleaned file (`data/processed/countries_clean.csv`),
in the order the cleaning script (`clean_data.py`) applies them. Each entry
says what was found, what was done about it, and why — including entries
where a decision was made to leave something unchanged.

## Entry 1 — Long-to-wide pivot (no values changed)

**Found:** The raw table from `fetch_data.py` is long: one row per
country-per-indicator (1160 raw rows across 5 indicators, before removing
aggregates).
**Action:** Pivoted so each row is one country and each column is one
indicator (`pivot_to_country_rows`), using `aggfunc="first"` since each
country has at most one most-recent-non-empty value per indicator.
**Why:** A usable comparison/clustering dataset needs one row per country.

## Entry 2 — Removing World Bank aggregate codes

**Found:** The World Bank API's "all countries" endpoint also returns
regional and income-group aggregates (e.g. `WLD` = World, `HIC` = High
income, `LMY` = Low & middle income) mixed in with real countries — 43
such codes.
**Action:** Filtered these out by ISO3 code before any further cleaning.
**Why:** These are not countries; including them would let a region's
summary value be compared against or clustered with real countries, which
is meaningless.

## Entry 3 — Recomputing price_level_ratio (archived indicator)

**Found:** The indicator originally chosen for a precomputed price-level
ratio, `PA.NUS.PPPC.RF`, returned a direct API error: *"The indicator was
not found. It may have been deleted or archived."*
**Action:** Recomputed `price_level_ratio` manually as
`ppp_conversion_factor / official_exchange_rate` using two indicators
(`PA.NUS.PPP`, `PA.NUS.FCRF`) that are still live.
**Why:** This ratio is the standard way to express how expensive a
country's price level is relative to the US dollar once exchange rates are
accounted for, and it was reconstructable from still-available data rather
than needing a new indicator choice.

## Entry 4 — Dropping countries missing an essential indicator

**Found:** After the pivot, some countries were missing `gni_per_capita_ppp`,
`price_level_ratio`, or `inflation_pct` entirely (small territories/states
not covered by all WDI series, e.g. Faroe Islands and Greenland have no
inflation figure; Andorra and Bermuda have no inflation figure either).
**Action:** Dropped any country missing one of these three *essential*
indicators. 26 rows dropped; 191 countries remaining.
**Why:** These three indicators are used directly in both the comparison
table and the clustering model — a country missing one can't be placed
meaningfully.

## Entry 5 — Chose NOT to drop countries missing education_spend_pct_gdp

**Found:** `education_spend_pct_gdp` has more missing values than the three
essential indicators (several small island nations and a few larger
countries don't report it).
**Decision:** Left these rows in, and the tool displays "not reported"
instead of a number.
**Why:** Education spend is a secondary/contextual field, not used in the
core affordability score or in clustering — dropping a country over a
field it isn't scored on would throw away otherwise-usable comparison data.

## Entry 6 — Chose NOT to remove extreme inflation values

**Found:** A few countries have extreme inflation (Venezuela ~255%,
Zimbabwe ~105%, Sudan ~139%, Argentina ~220%).
**Decision:** Did not drop or treat these as data errors — the raw
`inflation_pct` value shown to users is the true, uncapped figure.
**Why:** These are real, documented hyperinflation episodes, not
measurement errors, and a student comparing affordability should see the
true number. (See Entry 7 for how this is handled specifically inside the
clustering step, which is a separate concern from display/cleaning.)

## Entry 7 — Capping inflation for clustering input only

**Found:** Running K-Means directly on raw `inflation_pct` produced a
"Budget-Friendly" cluster whose *average* inflation was 161.96% — i.e. the
hyperinflation outliers were dominating the distance calculation so badly
that unstable, crisis economies were being grouped with (and labeled as)
the cheapest, most attractive group.
**Action:** Added `inflation_capped = inflation_pct.clip(upper=40)` as the
feature actually fed into K-Means, kept the true `inflation_pct` for
display, and added a boolean `economic_instability_flag` (true when
inflation > 40%) so the distinction isn't hidden.
**Why:** The cap prevents a handful of outliers from distorting the
distance-based clustering, while the flag and the untouched display value
mean no information is lost or hidden from the end user — just kept out of
the math that decides group membership.

## Entry 8 — Data Quality Verification
Data quality was checked for the final data set and showed that there were no duplicate country_code values, just 191. All three essential indicators had no missing values, and only two (education_spend_pct_gdp) were found to have missing values. Data types were also checked: numeric indicators stored as float64, the cluster ID as int64, the instability flag as bool, country identifiers and group labels as strings. No extra lines were deleted in this verification, which shows that the set contains 191 items.

## Entry 9 - Year Consistency Check
191 countries were checked and 168 of them had the same reporting year on the indicators, and 23 countries (around 12%) had different reporting years. There were no changes to data at this check, only to help identify differences in reporting years. Such mismatches could impact the reliability of price_level_ratio comparisons as indicators reported for different years may not accurately reflect the same economic conditions.

## Verified pipeline run

Running `fetch_data.py` then `clean_data.py` end-to-end on the author's
machine produced:
```
Raw rows loaded: 1160
Removed 43 aggregate/region rows (e.g. World, High income).
Dropped 26 rows missing an essential indicator (gni_per_capita_ppp, price_level_ratio, or inflation_pct). Remaining: 191 countries.

Affordability group sizes:
affordability_group
Mid-Range          129
Premium             52
Budget-Friendly     10
Name: count, dtype: int64

Saved cleaned, clustered data -> data/processed\countries_clean.csv
Final shape: (191, 12)
```
This is the real, unedited console output from the run, confirming the
pipeline is reproducible top-to-bottom from raw to cleaned.
