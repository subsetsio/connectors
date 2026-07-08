SELECT
    CAST(reference_date AS DATE)  AS reference_date,
    CAST(series_id AS BIGINT)     AS series_id,
    series_label,
    CAST(value AS DOUBLE)         AS value
FROM "banco-de-portugal-d64e4ec9e100e1eb22e7eeb21a298d09"
WHERE value IS NOT NULL
