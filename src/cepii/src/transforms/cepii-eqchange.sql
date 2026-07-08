SELECT
    series,
    CAST(year AS INTEGER)    AS year,
    country,
    TRY_CAST(value AS DOUBLE) AS index_2010_100
FROM "cepii-eqchange"
WHERE TRY_CAST(value AS DOUBLE) IS NOT NULL
