SELECT DISTINCT
    CAST(date AS DATE)              AS date,
    hemisphere,
    NULLIF(source_dataset, '-9999') AS source_dataset,
    extent_million_km2,
    area_million_km2
FROM "nsidc-sea-ice-extent-monthly"
-- Drop fully-missing months (e.g. the Dec 1987-Jan 1988 sensor gap):
-- a monthly-extent table should carry only real observations.
WHERE extent_million_km2 IS NOT NULL
   OR area_million_km2 IS NOT NULL
ORDER BY hemisphere, date
