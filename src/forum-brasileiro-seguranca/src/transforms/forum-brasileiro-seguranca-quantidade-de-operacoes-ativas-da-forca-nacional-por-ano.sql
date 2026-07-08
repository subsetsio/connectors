SELECT
    geography,
    geo_level,
    CAST(year AS INTEGER) AS year,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "forum-brasileiro-seguranca-quantidade-de-operacoes-ativas-da-forca-nacional-por-ano"
WHERE value IS NOT NULL AND geography IS NOT NULL
