SELECT
    geography,
    geo_level,
    CAST(year AS INTEGER) AS year,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "forum-brasileiro-seguranca-total-de-pessoas-privadas-de-liberdade-por-tipo-de-estabelecimento-e-s"
WHERE value IS NOT NULL AND geography IS NOT NULL
