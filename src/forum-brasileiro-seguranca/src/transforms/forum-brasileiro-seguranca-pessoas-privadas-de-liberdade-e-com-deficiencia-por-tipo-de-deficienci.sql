SELECT
    geography,
    geo_level,
    CAST(year AS INTEGER) AS year,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "forum-brasileiro-seguranca-pessoas-privadas-de-liberdade-e-com-deficiencia-por-tipo-de-deficienci"
WHERE value IS NOT NULL AND geography IS NOT NULL
