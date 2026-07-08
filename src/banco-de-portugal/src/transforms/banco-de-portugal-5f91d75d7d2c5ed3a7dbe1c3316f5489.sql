SELECT
    CAST(reference_date AS DATE)  AS reference_date,
    CAST(series_id AS BIGINT)     AS series_id,
    series_label,
    CAST(value AS DOUBLE)         AS value
FROM "banco-de-portugal-5f91d75d7d2c5ed3a7dbe1c3316f5489"
WHERE value IS NOT NULL
