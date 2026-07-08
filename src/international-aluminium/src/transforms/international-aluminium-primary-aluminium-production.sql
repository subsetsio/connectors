SELECT
    CAST(period_start AS DATE) AS period_start,
    CAST(period_end   AS DATE) AS period_end,
    period_name,
    series_group,
    series,
    category,
    CAST(value AS DOUBLE)      AS value
FROM "international-aluminium-primary-aluminium-production"
WHERE value IS NOT NULL
