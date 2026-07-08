SELECT
    geography,
    geo_level,
    CAST(year AS INTEGER) AS year,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "forum-brasileiro-seguranca-producao-ou-distribuicao-de-material-de-abuso-sexual-infantil-art-240"
WHERE value IS NOT NULL AND geography IS NOT NULL
