### 1. What is a row?

The raw data set consists of individual indicator values for each country or territory for each year. This long-form data is then filtered and transformed to country level data in the cleaning script, resulting in a final dataset of 191 rows and 12 columns. So each row should be used to represent one country or one country's separate report, but an extra check of the country codes is still required to ensure that all records are distinct. Confidence: High regarding desired structure, but not verified as yet for uniqueness.

### 2. What is the result (and the units)?

The data set contains a number of economic indicators; namely: GNI per capita PPP (current international dollars per capita, dimensionless); price-level ratio (dimensionless); and inflation (annual percentage). It also provides an affordability cluster group, which is a k-means clustering of some data. This group is a derived categorical label, and is not a World Bank indicator, but it is not a measure of tuition fees, accommodation costs or students' household budgets. The indicator units should be confirmed using World Bank metadata. Confidence: high for the units documented and subject to metadata verification and medium for the interpretation of the derived classification.

### 3. How long is the time period?

It is important to note that data were provided for the latest point available, not as a comparison to a single year: The acquisition script is configured with mrnev=1; which means that the most recent non-empty observation for each country and indicator is returned as the latest-available point. This means that GNI per capita and inflation figures can be from different years for the same country, making it difficult to compare in time. To determine the degree of this variation, the actual earliest and latest reporting year(s) and the number of observations in each year must be known. Confidence: high for the expected behavior of the API, lower for the cross-country temporal comparability of the dataset until the reporting years are confirmed.

### 4. Who is missing?

The country-level dataset, which was reduced from 201 to 191 records to remove information for Andorra, Bermuda, Eritrea, Faroe Islands, Greenland, Marshall Islands, Puerto Rico US, Somalia Fed Rep, Turkmenistan, and Turks and Caicos Islands, was compared with an earlier dataset. There were also 26 rows removed because essential indicators were not available, but these rows were removed at a different stage in the cleaning process and may not be 26 more countries. This newer API download should be compared individually to check if the same exclusions are used. Confidence: High for earlier file comparison, but the exclusions for the current dataset have yet to be verified.

### 5. What is the population from which we want to collect these samples?

The project fetches World Bank World Development Indicators (WDI) data from the `/country/all/indicator/` API endpoint, which can offer country, territory, and regional aggregates. This cleaning script excludes aggregates and records that do not have the key indicators, resulting in a dataset that is based on data availability, not a formal random sample. In addition, the statistics for WDI can also be derived from national surveys, administrative records or statistical models, depending on the indicator. World Bank metadata and methodological documentation are needed to establish the precise data-production methods. Confidence: High in the API selection mechanism and limited in the methods used to gather the data, until the source documentation is verified.
