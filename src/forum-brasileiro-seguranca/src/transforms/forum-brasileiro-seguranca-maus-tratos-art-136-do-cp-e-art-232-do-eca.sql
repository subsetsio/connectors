SELECT
    geography,
    geo_level,
    CAST(year AS INTEGER) AS year,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "forum-brasileiro-seguranca-maus-tratos-art-136-do-cp-e-art-232-do-eca"
WHERE value IS NOT NULL AND geography IS NOT NULL
