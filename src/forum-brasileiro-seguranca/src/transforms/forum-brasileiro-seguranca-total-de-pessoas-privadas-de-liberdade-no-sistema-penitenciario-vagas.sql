SELECT
    geography,
    geo_level,
    CAST(year AS INTEGER) AS year,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "forum-brasileiro-seguranca-total-de-pessoas-privadas-de-liberdade-no-sistema-penitenciario-vagas"
WHERE value IS NOT NULL AND geography IS NOT NULL
