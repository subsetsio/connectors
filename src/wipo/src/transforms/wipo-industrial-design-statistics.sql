SELECT
    office,
    origin,
    indicator_id,
    indicator,
    report_type,
    CAST(year AS INTEGER)          AS year,
    breakdown_index,
    CAST(value AS DOUBLE)          AS value
FROM "wipo-industrial-design-statistics"
WHERE value IS NOT NULL
