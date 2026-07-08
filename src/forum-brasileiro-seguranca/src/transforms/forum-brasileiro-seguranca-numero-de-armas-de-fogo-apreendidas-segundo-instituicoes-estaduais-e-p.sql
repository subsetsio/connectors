SELECT
    geography,
    geo_level,
    CAST(year AS INTEGER) AS year,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "forum-brasileiro-seguranca-numero-de-armas-de-fogo-apreendidas-segundo-instituicoes-estaduais-e-p"
WHERE value IS NOT NULL AND geography IS NOT NULL
