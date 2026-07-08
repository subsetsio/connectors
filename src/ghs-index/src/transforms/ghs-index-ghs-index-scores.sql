SELECT
    country,
    CAST(year AS INTEGER)      AS year,
    indicator_code,
    indicator_label,
    level,
    CAST(score AS DOUBLE)      AS score
FROM "ghs-index-ghs-index-scores"
WHERE score IS NOT NULL
