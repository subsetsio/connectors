SELECT
    CAST(reference_date AS DATE)  AS reference_date,
    CAST(series_id AS BIGINT)     AS series_id,
    series_label,
    CAST(value AS DOUBLE)         AS value
FROM "banco-de-portugal-f8d9de1f6eafa76afc24ab71b570bf4c"
WHERE value IS NOT NULL
