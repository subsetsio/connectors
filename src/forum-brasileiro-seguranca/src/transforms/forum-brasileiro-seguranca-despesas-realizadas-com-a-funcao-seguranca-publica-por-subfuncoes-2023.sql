SELECT
    geography,
    geo_level,
    CAST(year AS INTEGER) AS year,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "forum-brasileiro-seguranca-despesas-realizadas-com-a-funcao-seguranca-publica-por-subfuncoes-2023"
WHERE value IS NOT NULL AND geography IS NOT NULL
