# Data Dictionary

File: `data/processed/countries_clean.csv` (191 rows, one per country)

| Column | Type | Unit | Definition | Source | Caveats |
|---|---|---|---|---|---|
| `country_code` | string | ISO3 code | Country identifier, e.g. `PAK` | World Bank WDI API | World Bank country codes should not automatically be assumed to be valid ISO3 codes. Some territories may use different identifiers, so the codes should be checked against an authoritative reference before using them for matching or merging datasets. |
| `country_name` | string | — | Country name as returned by the World Bank | World Bank WDI API | A few names differ from common usage (e.g. "Egypt, Arab Rep.", "Korea, Rep.") |
| `gni_per_capita_ppp` | float | current international $ | Gross National Income per capita, PPP-adjusted (indicator `NY.GNP.PCAP.PP.CD`) — most recent non-empty value per country | World Bank WDI API | Most-recent-non-empty (`mrnev=1`) means different countries' values may come from different years |
| `ppp_conversion_factor` | float | local currency units per international $ | PPP conversion factor (indicator `PA.NUS.PPP`) | World Bank WDI API | Intermediate value, used only to compute `price_level_ratio` |
| `official_exchange_rate` | float | local currency units per US$ | Official exchange rate (indicator `PA.NUS.FCRF`) | World Bank WDI API | Intermediate value, used only to compute `price_level_ratio` |
| `price_level_ratio` | float | ratio (dimensionless) | `ppp_conversion_factor / official_exchange_rate` | Derived (see CLEANING.md Entry 3) | Original precomputed WDI indicator for this (`PA.NUS.PPPC.RF`) was archived/deleted mid-project; this is a manual reconstruction. The PPP conversion factor and exchange-rate reporting years do not match for 23 out of 191 countries. This mismatch may make the calculated price_level_ratio less reliable and could affect affordability comparisons. The interpretation of values above 1 still needs to be verified against World Bank metadata and should not yet be treated as a confirmed fact. |
| `inflation_pct` | float | % per year | Consumer price inflation, annual % (indicator `FP.CPI.TOTL.ZG`), most recent non-empty value | World Bank WDI API | A few countries show extreme values (hyperinflation episodes) — true values, not errors; see CLEANING.md Entry 6 |
| `education_spend_pct_gdp` | float | % of GDP | Government expenditure on education (indicator `SE.XPD.TOTL.GD.ZS`) | World Bank WDI API | This variable has missing values for 2 out of 191 countries. Therefore, the missing-data issue is limited to these two records rather than several countries. |
| `inflation_capped` | float | % per year | `inflation_pct` clipped at 40, used only as a K-Means feature | Derived (see CLEANING.md Entry 7) | Not the true inflation value — do not use for display/reporting |
| `economic_instability_flag` | boolean | — | True when true `inflation_pct` > 40% | Derived | Flags countries where the clustering feature was capped |
| `cluster` | int (0-2) | — | Raw K-Means cluster label | Derived (model output) | Arbitrary numeric label; `affordability_group` is the human-readable version |
| `affordability_group` | string | — | `Budget-Friendly`, `Mid-Range`, or `Premium` — cluster labels reordered by each cluster's mean `gni_per_capita_ppp` | Derived (model output) | A clustering result, not an official classification; see LIMITATIONS.md |

**Row definition:** one row = one country (or territory reported separately
by the World Bank, e.g. Hong Kong SAR China).

**Granularity:** country-level, single most-recent-available snapshot per
indicator (not a time series/panel in this version).
