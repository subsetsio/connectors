SELECT
    geography,
    geo_level,
    CAST(year AS INTEGER) AS year,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "forum-brasileiro-seguranca-medidas-protetivas-de-urgencia-distribuidas-e-concedidas-pelos-tribuna-t52"
WHERE value IS NOT NULL AND geography IS NOT NULL
