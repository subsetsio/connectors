SELECT
    iso3,
    country,
    hdicode,
    region,
    indicator,
    CAST(year AS INTEGER) AS year,
    CAST(value AS DOUBLE) AS value
FROM "undp-composite-indices"
WHERE value IS NOT NULL
