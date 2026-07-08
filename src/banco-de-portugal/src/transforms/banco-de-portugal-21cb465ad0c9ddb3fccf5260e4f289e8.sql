SELECT
    CAST(reference_date AS DATE)  AS reference_date,
    CAST(series_id AS BIGINT)     AS series_id,
    series_label,
    CAST(value AS DOUBLE)         AS value
FROM "banco-de-portugal-21cb465ad0c9ddb3fccf5260e4f289e8"
WHERE value IS NOT NULL
