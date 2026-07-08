SELECT
    CAST(reference_date AS DATE)  AS reference_date,
    CAST(series_id AS BIGINT)     AS series_id,
    series_label,
    CAST(value AS DOUBLE)         AS value
FROM "banco-de-portugal-38fa260d12e2d0c4f648fe3e6eabccf8"
WHERE value IS NOT NULL
