SELECT
    geography,
    geo_level,
    CAST(year AS INTEGER) AS year,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "forum-brasileiro-seguranca-apreensao-de-maconha-e-cocaina-em-kg-segundo-as-secretarias-de-seguran"
WHERE value IS NOT NULL AND geography IS NOT NULL
