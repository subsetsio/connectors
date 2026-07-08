SELECT
    geography,
    geo_level,
    CAST(year AS INTEGER) AS year,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "forum-brasileiro-seguranca-numero-de-registros-de-descumprimento-de-medida-protetiva-de-urgencia"
WHERE value IS NOT NULL AND geography IS NOT NULL
