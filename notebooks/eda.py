"""
eda.py
Exploratory Data Analysis for the Study-Abroad Affordability Comparison
project. Reads the final cleaned file (data/processed/countries_clean.csv)
and produces a 5-chart figure plus the printed summary stats quoted in
EDA.md. Capped at 5 charts per the assignment's 3-5 chart limit.
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.read_csv("data/processed/countries_clean.csv")

fig, axes = plt.subplots(2, 3, figsize=(16, 9))
axes = axes.flatten()
axes[5].axis("off")  # only 5 charts used; 6th grid cell left blank

# 1. GNI per capita PPP — raw distribution (the "before" half of the
# transformation pair)
axes[0].hist(df["gni_per_capita_ppp"], bins=30, color="#4C72B0", edgecolor="white")
axes[0].set_title("GNI per Capita (PPP) Is Heavily Right-Skewed\n"
                   "A small number of high-income countries stretch the tail",
                   fontsize=10)
axes[0].set_xlabel("GNI per capita, PPP (intl $)")
axes[0].set_ylabel("Number of countries")

# 2. log(GNI per capita) — the "after" half of the transformation
axes[1].hist(np.log10(df["gni_per_capita_ppp"]), bins=30, color="#55A868", edgecolor="white")
axes[1].set_title("Log-Transforming GNI Makes It Roughly Symmetric\n"
                   "Same variable, log10 scale — skew drops from 1.27 to -0.38",
                   fontsize=10)
axes[1].set_xlabel("log10(GNI per capita, PPP)")
axes[1].set_ylabel("Number of countries")

# 3. GNI vs price level ratio, colored by affordability group
colors = {"Budget-Friendly": "#55A868", "Mid-Range": "#4C72B0", "Premium": "#C44E52"}
for grp, sub in df.groupby("affordability_group"):
    axes[2].scatter(sub["gni_per_capita_ppp"], sub["price_level_ratio"],
                     label=grp, color=colors[grp], alpha=0.7, s=25)
axes[2].set_title("Affordability Groups Separate Along Income & Price Level\n"
                   "K-Means groups roughly follow these two axes",
                   fontsize=10)
axes[2].set_xlabel("GNI per capita, PPP (intl $)")
axes[2].set_ylabel("Price level ratio")
axes[2].legend(fontsize=8)

# 4. Confounder check: slice the same relationship by a third variable
# (economic_instability_flag) to see whether the story changes
for flag, sub in df.groupby("economic_instability_flag"):
    axes[3].scatter(sub["gni_per_capita_ppp"], sub["price_level_ratio"],
                     label=f"Unstable inflation (>40%): {flag}",
                     alpha=0.7, s=25,
                     color="#C44E52" if flag else "#4C72B0")
axes[3].set_title("Confounder Check: Instability Flag vs the Same Axes\n"
                   "Story holds: instability isn't what separates the groups",
                   fontsize=10)
axes[3].set_xlabel("GNI per capita, PPP (intl $)")
axes[3].set_ylabel("Price level ratio")
axes[3].legend(fontsize=8)

# 5. Cluster sizes
counts = df["affordability_group"].value_counts().reindex(
    ["Budget-Friendly", "Mid-Range", "Premium"])
axes[4].bar(counts.index, counts.values,
            color=[colors[g] for g in counts.index])
axes[4].set_title("Mid-Range Dominates the Affordability Groups\n"
                   "129 Mid-Range vs 52 Premium vs 10 Budget-Friendly",
                   fontsize=10)
axes[4].set_ylabel("Number of countries")
for i, v in enumerate(counts.values):
    axes[4].text(i, v + 1, str(v), ha="center")

plt.tight_layout()
plt.savefig("notebooks/eda_charts.png", dpi=150)
print("Saved notebooks/eda_charts.png")

# Printed summary stats, quoted in EDA.md
print("\n--- Summary stats ---")
print(df[["gni_per_capita_ppp", "price_level_ratio", "inflation_pct"]].describe())
print("\nSkew of gni_per_capita_ppp (raw):", df["gni_per_capita_ppp"].skew())
print("Skew of log10(gni_per_capita_ppp):", np.log10(df["gni_per_capita_ppp"]).skew())
print("\nCountries flagged economic_instability_flag=True:")
print(df.loc[df["economic_instability_flag"], ["country_name", "inflation_pct", "affordability_group"]])
print("\nMean inflation_pct by affordability_group (true, uncapped values):")
print(df.groupby("affordability_group")["inflation_pct"].mean())
