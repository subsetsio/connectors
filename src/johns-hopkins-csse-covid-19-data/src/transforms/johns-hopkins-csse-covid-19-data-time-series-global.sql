SELECT
    CAST(date AS DATE)                          AS date,
    country_region,
    province_state,
    TRY_CAST(lat AS DOUBLE)                     AS lat,
    TRY_CAST(long AS DOUBLE)                    AS long,
    metric,
    TRY_CAST(TRY_CAST(value AS DOUBLE) AS BIGINT) AS value
FROM "johns-hopkins-csse-covid-19-data-time-series-global"
WHERE value IS NOT NULL
