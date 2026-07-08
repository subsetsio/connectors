SELECT
    CAST(reference_date AS DATE)  AS reference_date,
    CAST(series_id AS BIGINT)     AS series_id,
    series_label,
    CAST(value AS DOUBLE)         AS value
FROM "banco-de-portugal-2d8f1e2983223b37ab0ec0130fdc49d8"
WHERE value IS NOT NULL
