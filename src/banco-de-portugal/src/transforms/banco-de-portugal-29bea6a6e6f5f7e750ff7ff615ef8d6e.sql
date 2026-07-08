SELECT
    CAST(reference_date AS DATE)  AS reference_date,
    CAST(series_id AS BIGINT)     AS series_id,
    series_label,
    CAST(value AS DOUBLE)         AS value
FROM "banco-de-portugal-29bea6a6e6f5f7e750ff7ff615ef8d6e"
WHERE value IS NOT NULL
