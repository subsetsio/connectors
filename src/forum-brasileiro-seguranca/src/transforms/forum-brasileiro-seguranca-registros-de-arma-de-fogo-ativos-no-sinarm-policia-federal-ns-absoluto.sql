SELECT
    geography,
    geo_level,
    CAST(year AS INTEGER) AS year,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "forum-brasileiro-seguranca-registros-de-arma-de-fogo-ativos-no-sinarm-policia-federal-ns-absoluto"
WHERE value IS NOT NULL AND geography IS NOT NULL
