SELECT
    geography,
    geo_level,
    CAST(year AS INTEGER) AS year,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "forum-brasileiro-seguranca-homicidios-dolosos-por-numero-de-vitimas-e-ocorrencias"
WHERE value IS NOT NULL AND geography IS NOT NULL
