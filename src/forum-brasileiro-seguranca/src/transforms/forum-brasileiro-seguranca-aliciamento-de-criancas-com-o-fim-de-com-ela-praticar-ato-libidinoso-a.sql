SELECT
    geography,
    geo_level,
    CAST(year AS INTEGER) AS year,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "forum-brasileiro-seguranca-aliciamento-de-criancas-com-o-fim-de-com-ela-praticar-ato-libidinoso-a"
WHERE value IS NOT NULL AND geography IS NOT NULL
