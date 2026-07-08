SELECT
    CAST(reference_date AS DATE)  AS reference_date,
    CAST(series_id AS BIGINT)     AS series_id,
    series_label,
    CAST(value AS DOUBLE)         AS value
FROM "banco-de-portugal-348f0a09f36f47c5eef24187b4b4afaa"
WHERE value IS NOT NULL
