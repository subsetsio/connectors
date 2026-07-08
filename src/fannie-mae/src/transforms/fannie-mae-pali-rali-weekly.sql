SELECT
    CAST(week_ending AS DATE) AS week_ending,
    CAST(metric AS VARCHAR)   AS metric,
    CAST(value AS DOUBLE)     AS value
FROM "fannie-mae-pali-rali-weekly"
WHERE value IS NOT NULL
