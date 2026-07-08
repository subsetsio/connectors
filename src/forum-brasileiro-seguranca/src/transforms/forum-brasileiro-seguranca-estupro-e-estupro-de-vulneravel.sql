SELECT
    geography,
    geo_level,
    CAST(year AS INTEGER) AS year,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "forum-brasileiro-seguranca-estupro-e-estupro-de-vulneravel"
WHERE value IS NOT NULL AND geography IS NOT NULL
