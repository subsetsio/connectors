SELECT
    CAST(reference_date AS DATE)  AS reference_date,
    CAST(series_id AS BIGINT)     AS series_id,
    series_label,
    CAST(value AS DOUBLE)         AS value
FROM "banco-de-portugal-f648a7e7dec2e61dd4bdd6ba56ac519b"
WHERE value IS NOT NULL
