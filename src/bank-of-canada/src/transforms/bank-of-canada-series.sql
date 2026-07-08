SELECT
    series_id,
    label,
    description
FROM "bank-of-canada-series"
WHERE series_id IS NOT NULL
