-- caution: `region` carries a "World" total alongside the eight Maddison
-- regions -- filter it out before summing or ranking across regions.
-- caution: `year` is benchmark years, not an annual series: decadal 1820-2010,
-- then annual 2015-2022. Consecutive rows are not consecutive years.
SELECT
    region                  AS region,
    CAST(year AS INTEGER)   AS year,
    CAST(gdppc AS DOUBLE)   AS gdp_per_capita,
    CAST(pop AS DOUBLE)     AS population
FROM "maddison-project-regional-aggregates"
WHERE gdppc IS NOT NULL OR pop IS NOT NULL
