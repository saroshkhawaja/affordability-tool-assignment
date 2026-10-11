# Study-Abroad Affordability Comparison Tool

**Course:** Problem Solving with Data Science — ITU, Fall 2026
**Authors:** Khawaja Muhammad Sarosh Abdullah & Syeda Zoya Ali

## Project summary

For a prospective international student, this project compares countries
on affordability for living and studying abroad — GNI per capita (PPP), a
relative price-level ratio, and inflation — pulled from the World Bank
World Development Indicators (WDI) API, so that a student can get a
side-by-side comparison of any two countries and see which affordability
tier (Budget-Friendly / Mid-Range / Premium) a country falls into, based
on a K-Means clustering model.

**Live tool:** `index.html`, deployed via GitHub Pages at
https://saroshkhawaja.github.io/affordability-tool-assignment/

## Repo structure

```
index.html                       # The live comparison tool (static HTML/CSS/JS, deployed via GitHub Pages)

fetch_data.py                    # Acquisition only — pulls raw WDI data via API
clean_data.py                    # Cleaning + K-Means clustering -> processed data

data/raw/wdi_raw_response.json   # Untouched raw API response
data/raw/wdi_raw_table.csv       # Untouched, flattened (unfiltered) raw data
data/processed/countries_clean.csv  # Final cleaned, clustered dataset (191 countries)

notebooks/eda.py                 # EDA script -> generates notebooks/eda_charts.png
notebooks/eda_charts.png         # The 5 EDA charts referenced in EDA.md
notebooks/build_real_data.py     # Reconstructs this repo's data/ from the verified,
                                  # previously-captured real API output

PROPOSAL_V2.md                   # Updated Framing Formula proposal + what changed since v1
CLEANING.md                      # Cleaning decision log (one entry per loop cycle)
DATA_DICTIONARY.md               # Every column: type, unit, definition, source, caveats
FIVE_QUESTIONS.md                # Row / outcome / timeframe / missingness / sampling frame
EDA.md                           # Charts, transformation, five properties, confounder check, findings
MODELING.md                      # Why K-Means, choosing k, cluster diagnostics, what was rejected
JOURNAL.md                       # Engagement journal (before I looked, what I did, what surprised me, etc.)
LIMITATIONS.md                   # Known limitations and risks
AI_USE_LOG.md                    # Required AI-use disclosure
CONTRIBUTIONS.md                 # Signed contribution split
```



## Reproducing the pipeline

```
python3 fetch_data.py     # requires network access to api.worldbank.org
python3 clean_data.py     # reads data/raw/wdi_raw_table.csv -> data/processed/countries_clean.csv
python3 notebooks/eda.py  # reads data/processed/countries_clean.csv -> notebooks/eda_charts.png
```

Both `fetch_data.py` and `clean_data.py` were run for real; the exact
printed console output is quoted in `CLEANING.md`. Running them again
reproduces the same 191-country dataset, split Mid-Range 129 / Premium 52
/ Budget-Friendly 10 (see `CLEANING.md` for the full verified run output).

## Deployment

`index.html` is a single self-contained static page — HTML, CSS, and
JavaScript, with all 201 countries' data embedded directly in the page as
a JavaScript array. No backend or database is needed since the data
doesn't change in real time. It's deployed for free via **GitHub Pages**,
serving directly from this repo's `main` branch.
