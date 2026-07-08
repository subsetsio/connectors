SELECT
    geography,
    geo_level,
    CAST(year AS INTEGER) AS year,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "forum-brasileiro-seguranca-bases-salariais-dos-vigilantes-por-tipo-de-servico"
WHERE value IS NOT NULL AND geography IS NOT NULL
