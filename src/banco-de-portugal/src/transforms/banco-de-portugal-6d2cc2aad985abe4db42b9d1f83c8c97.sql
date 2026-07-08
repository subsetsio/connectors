SELECT
    CAST(reference_date AS DATE)  AS reference_date,
    CAST(series_id AS BIGINT)     AS series_id,
    series_label,
    CAST(value AS DOUBLE)         AS value
FROM "banco-de-portugal-6d2cc2aad985abe4db42b9d1f83c8c97"
WHERE value IS NOT NULL
