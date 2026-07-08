SELECT
    CAST(reference_date AS DATE)  AS reference_date,
    CAST(series_id AS BIGINT)     AS series_id,
    series_label,
    CAST(value AS DOUBLE)         AS value
FROM "banco-de-portugal-b57d7d3c318057c5c9e43b5e4671e4ae"
WHERE value IS NOT NULL
