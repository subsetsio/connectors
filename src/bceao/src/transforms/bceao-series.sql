SELECT
    series_code,
    frequency,
    label,
    sector,
    subsector,
    NULLIF(unit, '')      AS unit,
    valuation,
    localities,
    locality_count
FROM "bceao-series"
WHERE series_code IS NOT NULL
