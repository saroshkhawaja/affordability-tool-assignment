# Limitations

1. **Snapshot, not a time series.** Each indicator uses the most recent
   available value per country (`mrnev=1`), which may come from different
   years for different countries. Two countries shown side-by-side are not
   guaranteed to be compared in the same year.

2. **Clustering is a modeling choice, not ground truth.** The
   Budget-Friendly / Mid-Range / Premium labels come from K-Means with
   k=3, a fixed random seed, and three chosen features. A different k, a
   different feature set, or a different scaling choice could place some
   borderline countries in a different group. The group a country falls
   into should be read as "similar to other countries in this group on
   these three measures," not as an authoritative affordability rating.

3. **Price level ratio is a manual reconstruction.** The original WDI
   indicator intended for this (`PA.NUS.PPPC.RF`) was archived by the World
   Bank mid-project. The version used here (`PPP conversion factor ÷
   official exchange rate`) is a standard approximation but is not
   identical to the original discontinued series, and may behave
   differently for countries with multiple/parallel exchange rates.

4. **Reporting-year mismatch in price-level ratio.**
There are 191 countries in the world, of which 23 countries (about 12%) report the PPP conversion factor and exchange rate in different years. In the case of Afghanistan, for instance, the exchange-rate value is from 2020, and the PPP conversion factor is from 2024. Calculating price_level_ratio with different years may result in misleading values, and may influence comparisons of affordability and the K-Means clustering. The next step would be to examine if these values are retrievable in the same year or if it would be more accurate to flag these mismatched records for analysis.

5. **Smaller territories are underrepresented.** The 10 countries/
   territories dropped for missing essential data are disproportionately
   small island nations and dependent territories, so the comparison tool
   is most reliable for larger, more data-complete economies.

6. **No cost-of-living detail below the national level.** GNI per capita
   and the price-level ratio are national averages; actual cost of living
   for a student depends heavily on the specific city (a capital city is
   often far more expensive than the national average suggests).

7. **Inflation capping for clustering trades off precision for
   robustness.** Capping inflation at 40% for clustering input prevents a
   few hyperinflation countries from dominating the distance calculation,
   but it also means the clustering algorithm cannot distinguish between,
   say, 45% and 250% inflation — both get treated identically as "high."
   The `economic_instability_flag` column is intended to compensate for
   this by surfacing the distinction separately.

8. **Not causal, not predictive.** This is a descriptive comparison and
   grouping tool. It does not predict future affordability and should not
   be read as recommending one country's immigration, tuition, or
   cost-of-living policy over another's.
