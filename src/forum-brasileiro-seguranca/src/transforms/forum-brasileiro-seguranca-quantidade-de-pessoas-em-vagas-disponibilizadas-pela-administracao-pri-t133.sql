SELECT
    geography,
    geo_level,
    CAST(year AS INTEGER) AS year,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "forum-brasileiro-seguranca-quantidade-de-pessoas-em-vagas-disponibilizadas-pela-administracao-pri-t133"
WHERE value IS NOT NULL AND geography IS NOT NULL
