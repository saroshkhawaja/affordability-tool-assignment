# Acquisition Record

The World Bank World Development Indicators (WDI) database is the source for this information.
data are derived from national statistical data collected by the World Bank from member countries' national statistical data.
agencies (and, in some cases, World Bank economists themselves).
In particular for monitoring global development and economic indicators for
Application of policy and research.

The exact date of: October 2026 (see commit history for date pulled)
Running this repo's `data/raw/` is the `fetch_data.py` (reflects).

New York is the source of the data, and the data is in current dollars.
PA.NUS.PPP and PA.NUS.FCRF (combined to calculate price level)
The data is available for the following categories: `FP.CPI.TOTL.ZG` (inflation), `SE.XPD.TOTL.GD.ZS` (education), and so on).
spend % GDP).

Explain why you selected a particular method to acquire your product and why you did not choose any of the other methods.

The four acquisition methods (API, manual download, web scraping, or SMS) were used at each stage.At every stage, the four acquisition methods (API, manual download, web scraping, or SMS) were employed.
API was used, which is a pre-packaged dataset.

Why not manual download: Manual export from World Bank site:
  serves a single time snapshot of the data; rerunning the
  project later would imply a manual click-through instead of.
  Avoid re-running a script, and it's simple to download the wrong vintage of a script.
  file without noticing.
The real question is: why not scraping? WDI explicitly provides a well-documented, free, public,
  Scraping the HTML of this particular website would be API for this exact data.
  Solving a solved problem, would be more fragile to page
  layout changes.
Why not a pre-packaged dataset:
  combining these five indicators exactly in this manner already in all countries,
  It was discovered — and if used would conceal exactly the opposite of — the truth of what was seen.
  This assignment requests that we record the decisions made in the acquisition/cleaning process
  ourselves.
- **Why API:** It fetches the complete list of countries in a single consistent API call,
  can be automatically re-run when the data that it uses changes,
  Not reliant on a single, manual file.

This script's results are not guaranteed to be reproducible.The results of this script are not guaranteed to be reproducible.

`fetch_data.py` only does acquisition — no cleaning, no filtering, no
derived columns. Its output, `data/raw/wdi_raw_response.json` (completely
untouched raw API response) and `data/raw/wdi_raw_table.csv` (flattened
The data that the script `clean_data.py` reads and cleans are the but still unfiltered/uncleaned.
This repo's data/raw/ was recreated from a previously-verified,
This is a real run of this same script (see CLEANING.md for the exact console)
This particular environment could not reach output (of that run)
Using the direct link to the API: api.worldbank.org — re-running `fetch_data.py` from scratch
Reproduces the same data (except for routine data revisions, see below).

## Licence and terms of use

The World Bank's data is licensed under the CC BY-4.0 licence.
The CC BY-ND-4.0 license allows for reuse, including for:
A student project complete with citation to the World Bank as a source, is included.This is included as a student project, with proper citation to the World Bank as a source.
the source. The WDI API did not require any paid access or registration.
used here.

## Privacy concerns

None. This is macroeconomic data at a country level, aggregated —
individually identifiable data is at play (e.g., personally identifiable information)
any point in the pipeline.

May be able to re-pull this data again next month?

Yes, for the most part, but with exceptions. If the above was run again next month it would
For each indicator, pull each countries current "most recent non empty value"
— for most countries this would get the same results as WDI
Does not update all indicators monthly. What could change:

- Revisions: The World Bank updates the data of recent years.
  estimates such as a provisional inflation figure revised later, so a
  re-pull may give a slightly different set of values for the same
  no_change.country/indicator with no change in the code.
When a newer "most recent" data value is reported:
  If you change the value of `mrnev=1` between the re-pull and now, it will return that newer value
  Rather, perhaps altering who a borderline is in relation to the affordability group.
  country falls into.
- If the World Bank archives or renames another, what would it be?
  mid-project (see CLEANING.md) it indicates in the same way as it did `PA.NUS.PPPC.RF`.
  As for Entry 3), the force for that indicator would simply return an empty string (no result).
  Unless the person who re-runs it verifies the row, don't shout "error" loudly, but rather silently.
  This project's debugging process has been similar to counts.
