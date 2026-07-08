SELECT
    geography,
    geo_level,
    CAST(year AS INTEGER) AS year,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "forum-brasileiro-seguranca-abandono-material-art-244-cp"
WHERE value IS NOT NULL AND geography IS NOT NULL
