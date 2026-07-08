SELECT
    geography,
    geo_level,
    CAST(year AS INTEGER) AS year,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "forum-brasileiro-seguranca-lesao-corporal-dolosa-em-contexto-de-violencia-domestica-art-129-9o-do"
WHERE value IS NOT NULL AND geography IS NOT NULL
