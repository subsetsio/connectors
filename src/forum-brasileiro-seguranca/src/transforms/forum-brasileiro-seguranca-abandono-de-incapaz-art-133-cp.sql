SELECT
    geography,
    geo_level,
    CAST(year AS INTEGER) AS year,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "forum-brasileiro-seguranca-abandono-de-incapaz-art-133-cp"
WHERE value IS NOT NULL AND geography IS NOT NULL
