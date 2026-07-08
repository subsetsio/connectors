SELECT
    CAST(reference_date AS DATE)  AS reference_date,
    CAST(series_id AS BIGINT)     AS series_id,
    series_label,
    CAST(value AS DOUBLE)         AS value
FROM "banco-de-portugal-9744c7a78f7417d4a91cf1a1b55fac1d"
WHERE value IS NOT NULL
