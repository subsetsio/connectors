SELECT
    CAST(reference_date AS DATE)  AS reference_date,
    CAST(series_id AS BIGINT)     AS series_id,
    series_label,
    CAST(value AS DOUBLE)         AS value
FROM "banco-de-portugal-4900a7b66f6890857b1eeb2edb1e1148"
WHERE value IS NOT NULL
