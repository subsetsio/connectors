SELECT
    iso3,
    country,
    CAST(year AS INTEGER) AS year,
    category,
    CAST(score AS DOUBLE) AS score
FROM "nd-gain-readiness"
WHERE score IS NOT NULL
