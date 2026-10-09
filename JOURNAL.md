# Engagement Journal

## Before I looked

This was my first time working with an API, so before running anything I
expected it either wouldn't run at all, or that the results would come out
in a form that was difficult to make sense of. It ended up running well,
and working with an API for the first time went better than I expected —
I'll be using APIs for my own data pulls from now on.

## What I did

I picked five WDI indicators to cover income, price level, and inflation
(GNI per capita PPP, PPP conversion factor, official exchange rate,
inflation, education spend), and pulled them for all countries through the
World Bank API rather than a manual download, so the pull could be
reproduced. The first indicator I wanted for price level,
`PA.NUS.PPPC.RF`, turned out to have been archived by the World Bank — the
API returned an explicit "deleted or archived" error — so I recomputed the
same ratio manually from two indicators that were still live (PPP
conversion factor divided by the official exchange rate). I also tried
using the REST Countries API for extra country metadata, but it returned a
deprecation error for every request, so I dropped it from the pipeline
entirely instead of working around it. Pulling all countries in one date
range also caused a timeout, which I fixed by only requesting each
country's most recent non-empty value (`mrnev=1`) instead of a full date
range. After the raw data was in, I pivoted it from long to wide (one row
per country), removed the ~47 regional/income-group aggregate codes mixed
into the country list (e.g. "World," "High income"), dropped the countries
missing an essential indicator (201 down to 191), and ran K-Means to group
countries into Budget-Friendly / Mid-Range / Premium tiers.

## What surprised me

The clustering result surprised me the most: when I first ran K-Means
directly on raw inflation values, the "Budget-Friendly" group came out
with an average inflation of 161.96% — it had grouped actual hyperinflation
economies (Venezuela, Zimbabwe, Sudan, Argentina) in with what was supposed
to be the cheapest, most attractive tier for students, purely because a
few extreme values were dominating the distance calculation. I also didn't
expect a precomputed World Bank indicator to just be archived/deleted
mid-project, or for a public countries API to have been fully deprecated —
I'd assumed "official" data sources would be more stable than that.

## What I revised

Once I saw the hyperinflation distortion in the clustering, I capped
inflation at 40% as the input *only* for the K-Means feature, while
keeping the true, uncapped inflation value for everything the tool
actually displays to a user, and added a separate flag
(`economic_instability_flag`) so a country with real hyperinflation is
still clearly marked, just not allowed to wreck the clustering math.

## What I still don't trust

I have full confidence in this project and its results — I went through
every step myself (the API pull, the cleaning, the clustering fix), ran
into real problems along the way, and fixed and verified each one by
actually running the scripts rather than assuming they worked. I trust
this is the best version I could have put together.
