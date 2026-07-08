SELECT
    geography,
    geo_level,
    CAST(year AS INTEGER) AS year,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "forum-brasileiro-seguranca-policiais-civis-e-militares-vitimas-de-cvli-em-servico-e-fora-de-servi"
WHERE value IS NOT NULL AND geography IS NOT NULL
