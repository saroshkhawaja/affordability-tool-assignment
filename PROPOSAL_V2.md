# Project Proposal (v2)

**Course:** Problem Solving with Data Science — ITU, Fall 2026
**Authors:** Khawaja Muhammad Sarosh Abdullah & Syeda Zoya Ali

## Framing statement

For a **prospective international student** deciding where to study abroad,
this project **groups and compares countries** on affordability — using
income, relative price level, and inflation from the **World Bank World
Development Indicators (WDI) API** — to a level **validated by a
reproducible clustering pipeline run against 191 countries**, so that a
**student weighing study-abroad destinations** can **shortlist and compare
countries** by affordability tier before researching any one country in
depth.

## Stakeholder

A prospective international student (and, secondarily, a study-abroad
advisor helping students narrow down destination options).

## Users

Students comparing two or more countries side-by-side, or browsing a
ranked/grouped view of all countries to shortlist candidates.

## Problem type

Primarily **descriptive/comparative** (a ranked side-by-side comparison
tool), with one **unsupervised learning** component: K-Means clustering
groups countries into three affordability tiers (Budget-Friendly,
Mid-Range, Premium) based on income, price level, and inflation.

## Sampling frame

All countries/territories the World Bank API returns a value for across
the five chosen indicators — 201 before cleaning, 191 after dropping
countries missing an essential indicator (see CLEANING.md). This excludes
places WDI does not cover at all and a small number of mostly island
nations/territories missing inflation data.

## Baseline

Before any modeling, the "baseline" comparison a student would otherwise
do is manually looking up GNI-per-capita rankings or big-cheap-countries
listicles one at a time — slow, inconsistent across sources, and with no
single place to directly compare two specific countries on the same
measures. This project's baseline improvement is simply having the three
core measures for (almost) every country in one place, comparable
side-by-side.

## Cost of error

- **False "Budget-Friendly" label:** A student relying on the group label
  alone, without checking `economic_instability_flag`, could pick a
  country that is "cheap" largely because of a currency/inflation crisis
  rather than genuine low cost of living — a real financial risk if
  tuition or living costs are paid in volatile local currency.
- **Missing/stale indicator values:** Because the tool uses each country's
  most-recent available data point rather than one shared year, two
  countries being compared may not reflect the same point in time, which
  could understate or overstate a real difference.
- **Excluded countries:** A student interested in one of the 10 dropped
  countries/territories gets no data at all from this tool, rather than a
  clearly wrong number — which is a safer failure mode, but still a gap.

## Metric

For the clustering model, success is a qualitative/diagnostic check rather
than a single accuracy number (there's no ground-truth "correct"
affordability label to score against): group sizes should be reasonably
interpretable (not one giant group and two tiny ones), and a confounder
check (does `economic_instability_flag` or extreme inflation alone explain
the grouping, rather than income and price level genuinely separating
countries?) should show the grouping is not purely an artifact of a few
outliers — documented in EDA.md.

## Data source

World Bank World Development Indicators (WDI), via the free public API
(`api.worldbank.org/v2`). Indicators used: `NY.GNP.PCAP.PP.CD` (GNI per
capita, PPP), `PA.NUS.PPP` and `PA.NUS.FCRF` (used together to derive price
level ratio), `FP.CPI.TOTL.ZG` (inflation), and `SE.XPD.TOTL.GD.ZS`
(education spend % GDP, secondary/contextual field).

## Deployment

A live, interactive comparison tool (published web page) lets a user pick
any two countries and see them compared side-by-side, including their
affordability-group label. Live at:
https://claude.ai/artifact/RuXMTffUqpBFsnWzsbZGS8
