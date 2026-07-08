SELECT
    station,
    measure,
    make_date(year, month, day) AS date,
    CAST(TRY_CAST(value AS DOUBLE) AS DOUBLE) AS temperature_c,
    completeness
FROM "hong-kong-observatory-daily-temperature"
WHERE TRY_CAST(value AS DOUBLE) IS NOT NULL
