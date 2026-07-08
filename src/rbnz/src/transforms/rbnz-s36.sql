SELECT DISTINCT
    CAST(date AS DATE)     AS date,
    series_code,
    option,
    indicator_label,
    series_id,
    series_name,
    unit,
    CAST(value AS DOUBLE)  AS value
FROM "rbnz-s36"
WHERE value IS NOT NULL AND date IS NOT NULL
ORDER BY date, indicator_label
