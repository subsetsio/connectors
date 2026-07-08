SELECT
    indicator,
    geo,
    geo_dim,
    TRY_CAST(time AS INTEGER)  AS year,
    TRY_CAST(value AS DOUBLE)  AS value,
    repo
FROM "gapminder-values"
WHERE TRY_CAST(value AS DOUBLE) IS NOT NULL
  AND TRY_CAST(time AS INTEGER) IS NOT NULL
