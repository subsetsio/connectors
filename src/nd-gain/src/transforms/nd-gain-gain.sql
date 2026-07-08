SELECT
    iso3,
    country,
    CAST(year AS INTEGER) AS year,
    CAST(score AS DOUBLE) AS score
FROM "nd-gain-gain"
WHERE score IS NOT NULL
