SELECT
    iso3_code,
    country,
    region,
    subregion,
    indicator,
    dimension,
    category,
    sex,
    age,
    CAST(TRY_CAST(year AS DOUBLE) AS INTEGER) AS year,
    unit_of_measurement                       AS unit,
    value                                     AS value_raw,
    -- VALUE carries English-formatted numbers (period decimal, comma
    -- thousands sep) and censored entries like "<5"; strip the grouping
    -- commas so real magnitudes parse, leaving censored strings NULL.
    TRY_CAST(REPLACE(value, ',', '') AS DOUBLE) AS value,
    source
FROM "unodc-data-cts-violent-and-sexual-crime"
WHERE value IS NOT NULL
