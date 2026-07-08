SELECT
    geography,
    geo_level,
    CAST(year AS INTEGER) AS year,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "forum-brasileiro-seguranca-quantidade-de-operacoes-ativas-de-garantia-da-lei-e-ordem-glo-por-ano"
WHERE value IS NOT NULL AND geography IS NOT NULL
