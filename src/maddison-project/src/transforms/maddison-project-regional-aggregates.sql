SELECT
    region,
    CAST(year AS INTEGER) AS year,
    CAST(gdppc AS DOUBLE) AS gdppc,
    CAST(pop AS DOUBLE)   AS pop
FROM "maddison-project-regional-aggregates"
WHERE gdppc IS NOT NULL OR pop IS NOT NULL
