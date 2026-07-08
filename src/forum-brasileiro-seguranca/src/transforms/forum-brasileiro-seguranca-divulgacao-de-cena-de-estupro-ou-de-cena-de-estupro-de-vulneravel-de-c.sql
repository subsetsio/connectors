SELECT
    geography,
    geo_level,
    CAST(year AS INTEGER) AS year,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "forum-brasileiro-seguranca-divulgacao-de-cena-de-estupro-ou-de-cena-de-estupro-de-vulneravel-de-c"
WHERE value IS NOT NULL AND geography IS NOT NULL
