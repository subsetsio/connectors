SELECT
    CAST(reference_date AS DATE)  AS reference_date,
    CAST(series_id AS BIGINT)     AS series_id,
    series_label,
    CAST(value AS DOUBLE)         AS value
FROM "banco-de-portugal-4d73fa9f4befd82d7aa1d75debd79bd2"
WHERE value IS NOT NULL
