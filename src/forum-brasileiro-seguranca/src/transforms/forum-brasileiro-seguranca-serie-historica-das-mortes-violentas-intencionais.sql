SELECT
    geography,
    geo_level,
    CAST(year AS INTEGER) AS year,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "forum-brasileiro-seguranca-serie-historica-das-mortes-violentas-intencionais"
WHERE value IS NOT NULL AND geography IS NOT NULL
