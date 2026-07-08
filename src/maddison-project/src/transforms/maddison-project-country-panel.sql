SELECT
    countrycode,
    country,
    region,
    CAST(year AS INTEGER) AS year,
    CAST(gdppc AS DOUBLE) AS gdppc,
    CAST(pop AS DOUBLE)   AS pop
FROM "maddison-project-country-panel"
WHERE gdppc IS NOT NULL OR pop IS NOT NULL
