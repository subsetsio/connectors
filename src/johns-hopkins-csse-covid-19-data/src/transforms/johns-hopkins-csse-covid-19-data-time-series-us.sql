SELECT
    CAST(date AS DATE)                          AS date,
    uid,
    iso2,
    iso3,
    fips,
    admin2,
    province_state,
    combined_key,
    TRY_CAST(lat AS DOUBLE)                     AS lat,
    TRY_CAST(long AS DOUBLE)                    AS long,
    TRY_CAST(TRY_CAST(population AS DOUBLE) AS BIGINT) AS population,
    metric,
    TRY_CAST(TRY_CAST(value AS DOUBLE) AS BIGINT) AS value
FROM "johns-hopkins-csse-covid-19-data-time-series-us"
WHERE value IS NOT NULL
