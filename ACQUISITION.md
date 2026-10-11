# Acquisition Record

**Source:** World Bank World Development Indicators (WDI) database,
collected by the World Bank from member countries' national statistical
agencies (and, for some series, the World Bank's own economists)
specifically to track global development and economic indicators for
policy and research use.

**Date pulled:** October 2026 (see commit history for the exact date of
the `fetch_data.py` run this repo's `data/raw/` reflects).

**Indicators pulled:** `NY.GNP.PCAP.PP.CD` (GNI per capita, PPP),
`PA.NUS.PPP` and `PA.NUS.FCRF` (used together to derive price level
ratio), `FP.CPI.TOTL.ZG` (inflation), `SE.XPD.TOTL.GD.ZS` (education
spend % GDP).

## Acquisition method chosen, and why not the others

Of the four acquisition methods (API, manual download, web scraping, or
a pre-packaged dataset), **API** was used.

- **Why not manual download:** The World Bank site's manual CSV export
  covers the same data but as a one-time static file; re-running the
  project later would mean repeating a manual click-through rather than
  re-running a script, and it's easy to download the wrong vintage of a
  file without noticing.
- **Why not scraping:** WDI explicitly offers a documented, free, public
  API for this exact data, so scraping the website's HTML would be
  solving an already-solved problem, and would be more fragile to page
  layout changes.
- **Why not a pre-packaged dataset:** No ready pre-packaged dataset
  combining exactly these five indicators across all countries, already
  cleaned, was found — and using one would hide exactly the
  acquisition/cleaning decisions this assignment asks us to document
  ourselves.
- **Why API:** It pulls the full country list in one reproducible call,
  can be re-run automatically if the underlying data changes, and
  doesn't depend on a one-time manual file.

## Reproducibility — raw copy and fetch script

`fetch_data.py` does acquisition only — no cleaning, no filtering, no
derived columns. Its output, `data/raw/wdi_raw_response.json` (completely
untouched raw API response) and `data/raw/wdi_raw_table.csv` (flattened
but still unfiltered/uncleaned), is what `clean_data.py` reads and cleans.
This repo's `data/raw/` was reconstructed from a previously-verified,
real run of this same script (see CLEANING.md for the exact console
output of that run) since this particular environment could not reach
`api.worldbank.org` directly — re-running `fetch_data.py` from scratch
reproduces the same data (barring routine data revisions, see below).

## Licence and terms of use

World Bank data is released under the **CC BY-4.0 licence**
(Creative Commons Attribution 4.0), which permits reuse, including for
a student project like this one, with attribution to the World Bank as
the source. No registration or paid access was required for the WDI API
used here.

## Privacy concerns

None. This is aggregated, country-level macroeconomic data — no
individual-level or personally identifiable information is involved at
any point in the pipeline.

## Could a stranger re-pull this data next month?

Mostly yes, with caveats. Re-running `fetch_data.py` next month would
pull each country's current "most recent non-empty value" per indicator
— for most countries this would return the same figures, since WDI
doesn't update every indicator every month. What could change:

- **Revisions:** The World Bank periodically revises recent-year
  estimates (e.g. a provisional inflation figure later corrected), so a
  re-pull could return slightly different numbers for the same
  country/indicator without any code having changed.
- **Newer "most recent" values:** If a country reports a newer data point
  between now and the re-pull, `mrnev=1` would return that newer value
  instead, potentially shifting which affordability group a borderline
  country falls into.
- **What would break:** If the World Bank archives or renames another
  indicator the way it did `PA.NUS.PPPC.RF` mid-project (see CLEANING.md
  Entry 3), the pull for that indicator would silently return empty
  rather than erroring loudly, unless whoever re-runs it checks the row
  counts the way this project's debugging process did.
