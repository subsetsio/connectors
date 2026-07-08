SELECT
    geography,
    geo_level,
    CAST(year AS INTEGER) AS year,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "forum-brasileiro-seguranca-subtracao-de-criancas-e-adolescentes-art-249-do-cp-e-art-237-do-eca"
WHERE value IS NOT NULL AND geography IS NOT NULL
