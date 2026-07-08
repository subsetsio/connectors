SELECT
    geography,
    geo_level,
    CAST(year AS INTEGER) AS year,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "forum-brasileiro-seguranca-registros-de-posse-ou-porte-ilegais-de-arma-de-fogo-arts-12-14-e-16-le"
WHERE value IS NOT NULL AND geography IS NOT NULL
