SELECT
    series_code,
    locality,
    country,
    frequency,
    CAST(date AS DATE)    AS date,
    CAST(value AS DOUBLE) AS value,
    label,
    sector,
    subsector,
    NULLIF(unit, '')                  AS unit,
    NULLIF(magnitude, '')             AS magnitude,
    NULLIF(source, '')                AS source,
    NULLIF(series_type, '')           AS series_type,
    NULLIF(method, '')                AS method,
    period
FROM "bceao-values"
WHERE value IS NOT NULL AND date IS NOT NULL
