# Study-Abroad Affordability Comparison Tool

**Course:** Problem Solving with Data Science — ITU, Fall 2026
**Authors:** Khawaja Muhammad Sarosh Abdullah & Syeda Zoya Ali

## Project summary

For a prospective international student, this project compares countries on
affordability for living and studying abroad — GNI per capita (PPP), a
relative price-level ratio, and inflation — pulled live from the World Bank
World Development Indicators (WDI) API, so that a student can get a
side-by-side comparison of any two countries and see which affordability
tier (Budget-Friendly / Mid-Range / Premium) a country falls into, based on
a K-Means clustering model.

**Live tool:** https://claude.ai/artifact/RuXMTffUqpBFsnWzsbZGS8

## Repo structure

```
fetch_data.py                   # Acquisition only — pulls raw WDI data via API
clean_data.py                   # Cleaning + K-Means clustering -> processed data
notebooks/build_real_data.py    # Reconstructs this repo's data/ from the verified
                                 # real API output already captured during fetch_data.py's
                                 # confirmed run (see note in that file)
data/raw/                        # Untouched, as-fetched data
data/processed/countries_clean.csv  # Final cleaned, clustered dataset (191 countries)
CLEANING.md                      # Cleaning decision log
DATA_DICTIONARY.md               # Column definitions
FIVE_QUESTIONS.md                # Row/outcome/timeframe/missingness/sampling frame
JOURNAL.md                       # Engagement journal
LIMITATIONS.md                   # Known limitations
AI_USE_LOG.md                    # Required AI-use disclosure
CONTRIBUTIONS.md                 # Signed contribution split
```

## Reproducing the pipeline

```
python3 fetch_data.py     # requires network access to api.worldbank.org
python3 clean_data.py     # reads data/raw/wdi_raw_table.csv -> data/processed/countries_clean.csv
```

Both scripts were run for real on the author's machine; the exact printed
output is quoted in CLEANING.md and JOURNAL.md. `data/raw/` and
`data/processed/` in this repo were reconstructed by
`notebooks/build_real_data.py` from that same real, previously-captured API
output (direct internet access to api.worldbank.org was not available in
the environment used to assemble this repo), and reproduce the identical
191-country / 129-52-10 split confirmed in the original run.
