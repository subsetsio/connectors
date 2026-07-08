SELECT
    CAST(reference_date AS DATE)  AS reference_date,
    CAST(series_id AS BIGINT)     AS series_id,
    series_label,
    CAST(value AS DOUBLE)         AS value
FROM "banco-de-portugal-7f13efcd65fc6bd0c5adb0e8d29d9b44"
WHERE value IS NOT NULL
