SELECT
    iso_code3,
    country,
    data_source,
    sector,
    gas,
    unit,
    CAST(year AS SMALLINT)  AS year,
    CAST(value AS DOUBLE)   AS value
FROM "wri-historical-emissions"
WHERE value IS NOT NULL
