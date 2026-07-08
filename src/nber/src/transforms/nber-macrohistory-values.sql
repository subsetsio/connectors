SELECT
    series_id,
    CAST(date AS DATE) AS date,
    CAST(value AS DOUBLE) AS value,
    frequency,
    chapter
FROM "nber-macrohistory-values"
WHERE value IS NOT NULL
