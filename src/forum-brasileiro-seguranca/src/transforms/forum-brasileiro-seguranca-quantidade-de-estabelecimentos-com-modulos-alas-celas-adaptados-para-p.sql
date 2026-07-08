SELECT
    geography,
    geo_level,
    CAST(year AS INTEGER) AS year,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "forum-brasileiro-seguranca-quantidade-de-estabelecimentos-com-modulos-alas-celas-adaptados-para-p"
WHERE value IS NOT NULL AND geography IS NOT NULL
