SELECT
    geography,
    geo_level,
    CAST(year AS INTEGER) AS year,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "forum-brasileiro-seguranca-mortes-violentas-intencionais-de-criancas-e-adolescentes-de-0-a-17-ano"
WHERE value IS NOT NULL AND geography IS NOT NULL
