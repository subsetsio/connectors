SELECT
    geography,
    geo_level,
    CAST(year AS INTEGER) AS year,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "forum-brasileiro-seguranca-quantidade-total-de-pessoas-privadas-de-liberdade-em-programas-de-labo"
WHERE value IS NOT NULL AND geography IS NOT NULL
