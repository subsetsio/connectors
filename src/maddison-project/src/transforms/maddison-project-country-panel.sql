-- caution: Every row is a country; there are no aggregate-region or world-total
-- rows. Use maddison-project-regional-aggregates for region-level series.
-- caution: Dissolved states run alongside their successors over overlapping
-- years (SUN beside RUS, YUG beside SRB, CSK beside CZE). Summing across all
-- country codes in a year double-counts those territories.
-- caution: gdp_per_capita is a ratio -- weight by population to aggregate it.
-- The raw sheet is a dense country x year grid in which ~82% of rows carry
-- neither estimate. Drop those: a row here means at least one value was observed.
SELECT
    countrycode             AS country_code,
    country                 AS country,
    region                  AS region,
    CAST(year AS INTEGER)   AS year,
    CAST(gdppc AS DOUBLE)   AS gdp_per_capita,
    CAST(pop AS DOUBLE)     AS population
FROM "maddison-project-country-panel"
WHERE gdppc IS NOT NULL OR pop IS NOT NULL
