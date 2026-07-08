SELECT
    country,
    country_code,
    region,
    year,
    indicator,
    CAST(score AS DOUBLE) AS score
FROM "world-justice-project-rule-of-law-index"
WHERE score IS NOT NULL
  AND country IS NOT NULL
  AND indicator IS NOT NULL
