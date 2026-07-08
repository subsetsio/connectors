SELECT
    geography,
    geo_level,
    CAST(year AS INTEGER) AS year,
    measure,
    CAST(value AS DOUBLE) AS value
FROM "forum-brasileiro-seguranca-numero-de-municoes-apreendidas-pela-policia-rodoviaria-federal"
WHERE value IS NOT NULL AND geography IS NOT NULL
