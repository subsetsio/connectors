SELECT
    CAST(reference_date AS DATE)  AS reference_date,
    CAST(series_id AS BIGINT)     AS series_id,
    series_label,
    CAST(value AS DOUBLE)         AS value
FROM "banco-de-portugal-d45bb68e792a6b1b2fc36d6a90da4f20"
WHERE value IS NOT NULL
