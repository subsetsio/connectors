SELECT
    uid,
    iso2,
    iso3,
    TRY_CAST(code3 AS BIGINT)                  AS code3,
    fips,
    admin2,
    province_state,
    country_region,
    TRY_CAST(lat AS DOUBLE)                    AS lat,
    TRY_CAST(long AS DOUBLE)                   AS long,
    combined_key,
    TRY_CAST(TRY_CAST(population AS DOUBLE) AS BIGINT) AS population
FROM "johns-hopkins-csse-covid-19-data-lookup-table"
WHERE uid IS NOT NULL
