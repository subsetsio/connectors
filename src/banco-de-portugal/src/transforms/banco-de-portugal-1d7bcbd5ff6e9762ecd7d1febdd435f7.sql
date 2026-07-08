SELECT
    CAST(reference_date AS DATE)  AS reference_date,
    CAST(series_id AS BIGINT)     AS series_id,
    series_label,
    CAST(value AS DOUBLE)         AS value
FROM "banco-de-portugal-1d7bcbd5ff6e9762ecd7d1febdd435f7"
WHERE value IS NOT NULL
