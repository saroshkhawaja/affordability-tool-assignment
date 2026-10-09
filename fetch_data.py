"""
fetch_data.py
Acquisition script for the Study-Abroad Affordability Comparison project.

Source: World Bank World Development Indicators (WDI), via the free public API.
Method: API (not manual download or scraping) — chosen because it pulls the
full country list in one reproducible call and can be re-run automatically if
the data changes, rather than depending on a one-time manual file, and because
WDI explicitly offers a documented public API (making scraping unnecessary).

This script does ONLY acquisition — no cleaning, no filtering, no derived
columns. Its output (data/raw/) is the untouched, as-received data, which
clean_data.py then reads and cleans.
"""

import requests
import pandas as pd
import json
import time
import os

INDICATORS = {
    "NY.GNP.PCAP.PP.CD": "gni_per_capita_ppp",
    "PA.NUS.PPP": "ppp_conversion_factor",
    "PA.NUS.FCRF": "official_exchange_rate",
    "FP.CPI.TOTL.ZG": "inflation_pct",
    "SE.XPD.TOTL.GD.ZS": "education_spend_pct_gdp",
}

BASE_URL = "https://api.worldbank.org/v2/country"
RAW_DIR = "data/raw"


def fetch_indicator_all(indicator_code, retries=3):
    """Fetch the most recent non-empty value per country (mrnev=1) for ALL
    countries. mrnev=1 was chosen after an earlier attempt to pull a full
    multi-year date range for all countries in one call caused a
    requests.exceptions.ReadTimeout — asking for only the latest value per
    country is a much lighter request."""
    url = f"{BASE_URL}/all/indicator/{indicator_code}"
    params = {"format": "json", "mrnev": 1, "per_page": 400}

    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, params=params, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            break
        except requests.exceptions.ReadTimeout:
            print(f"  Timeout on attempt {attempt}/{retries} for {indicator_code}, retrying...")
            time.sleep(3)
            if attempt == retries:
                print(f"  FAILED after {retries} attempts: {indicator_code}")
                return None, pd.DataFrame(columns=["country_code", "country_name", "value", "date"])

    if len(data) < 2 or data[1] is None:
        print(f"  WARNING: {indicator_code} returned: {data[0]}")
        return data, pd.DataFrame(columns=["country_code", "country_name", "value", "date"])

    rows = []
    for rec in data[1]:
        if rec["value"] is not None:
            rows.append({
                "country_code": rec["countryiso3code"],
                "country_name": rec["country"]["value"],
                "value": rec["value"],
                "date": rec["date"],
            })
    return data, pd.DataFrame(rows)


def main():
    os.makedirs(RAW_DIR, exist_ok=True)

    raw_json_all = {}
    raw_tables = []

    for code, name in INDICATORS.items():
        print(f"Fetching {name} ({code}) for all countries...")
        raw_json, df = fetch_indicator_all(code)
        raw_json_all[code] = raw_json

        if not df.empty:
            df["indicator_code"] = code
            df["indicator_name"] = name
            raw_tables.append(df)
        time.sleep(1)  # be polite to the API between calls

    with open(os.path.join(RAW_DIR, "wdi_raw_response.json"), "w") as f:
        json.dump(raw_json_all, f)
    print(f"\nSaved untouched raw API response -> {RAW_DIR}/wdi_raw_response.json")

    if raw_tables:
        raw_table = pd.concat(raw_tables, ignore_index=True)
        raw_table.to_csv(os.path.join(RAW_DIR, "wdi_raw_table.csv"), index=False)
        print(f"Saved flattened raw table -> {RAW_DIR}/wdi_raw_table.csv")
        print(f"Total raw rows (all indicators, all countries/aggregates): {len(raw_table)}")


if __name__ == "__main__":
    main()
