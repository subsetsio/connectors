SELECT
    geography,
    geo_level,
    CAST(year AS INTEGER) AS year,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "forum-brasileiro-seguranca-numero-de-adolescentes-apreendidos-em-flagrante-e-por-mandado-judicial"
WHERE value IS NOT NULL AND geography IS NOT NULL
