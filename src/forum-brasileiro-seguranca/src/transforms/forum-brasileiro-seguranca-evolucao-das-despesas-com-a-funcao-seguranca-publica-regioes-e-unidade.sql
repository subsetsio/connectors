SELECT
    geography,
    geo_level,
    CAST(year AS INTEGER) AS year,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "forum-brasileiro-seguranca-evolucao-das-despesas-com-a-funcao-seguranca-publica-regioes-e-unidade"
WHERE value IS NOT NULL AND geography IS NOT NULL
