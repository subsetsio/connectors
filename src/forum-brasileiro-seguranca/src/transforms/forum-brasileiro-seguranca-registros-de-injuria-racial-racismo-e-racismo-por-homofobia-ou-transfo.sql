SELECT
    geography,
    geo_level,
    CAST(year AS INTEGER) AS year,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "forum-brasileiro-seguranca-registros-de-injuria-racial-racismo-e-racismo-por-homofobia-ou-transfo"
WHERE value IS NOT NULL AND geography IS NOT NULL
