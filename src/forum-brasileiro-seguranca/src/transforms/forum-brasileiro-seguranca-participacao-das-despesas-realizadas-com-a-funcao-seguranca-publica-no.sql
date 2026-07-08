SELECT
    geography,
    geo_level,
    CAST(year AS INTEGER) AS year,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "forum-brasileiro-seguranca-participacao-das-despesas-realizadas-com-a-funcao-seguranca-publica-no"
WHERE value IS NOT NULL AND geography IS NOT NULL
