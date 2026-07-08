SELECT
    geography,
    geo_level,
    CAST(year AS INTEGER) AS year,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "forum-brasileiro-seguranca-lesao-corporal-seguida-de-morte-por-numero-de-ocorrencias-e-numero-de"
WHERE value IS NOT NULL AND geography IS NOT NULL
