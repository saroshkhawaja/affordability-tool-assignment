# Five Questions About the Data

### 1. What is a row?

A row is one country (or separately-reported territory), identified by
`country_code` (ISO3). Evidence: `clean_data.py`'s `pivot_to_country_rows`
step groups the long raw table by `["country_code", "country_name"]`, so
every distinct code becomes exactly one row in the output.
**Confidence: High** — directly verified by the printed `Final shape:
(191, 12)` matching one row per the 191 countries that passed the
completeness filter.

### 2. What is the outcome and its unit?

There are two outputs the tool reports, not one single "outcome":
(a) the three raw comparison indicators (GNI per capita PPP in
international dollars, price_level_ratio as a dimensionless ratio,
inflation_pct in % per year), and (b) the derived `affordability_group`
label (Budget-Friendly / Mid-Range / Premium), which is a K-Means cluster
assignment, not a measured quantity.
**Confidence: High** for (a) — these are standard WDI units, documented in
DATA_DICTIONARY.md. **Confidence: Medium** for (b) — cluster labels are a
modeling choice (3 clusters, specific features, specific random seed), so
a different choice could produce different group boundaries.

### 3. What is the timeframe?

Each indicator value is the most recent non-empty value per country
(`mrnev=1` in the API call), not a fixed calendar year. Evidence: `quoted
in fetch_data.py`: *"Fetch the most recent non-empty value per country...
for ALL countries."*
**Confidence: High** that this is what was requested from the API.
**Confidence: Low** on whether all countries' "most recent" values line up
to the same year — the API does not guarantee this, and the raw response
was not manually audited year-by-year for every one of the 191 countries.

### 4. Who is missing?

201 countries/territories were returned by the API; 191 remain after
dropping rows missing an essential indicator. The 10 dropped were missing
inflation data (e.g. Andorra, Bermuda, Faroe Islands, Greenland, Eritrea,
Kosovo, Marshall Islands, Montenegro, Puerto Rico US, Turkmenistan,
Turks and Caicos — exact list in `data/raw/wdi_fetched_countries.csv` minus
`data/processed/countries_clean.csv`). Smaller island nations and
territories are disproportionately represented among the missing.
**Confidence: High** — directly computable by diffing the two files.

### 5. What is the sampling frame?

The sampling frame is "every country/territory the World Bank's `/v2/
country/all/indicator/...` endpoint returns a value for," which is itself
the set of WDI-reporting economies — not literally every country in the
world (e.g. some very small or non-self-governing territories are absent
from WDI entirely, before any cleaning even happens).
**Confidence: Medium** — this is true by construction of the API call, but
no independent check was done against a canonical "list of all UN member
states" to see exactly which non-WDI-reporting places are absent from the
very first raw pull (as opposed to the 10 dropped later during cleaning).
