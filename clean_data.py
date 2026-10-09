"""
clean_data.py
Cleaning + modeling script for the Study-Abroad Affordability Comparison project.

Reads the untouched raw table from fetch_data.py (data/raw/wdi_raw_table.csv),
applies every documented cleaning decision (see CLEANING.md for the full
reasoning behind each one), and produces a single clean, model-ready file:
data/processed/countries_clean.csv

Run fetch_data.py first. This script runs top to bottom with no manual steps,
so the raw-to-clean pipeline is fully reproducible. Confirmed working run
(see CLEANING.md entry log): 1159 raw rows in -> 191 countries out, split
Mid-Range 129 / Premium 52 / Budget-Friendly 10.
"""

import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

RAW_PATH = "data/raw/wdi_raw_table.csv"
PROCESSED_DIR = "data/processed"

# World Bank aggregate / region codes — NOT real countries.
# Removing these is CLEANING.md Entry: these are regional/income-group
# summaries (e.g. "World", "High income") mixed into the country list.
AGG_CODES = [
    "ARB", "EAS", "EAP", "ECS", "ECA", "EMU", "EUU", "HIC", "IBD", "IBT", "IDA",
    "IDB", "IDX", "LCN", "LAC", "LDC", "LIC", "LMC", "LMY", "MIC", "MNA", "NAC",
    "OED", "SAS", "SSA", "SSF", "SST", "WLD", "AFE", "AFW", "CSS", "CEB", "EAR",
    "LTE", "MEA", "OSS", "PSS", "PST", "PRE", "TEA", "TEC", "TLA", "TMN", "TSA",
    "TSS", "HPC", "INX", "UMC",
]

# Threshold used to cap extreme inflation for CLUSTERING ONLY — the true,
# uncapped value is still kept and displayed to the user. CLEANING.md entry:
# hyperinflation outliers (Venezuela, Zimbabwe, Sudan, Argentina) were
# distorting K-Means groupings so badly that unstable economies were being
# mislabeled as "Budget-Friendly" (that cluster's average inflation was ~162%).
INFLATION_CAP = 40
INSTABILITY_THRESHOLD = 40


def load_raw():
    df = pd.read_csv(RAW_PATH)
    print(f"Raw rows loaded: {len(df)}")
    return df


def pivot_to_country_rows(raw):
    """Raw table is long (one row per country-indicator). Pivot so each row
    is one country, with one column per indicator — this is what makes it a
    usable panel/cross-section rather than a long list."""
    wide = raw.pivot_table(
        index=["country_code", "country_name"],
        columns="indicator_name",
        values="value",
        aggfunc="first",
    ).reset_index()
    return wide


def remove_aggregates(df):
    before = len(df)
    df = df[~df["country_code"].isin(AGG_CODES)].copy()
    print(f"Removed {before - len(df)} aggregate/region rows (e.g. World, High income).")
    return df


def compute_price_level_ratio(df):
    """PA.NUS.PPPC.RF (the original precomputed price-level indicator) was
    archived by the World Bank mid-project (API returned: 'The indicator was
    not found. It may have been deleted or archived.'). Recalculated manually
    from two indicators that are still live."""
    df["price_level_ratio"] = df["ppp_conversion_factor"] / df["official_exchange_rate"]
    return df


def drop_incomplete_rows(df):
    """Keep only countries with the 3 essential indicators needed for
    comparison + clustering. education_spend_pct_gdp is allowed to stay
    missing (displayed as 'not reported'), since it's a secondary field,
    not used in the core score or in clustering."""
    before = len(df)
    df = df.dropna(subset=["gni_per_capita_ppp", "price_level_ratio", "inflation_pct"]).copy()
    print(f"Dropped {before - len(df)} rows missing an essential indicator "
          f"(gni_per_capita_ppp, price_level_ratio, or inflation_pct). "
          f"Remaining: {len(df)} countries.")
    return df


def cluster_affordability(df):
    """K-Means clustering into 3 affordability tiers. Inflation is capped
    at INFLATION_CAP for clustering only, so hyperinflation outliers don't
    dominate the distance calculation — the true value is kept separately
    in `inflation_pct` and shown to users unmodified."""
    df["inflation_capped"] = df["inflation_pct"].clip(upper=INFLATION_CAP)
    df["economic_instability_flag"] = df["inflation_pct"] > INSTABILITY_THRESHOLD

    features = ["gni_per_capita_ppp", "price_level_ratio", "inflation_capped"]
    X = StandardScaler().fit_transform(df[features])

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df["cluster"] = kmeans.fit_predict(X)

    cluster_order = df.groupby("cluster")["gni_per_capita_ppp"].mean().sort_values().index
    label_map = {
        cluster_order[0]: "Budget-Friendly",
        cluster_order[1]: "Mid-Range",
        cluster_order[2]: "Premium",
    }
    df["affordability_group"] = df["cluster"].map(label_map)

    print("\nAffordability group sizes:")
    print(df["affordability_group"].value_counts())
    return df


def main():
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    raw = load_raw()
    df = pivot_to_country_rows(raw)
    df = remove_aggregates(df)
    df = compute_price_level_ratio(df)
    df = drop_incomplete_rows(df)
    df = cluster_affordability(df)

    out_path = os.path.join(PROCESSED_DIR, "countries_clean.csv")
    df.to_csv(out_path, index=False)
    print(f"\nSaved cleaned, clustered data -> {out_path}")
    print(f"Final shape: {df.shape}")


if __name__ == "__main__":
    main()
