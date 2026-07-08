SELECT
    geography,
    geo_level,
    CAST(year AS INTEGER) AS year,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "forum-brasileiro-seguranca-exploracao-sexual-infantil-art-218-b-do-cp-e-art-244-a-do-eca"
WHERE value IS NOT NULL AND geography IS NOT NULL
